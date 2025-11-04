package com.campuscoord.controller;

import com.campuscoord.dao.EventDao;
import com.campuscoord.dao.BookingDao;
import com.campuscoord.model.Event;
import com.campuscoord.model.Booking;
import com.campuscoord.model.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    private static final Logger logger = LoggerFactory.getLogger(AdminController.class);
    private final EventDao eventDao;
    private final BookingDao bookingDao;

    public AdminController(EventDao eventDao, BookingDao bookingDao) {
        this.eventDao = eventDao;
        this.bookingDao = bookingDao;
    }

    // Get all pending events for approval
    @GetMapping("/events/pending")
    public ResponseEntity<?> getPendingEvents(@AuthenticationPrincipal User user) {
        try {
            if (user == null || !"ADMIN".equalsIgnoreCase(user.getRole())) {
                return ResponseEntity.status(403).body(Map.of("error", "Admin access required"));
            }

            List<Event> allEvents = eventDao.findAll();
            List<Event> pendingEvents = allEvents.stream()
                .filter(event -> "pending".equalsIgnoreCase(event.getStatus()))
                .collect(Collectors.toList());

            return ResponseEntity.ok(pendingEvents);
        } catch (Exception ex) {
            logger.error("Error fetching pending events: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to fetch pending events", "message", ex.getMessage()));
        }
    }

    // Approve an event
    @PutMapping("/events/{id}/approve")
    public ResponseEntity<?> approveEvent(@PathVariable int id, @AuthenticationPrincipal User user, @RequestBody(required = false) Map<String, String> body) {
        try {
            logger.info("Approve request for event ID: {} by user ID: {}", id, user != null ? user.getId() : "null");
            
            if (user == null || !"ADMIN".equalsIgnoreCase(user.getRole())) {
                return ResponseEntity.status(403).body(Map.of("error", "Admin access required"));
            }

            // Check if event exists
            Event event = eventDao.findById(id);
            if (event == null) {
                return ResponseEntity.status(404).body(Map.of("error", "Event not found"));
            }

            // Update status to approved
            eventDao.updateStatus(id, "approved");

            Map<String, Object> resp = new HashMap<>();
            resp.put("message", "Event approved successfully");
            resp.put("event_id", id);
            resp.put("event_title", event.getTitle());
            logger.info("Event {} approved by admin {}", id, user.getId());
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            logger.error("Error approving event: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to approve event", "message", ex.getMessage()));
        }
    }

    // Reject an event
    @PutMapping("/events/{id}/reject")
    public ResponseEntity<?> rejectEvent(@PathVariable int id, @AuthenticationPrincipal User user, @RequestBody(required = false) Map<String, String> body) {
        try {
            logger.info("Reject request for event ID: {} by user ID: {}", id, user != null ? user.getId() : "null");
            
            if (user == null || !"ADMIN".equalsIgnoreCase(user.getRole())) {
                return ResponseEntity.status(403).body(Map.of("error", "Admin access required"));
            }

            // Check if event exists
            Event event = eventDao.findById(id);
            if (event == null) {
                return ResponseEntity.status(404).body(Map.of("error", "Event not found"));
            }

            // Update status to rejected
            eventDao.updateStatus(id, "rejected");

            String reason = body != null ? body.get("reason") : "Not specified";
            Map<String, Object> resp = new HashMap<>();
            resp.put("message", "Event rejected");
            resp.put("event_id", id);
            resp.put("event_title", event.getTitle());
            resp.put("reason", reason);
            logger.info("Event {} rejected by admin {} with reason: {}", id, user.getId(), reason);
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            logger.error("Error rejecting event: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to reject event", "message", ex.getMessage()));
        }
    }

    // Get all pending bookings for approval
    @GetMapping("/bookings/pending")
    public ResponseEntity<?> getPendingBookings(@AuthenticationPrincipal User user) {
        try {
            if (user == null || !"ADMIN".equalsIgnoreCase(user.getRole())) {
                return ResponseEntity.status(403).body(Map.of("error", "Admin access required"));
            }

            List<Booking> pendingBookings = bookingDao.findPendingBookings();
            return ResponseEntity.ok(pendingBookings);
        } catch (Exception ex) {
            logger.error("Error fetching pending bookings: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to fetch pending bookings", "message", ex.getMessage()));
        }
    }

    // Approve a booking
    @PutMapping("/bookings/{id}/approve")
    public ResponseEntity<?> approveBooking(@PathVariable int id, @AuthenticationPrincipal User user) {
        try {
            logger.info("Approve request for booking ID: {} by user ID: {}", id, user != null ? user.getId() : "null");
            
            if (user == null || !"ADMIN".equalsIgnoreCase(user.getRole())) {
                return ResponseEntity.status(403).body(Map.of("error", "Admin access required"));
            }

            // Check if booking exists
            Booking booking = bookingDao.findById(id);
            if (booking == null) {
                return ResponseEntity.status(404).body(Map.of("error", "Booking not found"));
            }

            // Update status to approved
            bookingDao.updateStatus(id, "approved");

            Map<String, Object> resp = new HashMap<>();
            resp.put("message", "Booking approved successfully");
            resp.put("booking_id", id);
            logger.info("Booking {} approved by admin {}", id, user.getId());
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            logger.error("Error approving booking: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to approve booking", "message", ex.getMessage()));
        }
    }

    // Reject a booking
    @PutMapping("/bookings/{id}/reject")
    public ResponseEntity<?> rejectBooking(@PathVariable int id, @AuthenticationPrincipal User user, @RequestBody(required = false) Map<String, String> body) {
        try {
            logger.info("Reject request for booking ID: {} by user ID: {}", id, user != null ? user.getId() : "null");
            
            if (user == null || !"ADMIN".equalsIgnoreCase(user.getRole())) {
                return ResponseEntity.status(403).body(Map.of("error", "Admin access required"));
            }

            // Check if booking exists
            Booking booking = bookingDao.findById(id);
            if (booking == null) {
                return ResponseEntity.status(404).body(Map.of("error", "Booking not found"));
            }

            // Update status to rejected
            bookingDao.updateStatus(id, "rejected");

            String reason = body != null ? body.get("reason") : "Not specified";
            Map<String, Object> resp = new HashMap<>();
            resp.put("message", "Booking rejected");
            resp.put("booking_id", id);
            resp.put("reason", reason);
            logger.info("Booking {} rejected by admin {} with reason: {}", id, user.getId(), reason);
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            logger.error("Error rejecting booking: ", ex);
            return ResponseEntity.status(500).body(Map.of("error", "Failed to reject booking", "message", ex.getMessage()));
        }
    }
}
