package com.campuscoord.controller;

import com.campuscoord.dao.ResourceDao;
import com.campuscoord.model.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/resources")
public class ResourceController {

    private final ResourceDao resourceDao;

    public ResourceController(ResourceDao resourceDao) {
        this.resourceDao = resourceDao;
    }

    @GetMapping
    public ResponseEntity<List<Resource>> listResources() {
        return ResponseEntity.ok(resourceDao.findAll());
    }
}
