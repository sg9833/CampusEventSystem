package com.campuscoord.controller;

import com.campuscoord.dao.EventDao;
import com.campuscoord.dto.CreateEventRequest;
import com.campuscoord.model.Event;
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

@RestController
@RequestMapping("/api/events")
public class EventController {

    private static final Logger logger = LoggerFactory.getLogger(EventController.class);
    private final EventDao eventDao;

    public EventController(EventDao eventDao) {
        this.eventDao = eventDao;
    }

    @GetMapping
    public ResponseEntity<List<Event>> listEvents() {
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
                LocalDateTime.now()
            );
            
            int id = eventDao.create(event);
            Map<String, Object> resp = new HashMap<>();
            resp.put("id", id);
            resp.put("message", "Event created successfully");
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            return ResponseEntity.status(500).body(Map.of("error", "Failed to create event", "message", ex.getMessage()));
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
