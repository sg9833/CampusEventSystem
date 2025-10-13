package com.campuscoord.controller;

import com.campuscoord.dao.BookingDao;
import com.campuscoord.dao.ResourceDao;
import com.campuscoord.model.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/resources")
public class ResourceController {

    private final ResourceDao resourceDao;
    private final BookingDao bookingDao;

    public ResourceController(ResourceDao resourceDao, BookingDao bookingDao) {
        this.resourceDao = resourceDao;
        this.bookingDao = bookingDao;
    }

    @GetMapping
    public ResponseEntity<List<Resource>> listResources() {
        return ResponseEntity.ok(resourceDao.findAll());
    }

    @GetMapping("/{resourceId}/availability")
    public ResponseEntity<Map<String, Object>> getResourceAvailability(
            @PathVariable int resourceId,
            @RequestParam String date) {
        
        List<String> bookedSlots = bookingDao.getBookedSlotsForDate(resourceId, date);
        
        Map<String, Object> availability = new HashMap<>();
        availability.put("booked_slots", bookedSlots);
        availability.put("unavailable_slots", List.of()); // Can be extended for maintenance/holidays
        
        return ResponseEntity.ok(availability);
    }
}
