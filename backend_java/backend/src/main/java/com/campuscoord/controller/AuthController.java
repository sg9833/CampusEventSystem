package com.campuscoord.controller;

import com.campuscoord.dao.UserDao;
import com.campuscoord.dto.LoginRequest;
import com.campuscoord.dto.LoginResponse;
import com.campuscoord.dto.RegisterRequest;
import com.campuscoord.exception.AuthenticationException;
import com.campuscoord.exception.DuplicateResourceException;
import com.campuscoord.security.JwtUtil;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCrypt;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserDao userDao;
    private final JwtUtil jwtUtil;

    public AuthController(UserDao userDao, JwtUtil jwtUtil) {
        this.userDao = userDao;
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest req) {
        return userDao.findByEmail(req.getEmail())
                .map(user -> {
                    if (BCrypt.checkpw(req.getPassword(), user.getPasswordHash())) {
                        // Generate JWT token
                        String token = jwtUtil.generateToken(
                            user.getEmail(),
                            user.getRole(),
                            user.getId()
                        );
                        
                        LoginResponse resp = new LoginResponse();
                        resp.setId(user.getId());
                        resp.setName(user.getName());
                        resp.setEmail(user.getEmail());
                        resp.setRole(user.getRole());
                        resp.setToken(token);  // Add token to response
                        
                        return ResponseEntity.ok(resp);
                    } else {
                        throw AuthenticationException.invalidCredentials();
                    }
                })
                .orElseThrow(AuthenticationException::invalidCredentials);
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody RegisterRequest request) {
        String name = request.getName();
        String email = request.getEmail();
        String password = request.getPassword();
        String role = request.getRole();

        // Check if user already exists
        if (userDao.findByEmail(email).isPresent()) {
            throw new DuplicateResourceException("User", "email", email);
        }

        // Set default role if not provided
        if (role == null || role.isEmpty()) {
            role = "student";
        }

        // Hash the password
        String hashedPassword = BCrypt.hashpw(password, BCrypt.gensalt());

        // Create user using direct SQL (since we don't have a User entity save method)
        int userId = userDao.createUser(name, email, hashedPassword, role);

        // Generate JWT token for newly registered user
        String token = jwtUtil.generateToken(email, role, userId);

        // Return success with user info and token
        LoginResponse resp = new LoginResponse();
        resp.setId(userId);
        resp.setName(name);
        resp.setEmail(email);
        resp.setRole(role);
        resp.setToken(token);  // Add token to response

        return ResponseEntity.ok(resp);
    }

    @PostMapping("/refresh")
    public ResponseEntity<?> refreshToken(@RequestHeader(value = "Authorization", required = false) String authHeader) {
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            throw AuthenticationException.tokenInvalid();
        }
        
        String oldToken = authHeader.substring(7);
        
        if (!jwtUtil.validateToken(oldToken)) {
            throw AuthenticationException.tokenExpired();
        }
        
        String email = jwtUtil.extractEmail(oldToken);
        String role = jwtUtil.extractRole(oldToken);
        Integer userId = jwtUtil.extractUserId(oldToken);
        
        String newToken = jwtUtil.generateToken(email, role, userId);
        
        return ResponseEntity.ok(Map.of("token", newToken));
    }
}
