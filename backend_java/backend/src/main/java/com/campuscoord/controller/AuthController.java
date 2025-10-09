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

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody Map<String, String> request) {
        try {
            String name = request.get("name");
            String email = request.get("email");
            String password = request.get("password");
            String role = request.get("role");

            // Validate required fields
            if (name == null || email == null || password == null) {
                return ResponseEntity.badRequest().body(Map.of("error", "Missing required fields"));
            }

            // Check if user already exists
            if (userDao.findByEmail(email).isPresent()) {
                return ResponseEntity.badRequest().body(Map.of("error", "User with this email already exists"));
            }

            // Set default role if not provided
            if (role == null || role.isEmpty()) {
                role = "student";
            }

            // Hash the password
            String hashedPassword = BCrypt.hashpw(password, BCrypt.gensalt());

            // Create user using direct SQL (since we don't have a User entity save method)
            int userId = userDao.createUser(name, email, hashedPassword, role);

            // Return success with user info
            LoginResponse resp = new LoginResponse();
            resp.setId(userId);
            resp.setName(name);
            resp.setEmail(email);
            resp.setRole(role);

            return ResponseEntity.ok(resp);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("error", "Registration failed", "message", e.getMessage()));
        }
    }
}
