package com.campuscoord.controller;

import com.campuscoord.dao.EventDao;
import com.campuscoord.dao.EventRegistrationDao;
import com.campuscoord.dto.CreateEventRequest;
import com.campuscoord.model.Event;
import com.campuscoord.model.EventRegistration;
import com.campuscoord.model.User;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/events")
public class EventController {

    private static final Logger logger = LoggerFactory.getLogger(EventController.class);
    private final EventDao eventDao;
    private final EventRegistrationDao registrationDao;

    public EventController(EventDao eventDao, EventRegistrationDao registrationDao) {
        this.eventDao = eventDao;
        this.registrationDao = registrationDao;
    }

    @GetMapping
    public ResponseEntity<List<Event>> listEvents(@AuthenticationPrincipal User user) {
        // Students should only see approved events
        // Organizers and Admins can see all events
        if (user != null && "STUDENT".equals(user.getRole())) {
            return ResponseEntity.ok(eventDao.findApproved());
        }
        return ResponseEntity.ok(eventDao.findAll());
    }

    // Accept validated event data in request body and create
    @PostMapping
    public ResponseEntity<?> createEvent(@Valid @RequestBody CreateEventRequest request) {
        try {
            Event event = new Event(
                0,
                request.getTitle(),
                request.getDescription(),
                request.getOrganizerId(),
                request.getStartTime(),
                request.getEndTime(),
                request.getVenue(),
                "pending", // New events are pending by default
                LocalDateTime.now()
            );
            
            int id = eventDao.create(event);
            Map<String, Object> resp = new HashMap<>();
            resp.put("id", id);
            resp.put("message", "Event created successfully and pending approval");
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            return ResponseEntity.status(500).body(Map.of("error", "Failed to create event", "message", ex.getMessage()));
        }
    }

