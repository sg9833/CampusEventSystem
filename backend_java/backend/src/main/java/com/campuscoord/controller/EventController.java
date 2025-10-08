package com.campuscoord.controller;

import com.campuscoord.dao.EventDao;
import com.campuscoord.model.Event;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.format.DateTimeParseException;
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

    // Accept minimal event data in request body and create
    @PostMapping
    public ResponseEntity<?> createEvent(@RequestBody Map<String, Object> body) {
        try {
            String title = (String) body.get("title");
            String description = (String) body.get("description");
            Integer organizerId = body.get("organizerId") == null ? null : ((Number) body.get("organizerId")).intValue();
            String startStr = (String) body.get("startTime");
            String endStr = (String) body.get("endTime");
            String venue = (String) body.get("venue");

            LocalDateTime start = startStr == null ? null : LocalDateTime.parse(startStr);
            LocalDateTime end = endStr == null ? null : LocalDateTime.parse(endStr);

            Event event = new Event(0, title, description, organizerId, start, end, venue, LocalDateTime.now());
            int id = eventDao.create(event);
            Map<String, Object> resp = new HashMap<>();
            resp.put("id", id);
            return ResponseEntity.ok(resp);
        } catch (DateTimeParseException ex) {
            return ResponseEntity.badRequest().body(Map.of("error", "Invalid date format for startTime or endTime. Use ISO-8601."));
        } catch (Exception ex) {
            return ResponseEntity.status(500).body(Map.of("error", ex.getMessage()));
        }
    }
}
