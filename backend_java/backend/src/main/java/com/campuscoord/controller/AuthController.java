package com.campuscoord.controller;

import com.campuscoord.dao.UserDao;
import com.campuscoord.dto.LoginRequest;
import com.campuscoord.dto.LoginResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCrypt;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserDao userDao;

    public AuthController(UserDao userDao) {
        this.userDao = userDao;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest req) {
        return userDao.findByEmail(req.getEmail())
                .map(user -> {
                    if (BCrypt.checkpw(req.getPassword(), user.getPasswordHash())) {
                        LoginResponse resp = new LoginResponse();
                        resp.setId(user.getId());
                        resp.setName(user.getName());
                        resp.setEmail(user.getEmail());
                        resp.setRole(user.getRole());
                        return ResponseEntity.ok(resp);
                    } else {
                        return ResponseEntity.status(401).body(Map.of("error", "Invalid credentials"));
                    }
                })
                .orElseGet(() -> ResponseEntity.status(401).body(Map.of("error", "Invalid credentials")));
    }
}