    // Register for an event
    @PostMapping("/{id}/register")
    public ResponseEntity<?> registerForEvent(@PathVariable int id, @AuthenticationPrincipal User user) {
        try {
            logger.info("Registration request for event ID: {} by user ID: {}", id, user.getId());
            
            if (user == null) {
                return ResponseEntity.status(401).body(Map.of("error", "Unauthorized"));
            }

            // Check if event exists
            Event event = eventDao.findById(id);
            if (event == null) {
                return ResponseEntity.status(404).body(Map.of("error", "Event not found"));
            }

            // Check if event is approved
            if (!"approved".equalsIgnoreCase(event.getStatus())) {
                return ResponseEntity.status(400).body(Map.of("error", "Cannot register for non-approved events"));
            }

            // Check if already registered
            EventRegistration existing = registrationDao.findByEventAndUser(id, user.getId());
            if (existing != null) {
                return ResponseEntity.status(400).body(Map.of("error", "Already registered for this event"));
            }

            // Create registration
            EventRegistration registration = new EventRegistration(
                0,
                id,
                user.getId(),
                LocalDateTime.now(),
                "active"
            );
            int registrationId = registrationDao.create(registration);

            Map<String, Object> resp = new HashMap<>();
            resp.put("id", registrationId);
            resp.put("message", "Successfully registered for event");
            resp.put("event_title", event.getTitle());
            logger.info("User {} successfully registered for event {}", user.getId(), id);
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            logger.error("Error registering for event: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to register for event", "message", ex.getMessage()));
        }
    }

    // Unregister from an event
    @DeleteMapping("/{id}/register")
    public ResponseEntity<?> unregisterFromEvent(@PathVariable int id, @AuthenticationPrincipal User user) {
        try {
            logger.info("Unregistration request for event ID: {} by user ID: {}", id, user.getId());
            
            if (user == null) {
                return ResponseEntity.status(401).body(Map.of("error", "Unauthorized"));
            }

            // Check if registered
            EventRegistration existing = registrationDao.findByEventAndUser(id, user.getId());
            if (existing == null) {
                return ResponseEntity.status(400).body(Map.of("error", "Not registered for this event"));
            }

            // Delete registration
            registrationDao.delete(id, user.getId());

            Map<String, Object> resp = new HashMap<>();
            resp.put("message", "Successfully unregistered from event");
            logger.info("User {} successfully unregistered from event {}", user.getId(), id);
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            logger.error("Error unregistering from event: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to unregister from event", "message", ex.getMessage()));
        }
    }

    // Get registered events for current user
    @GetMapping("/registered")
    public ResponseEntity<?> getRegisteredEvents(@AuthenticationPrincipal User user) {
        try {
            if (user == null) {
                return ResponseEntity.status(401).body(Map.of("error", "Unauthorized"));
            }

            List<EventRegistration> registrations = registrationDao.findByUserId(user.getId());
            List<Event> events = registrations.stream()
                .map(reg -> {
                    try {
                        return eventDao.findById(reg.getEventId());
                    } catch (Exception e) {
                        return null;
                    }
                })
                .filter(event -> event != null)
                .collect(Collectors.toList());

            return ResponseEntity.ok(events);
        } catch (Exception ex) {
            logger.error("Error fetching registered events: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to fetch registered events", "message", ex.getMessage()));
        }
    }

    // Get registrations for a specific event (for organizers)
    @GetMapping("/{id}/registrations")
    public ResponseEntity<?> getEventRegistrations(@PathVariable int id, @AuthenticationPrincipal User user) {
        try {
            if (user == null) {
                return ResponseEntity.status(401).body(Map.of("error", "Unauthorized"));
            }

            // Check if event exists
            Event event = eventDao.findById(id);
            if (event == null) {
                return ResponseEntity.status(404).body(Map.of("error", "Event not found"));
            }

            // Only organizer of the event or admin can view registrations
            if (!event.getOrganizerId().equals(user.getId()) && !"ADMIN".equals(user.getRole())) {
                return ResponseEntity.status(403).body(Map.of("error", "You do not have permission to view these registrations"));
            }

            List<EventRegistration> registrations = registrationDao.findByEventId(id);
            int count = registrations.size();

            Map<String, Object> resp = new HashMap<>();
            resp.put("count", count);
            resp.put("registrations", registrations);
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            logger.error("Error fetching event registrations: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to fetch registrations", "message", ex.getMessage()));
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteEvent(@PathVariable int id, @AuthenticationPrincipal User user) {
        try {
            logger.info("DELETE request for event ID: {}", id);
            logger.info("User from JWT - ID: {}, Email: {}, Role: {}", 
                       user != null ? user.getId() : "null", 
                       user != null ? user.getEmail() : "null",
                       user != null ? user.getRole() : "null");
            
            if (user == null) {
                logger.error("User is null - authentication failed");
                return ResponseEntity.status(401).body(Map.of("error", "Unauthorized"));
            }
            
            // Fetch the event to check ownership
            Event event = eventDao.findById(id);
            if (event == null) {
                logger.warn("Event not found: {}", id);
                return ResponseEntity.status(404).body(Map.of("error", "Event not found"));
            }
            
            logger.info("Event found - ID: {}, Title: {}, OrganizerId: {}", 
                       event.getId(), event.getTitle(), event.getOrganizerId());
            
            // Check if user is the owner (or admin can delete any event)
            if (!event.getOrganizerId().equals(user.getId()) && !"ADMIN".equals(user.getRole())) {
                logger.warn("Permission denied - User ID {} trying to delete event with OrganizerId {}", 
                           user.getId(), event.getOrganizerId());
                return ResponseEntity.status(403).body(Map.of("error", "You do not have permission to delete this event"));
            }
            
            logger.info("Permission granted - Deleting event {}", id);
            eventDao.delete(id);
            Map<String, Object> resp = new HashMap<>();
            resp.put("message", "Event deleted successfully");
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            logger.error("Error deleting event: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to delete event", "message", ex.getMessage()));
        }
    }
}
