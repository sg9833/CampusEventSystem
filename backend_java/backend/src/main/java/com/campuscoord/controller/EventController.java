package com.campuscoord.controller;

import com.campuscoord.dao.EventDao;
import com.campuscoord.dto.CreateEventRequest;
import com.campuscoord.model.Event;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/events")
public class EventController {

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
}
