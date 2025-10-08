package com.campuscoord.controller;

import com.campuscoord.dto.BookingRequest;
import com.campuscoord.service.BookingService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.format.DateTimeParseException;
import java.util.Map;

@RestController
@RequestMapping("/api/bookings")
public class BookingController {

    private final BookingService bookingService;

    public BookingController(BookingService bookingService) {
        this.bookingService = bookingService;
    }

    @PostMapping
    public ResponseEntity<?> createBooking(@RequestBody BookingRequest req) {
        try {
            LocalDateTime start = LocalDateTime.parse(req.getStartTime());
            LocalDateTime end = LocalDateTime.parse(req.getEndTime());
            int id = bookingService.createBooking(req.getUserId(), req.getResourceId(), start, end, req.getEventId());
            return ResponseEntity.ok(Map.of("bookingId", id, "status", "CONFIRMED"));
        } catch (DateTimeParseException ex) {
            return ResponseEntity.badRequest().body(Map.of("error", "Invalid date format. Use ISO-8601."));
        } catch (IllegalStateException ex) {
            return ResponseEntity.status(409).body(Map.of("error", ex.getMessage()));
        } catch (Exception ex) {
            return ResponseEntity.status(500).body(Map.of("error", ex.getMessage()));
        }
    }
}
