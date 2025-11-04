# ⚙️ Backend (Spring Boot) - Comprehensive Improvement Recommendations

**Campus Event System - Backend Analysis**  
**Date:** October 10, 2025  
**Version:** 0.0.1-SNAPSHOT  
**Technology Stack:** Java 17, Spring Boot 3.2.2, MySQL, Maven

---

## 📊 Executive Summary

### Current State
- **Framework:** Spring Boot 3.2.2
- **Java Version:** 17
- **Architecture:** REST API with DAO pattern
- **Database:** MySQL with JDBC
- **Authentication:** Basic BCrypt password hashing
- **Status:** ✅ Functional but needs enhancements

### Strengths
✅ Spring Boot framework (modern, maintainable)  
✅ RESTful API design  
✅ Password hashing with BCrypt  
✅ Simple DAO pattern  
✅ Maven for dependency management

### Critical Issues
❌ No authentication/authorization (JWT missing)  
❌ No input validation  
❌ No API documentation (Swagger/OpenAPI)  
❌ Direct JDBC instead of JPA  
❌ No logging framework  
❌ No exception handling  
❌ No database migrations  
❌ No unit tests  
❌ Hardcoded configuration  
❌ No CORS configuration

---

## 🎯 Priority Matrix

| Priority | Category | Impact | Effort | Timeline |
|----------|----------|--------|--------|----------|
| **P0 - Critical** | JWT Authentication | High | Medium | Week 1-2 |
| **P0 - Critical** | Input Validation | High | Low | Week 1 |
| **P0 - Critical** | Exception Handling | High | Low | Week 1 |
| **P0 - Critical** | Application Properties | High | Low | Week 1 |
| **P1 - High** | JPA Migration | High | High | Week 2-3 |
| **P1 - High** | API Documentation | Medium | Low | Week 2 |
| **P1 - High** | Logging Framework | Medium | Low | Week 2 |
| **P1 - High** | Unit Testing | High | High | Week 3-4 |
| **P2 - Medium** | Database Migrations | Medium | Medium | Week 4 |
| **P2 - Medium** | CORS Configuration | Medium | Low | Week 1 |
| **P2 - Medium** | DTOs & Validation | Medium | Medium | Week 3 |
| **P3 - Low** | Caching | Low | Medium | Week 5+ |
| **P3 - Low** | Rate Limiting | Low | Medium | Week 5+ |

---

## 🔴 P0 - CRITICAL IMPROVEMENTS

### 1. JWT Authentication & Authorization ⚠️ CRITICAL

**Current State:**
- ❌ No authentication mechanism
- ❌ No JWT tokens
- ❌ No role-based access control
- ✅ BCrypt password hashing exists

**Problems:**
- API is completely open
- No user sessions
- No protected endpoints
- Security vulnerability

**Recommended Solution:**

#### A. Add JWT Dependencies

**pom.xml:**
```xml
<!-- JWT Authentication -->
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.12.3</version>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.12.3</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.12.3</version>
    <scope>runtime</scope>
</dependency>

<!-- Spring Security -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

#### B. JWT Utility Class

**security/JwtUtil.java:**
```java
package com.campuscoord.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Component
public class JwtUtil {
    
    @Value("${jwt.secret}")
    private String secret;
    
    @Value("${jwt.expiration:86400000}") // 24 hours default
    private Long expiration;
    
    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(secret.getBytes());
    }
    
    public String generateToken(String email, String role, Integer userId) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("role", role);
        claims.put("userId", userId);
        
        return Jwts.builder()
                .setClaims(claims)
                .setSubject(email)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + expiration))
                .signWith(getSigningKey())
                .compact();
    }
    
    public String extractEmail(String token) {
        return extractClaims(token).getSubject();
    }
    
    public String extractRole(String token) {
        return (String) extractClaims(token).get("role");
    }
    
    public Integer extractUserId(String token) {
        return (Integer) extractClaims(token).get("userId");
    }
    
    public boolean validateToken(String token) {
        try {
            extractClaims(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
    
    public boolean isTokenExpired(String token) {
        return extractClaims(token).getExpiration().before(new Date());
    }
    
    private Claims extractClaims(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(getSigningKey())
                .build()
                .parseClaimsJws(token)
                .getBody();
    }
}
```

#### C. JWT Request Filter

**security/JwtRequestFilter.java:**
```java
package com.campuscoord.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Collections;

@Component
public class JwtRequestFilter extends OncePerRequestFilter {
    
    @Autowired
    private JwtUtil jwtUtil;
    
    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain chain
    ) throws ServletException, IOException {
        
        final String authHeader = request.getHeader("Authorization");
        
        String jwt = null;
        String email = null;
        
        // Extract JWT from header
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            jwt = authHeader.substring(7);
            try {
                email = jwtUtil.extractEmail(jwt);
            } catch (Exception e) {
                logger.error("JWT extraction failed", e);
            }
        }
        
        // Validate and set authentication
        if (email != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            if (jwtUtil.validateToken(jwt) && !jwtUtil.isTokenExpired(jwt)) {
                String role = jwtUtil.extractRole(jwt);
                
                UsernamePasswordAuthenticationToken authToken = 
                    new UsernamePasswordAuthenticationToken(
                        email,
                        null,
                        Collections.singletonList(new SimpleGrantedAuthority("ROLE_" + role))
                    );
                
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }
        
        chain.doFilter(request, response);
    }
}
```

#### D. Security Configuration

**security/SecurityConfig.java:**
```java
package com.campuscoord.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Autowired
    private JwtRequestFilter jwtRequestFilter;
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .cors()
            .and()
            .authorizeHttpRequests(auth -> auth
                // Public endpoints
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/health").permitAll()
                
                // Events - authenticated users only
                .requestMatchers(HttpMethod.GET, "/api/events/**").authenticated()
                .requestMatchers(HttpMethod.POST, "/api/events").hasAnyRole("ADMIN", "ORGANIZER")
                .requestMatchers(HttpMethod.PUT, "/api/events/**").hasAnyRole("ADMIN", "ORGANIZER")
                .requestMatchers(HttpMethod.DELETE, "/api/events/**").hasRole("ADMIN")
                
                // Bookings - authenticated users only
                .requestMatchers("/api/bookings/**").authenticated()
                
                // Resources - GET for all, write for admin
                .requestMatchers(HttpMethod.GET, "/api/resources/**").authenticated()
                .requestMatchers(HttpMethod.POST, "/api/resources").hasRole("ADMIN")
                .requestMatchers(HttpMethod.PUT, "/api/resources/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.DELETE, "/api/resources/**").hasRole("ADMIN")
                
                // Users - admin only
                .requestMatchers("/api/users/**").hasRole("ADMIN")
                
                // All other requests require authentication
                .anyRequest().authenticated()
            )
            .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            .and()
            .addFilterBefore(jwtRequestFilter, UsernamePasswordAuthenticationFilter.class);
        
        return http.build();
    }
}
```

#### E. Update AuthController

**controller/AuthController.java:**
```java
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
    public ResponseEntity<?> login(@RequestBody LoginRequest req) {
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
                        resp.setToken(token); // Add token to response
                        
                        return ResponseEntity.ok(resp);
                    } else {
                        return ResponseEntity.status(401)
                            .body(Map.of("error", "Invalid credentials"));
                    }
                })
                .orElseGet(() -> ResponseEntity.status(401)
                    .body(Map.of("error", "Invalid credentials")));
    }
    
    @PostMapping("/refresh")
    public ResponseEntity<?> refreshToken(
            @RequestHeader("Authorization") String authHeader
    ) {
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String oldToken = authHeader.substring(7);
            
            if (jwtUtil.validateToken(oldToken)) {
                String email = jwtUtil.extractEmail(oldToken);
                String role = jwtUtil.extractRole(oldToken);
                Integer userId = jwtUtil.extractUserId(oldToken);
                
                String newToken = jwtUtil.generateToken(email, role, userId);
                
                return ResponseEntity.ok(Map.of("token", newToken));
            }
        }
        
        return ResponseEntity.status(401).body(Map.of("error", "Invalid token"));
    }
}
```

#### F. Add to application.properties

```properties
# JWT Configuration
jwt.secret=your-256-bit-secret-key-change-this-in-production-minimum-32-characters
jwt.expiration=86400000
# Expiration in milliseconds (86400000 = 24 hours)
```

**Effort:** Medium (1-2 weeks)  
**Impact:** High (Critical security requirement)  
**Priority:** P0 - Critical

---

### 2. Input Validation & Sanitization ⚠️ CRITICAL

**Current State:**
- ❌ No validation annotations
- ❌ No input sanitization
- ❌ SQL injection risk
- ❌ XSS vulnerability risk

**Recommended Solution:**

#### A. Add Validation Dependency

**pom.xml:**
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

#### B. Create DTOs with Validation

**dto/CreateEventRequest.java:**
```java
package com.campuscoord.dto;

import jakarta.validation.constraints.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
public class CreateEventRequest {
    
    @NotBlank(message = "Title is required")
    @Size(min = 3, max = 255, message = "Title must be between 3 and 255 characters")
    private String title;
    
    @NotBlank(message = "Description is required")
    @Size(min = 10, max = 5000, message = "Description must be between 10 and 5000 characters")
    private String description;
    
    @NotNull(message = "Organizer ID is required")
    @Positive(message = "Organizer ID must be positive")
    private Integer organizerId;
    
    @NotNull(message = "Start time is required")
    @Future(message = "Start time must be in the future")
    private LocalDateTime startTime;
    
    @NotNull(message = "End time is required")
    @Future(message = "End time must be in the future")
    private LocalDateTime endTime;
    
    @NotBlank(message = "Venue is required")
    @Size(max = 255, message = "Venue must not exceed 255 characters")
    private String venue;
    
    @Size(max = 50, message = "Category must not exceed 50 characters")
    private String category;
    
    @Min(value = 1, message = "Capacity must be at least 1")
    @Max(value = 10000, message = "Capacity must not exceed 10000")
    private Integer capacity;
    
    // Custom validation
    @AssertTrue(message = "End time must be after start time")
    public boolean isEndTimeAfterStartTime() {
        if (startTime == null || endTime == null) {
            return true; // Let @NotNull handle null validation
        }
        return endTime.isAfter(startTime);
    }
}
```

**dto/CreateBookingRequest.java:**
```java
package com.campuscoord.dto;

import jakarta.validation.constraints.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
public class CreateBookingRequest {
    
    @Positive(message = "Event ID must be positive")
    private Integer eventId;
    
    @NotNull(message = "User ID is required")
    @Positive(message = "User ID must be positive")
    private Integer userId;
    
    @NotNull(message = "Resource ID is required")
    @Positive(message = "Resource ID must be positive")
    private Integer resourceId;
    
    @NotNull(message = "Start time is required")
    @Future(message = "Start time must be in the future")
    private LocalDateTime startTime;
    
    @NotNull(message = "End time is required")
    @Future(message = "End time must be in the future")
    private LocalDateTime endTime;
    
    @Size(max = 500, message = "Purpose must not exceed 500 characters")
    private String purpose;
}
```

#### C. Update Controllers with @Valid

**controller/EventController.java:**
```java
@RestController
@RequestMapping("/api/events")
public class EventController {
    
    private final EventDao eventDao;
    
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
            
            return ResponseEntity.ok(Map.of("id", id, "message", "Event created successfully"));
            
        } catch (Exception ex) {
            return ResponseEntity.status(500)
                .body(Map.of("error", "Failed to create event", "details", ex.getMessage()));
        }
    }
}
```

#### D. Global Validation Exception Handler

**exception/ValidationExceptionHandler.java:**
```java
package com.campuscoord.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class ValidationExceptionHandler {
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidationExceptions(
            MethodArgumentNotValidException ex
    ) {
        Map<String, String> errors = new HashMap<>();
        
        ex.getBindingResult().getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });
        
        Map<String, Object> response = new HashMap<>();
        response.put("status", "error");
        response.put("message", "Validation failed");
        response.put("errors", errors);
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }
}
```

**Effort:** Low (1 week)  
**Impact:** High (Prevents invalid data)  
**Priority:** P0 - Critical

---

### 3. Global Exception Handling ⚠️ CRITICAL

**Current State:**
- ✅ `GlobalExceptionHandler` exists but basic
- ❌ Not comprehensive
- ❌ No custom exceptions

**Recommended Solution:**

#### A. Custom Exceptions

**exception/ResourceNotFoundException.java:**
```java
package com.campuscoord.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
    
    public ResourceNotFoundException(String resource, Integer id) {
        super(String.format("%s with ID %d not found", resource, id));
    }
}
```

**exception/DuplicateResourceException.java:**
```java
package com.campuscoord.exception;

public class DuplicateResourceException extends RuntimeException {
    public DuplicateResourceException(String message) {
        super(message);
    }
}
```

**exception/BookingConflictException.java:**
```java
package com.campuscoord.exception;

public class BookingConflictException extends RuntimeException {
    public BookingConflictException(String message) {
        super(message);
    }
}
```

#### B. Enhanced Global Exception Handler

**exception/GlobalExceptionHandler.java:**
```java
package com.campuscoord.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {
    
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleResourceNotFound(
            ResourceNotFoundException ex,
            WebRequest request
    ) {
        logger.warn("Resource not found: {}", ex.getMessage());
        
        return buildErrorResponse(
            HttpStatus.NOT_FOUND,
            "Resource Not Found",
            ex.getMessage(),
            request.getDescription(false)
        );
    }
    
    @ExceptionHandler(DuplicateResourceException.class)
    public ResponseEntity<Map<String, Object>> handleDuplicateResource(
            DuplicateResourceException ex,
            WebRequest request
    ) {
        logger.warn("Duplicate resource: {}", ex.getMessage());
        
        return buildErrorResponse(
            HttpStatus.CONFLICT,
            "Duplicate Resource",
            ex.getMessage(),
            request.getDescription(false)
        );
    }
    
    @ExceptionHandler(BookingConflictException.class)
    public ResponseEntity<Map<String, Object>> handleBookingConflict(
            BookingConflictException ex,
            WebRequest request
    ) {
        logger.warn("Booking conflict: {}", ex.getMessage());
        
        return buildErrorResponse(
            HttpStatus.CONFLICT,
            "Booking Conflict",
            ex.getMessage(),
            request.getDescription(false)
        );
    }
    
    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<Map<String, Object>> handleAccessDenied(
            AccessDeniedException ex,
            WebRequest request
    ) {
        logger.warn("Access denied: {}", ex.getMessage());
        
        return buildErrorResponse(
            HttpStatus.FORBIDDEN,
            "Access Denied",
            "You don't have permission to access this resource",
            request.getDescription(false)
        );
    }
    
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<Map<String, Object>> handleIllegalArgument(
            IllegalArgumentException ex,
            WebRequest request
    ) {
        logger.warn("Invalid argument: {}", ex.getMessage());
        
        return buildErrorResponse(
            HttpStatus.BAD_REQUEST,
            "Invalid Request",
            ex.getMessage(),
            request.getDescription(false)
        );
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleGlobalException(
            Exception ex,
            WebRequest request
    ) {
        logger.error("Unexpected error", ex);
        
        return buildErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR,
            "Internal Server Error",
            "An unexpected error occurred. Please try again later.",
            request.getDescription(false)
        );
    }
    
    private ResponseEntity<Map<String, Object>> buildErrorResponse(
            HttpStatus status,
            String error,
            String message,
            String path
    ) {
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", LocalDateTime.now());
        response.put("status", status.value());
        response.put("error", error);
        response.put("message", message);
        response.put("path", path);
        
        return ResponseEntity.status(status).body(response);
    }
}
```

**Effort:** Low (3-4 days)  
**Impact:** High (Better error handling)  
**Priority:** P0 - Critical

---

### 4. Application Configuration ⚠️ CRITICAL

**Current State:**
- ❌ No application.properties file
- ❌ Hardcoded database connection
- ❌ No environment-specific configs

**Recommended Solution:**

**src/main/resources/application.properties:**
```properties
# Application Name
spring.application.name=Campus Event System

# Server Configuration
server.port=8080
server.servlet.context-path=/

# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/campus_events?useSSL=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# Connection Pool
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000
spring.datasource.hikari.idle-timeout=600000
spring.datasource.hikari.max-lifetime=1800000

# JPA Configuration (when migrated)
spring.jpa.hibernate.ddl-auto=none
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect
spring.jpa.properties.hibernate.format_sql=true

# Logging
logging.level.root=INFO
logging.level.com.campuscoord=DEBUG
logging.level.org.springframework.web=INFO
logging.level.org.springframework.security=DEBUG
logging.file.name=logs/application.log
logging.pattern.console=%d{yyyy-MM-dd HH:mm:ss} - %msg%n
logging.pattern.file=%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n

# JWT Configuration
jwt.secret=${JWT_SECRET:your-256-bit-secret-key-change-this-in-production-minimum-32-characters}
jwt.expiration=86400000

# CORS Configuration
cors.allowed-origins=http://localhost:3000,http://localhost:8080
cors.allowed-methods=GET,POST,PUT,DELETE,OPTIONS
cors.allowed-headers=*
cors.allow-credentials=true

# File Upload
spring.servlet.multipart.enabled=true
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB

# Jackson JSON
spring.jackson.serialization.write-dates-as-timestamps=false
spring.jackson.time-zone=UTC
```

**application-dev.properties:**
```properties
# Development Profile
spring.datasource.url=jdbc:mysql://localhost:3306/campus_events_dev?useSSL=false&serverTimezone=UTC
logging.level.com.campuscoord=DEBUG
spring.jpa.show-sql=true
```

**application-prod.properties:**
```properties
# Production Profile
spring.datasource.url=jdbc:mysql://prod-server:3306/campus_events?useSSL=true&serverTimezone=UTC
logging.level.com.campuscoord=WARN
spring.jpa.show-sql=false

# Use environment variables for sensitive data
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}
jwt.secret=${JWT_SECRET}
```

**Effort:** Low (1 day)  
**Impact:** High (Proper configuration)  
**Priority:** P0 - Critical

---

## 🟡 P1 - HIGH PRIORITY IMPROVEMENTS

### 5. Migrate from JDBC to Spring Data JPA

**Current:** Direct JDBC with JdbcTemplate  
**Recommended:** Spring Data JPA with Hibernate

#### A. Update Dependencies

**pom.xml:**
```xml
<!-- Already have spring-boot-starter-data-jpa -->
<!-- Remove spring-boot-starter-jdbc if not needed -->
```

#### B. Update Entities with JPA Annotations

**model/Event.java:**
```java
package com.campuscoord.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "events")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Event {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    @Column(nullable = false, length = 255)
    private String title;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "organizer_id", nullable = false)
    private Integer organizerId;
    
    @Column(name = "start_time", nullable = false)
    private LocalDateTime startTime;
    
    @Column(name = "end_time", nullable = false)
    private LocalDateTime endTime;
    
    @Column(length = 255)
    private String venue;
    
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
```

#### C. Create JPA Repositories

**repository/EventRepository.java:**
```java
package com.campuscoord.repository;

import com.campuscoord.model.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface EventRepository extends JpaRepository<Event, Integer> {
    
    // Find events by organizer
    List<Event> findByOrganizerId(Integer organizerId);
    
    // Find upcoming events
    List<Event> findByStartTimeAfter(LocalDateTime date);
    
    // Find events by venue
    List<Event> findByVenueContainingIgnoreCase(String venue);
    
    // Custom query - find events in date range
    @Query("SELECT e FROM Event e WHERE e.startTime >= :start AND e.endTime <= :end")
    List<Event> findEventsInDateRange(
        @Param("start") LocalDateTime start,
        @Param("end") LocalDateTime end
    );
    
    // Find events with pagination and sorting
    // Automatic: findAll(Pageable pageable)
}
```

**repository/UserRepository.java:**
```java
package com.campuscoord.repository;

import com.campuscoord.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {
    
    Optional<User> findByEmail(String email);
    
    boolean existsByEmail(String email);
    
    List<User> findByRole(String role);
}
```

#### D. Create Service Layer

**service/EventService.java:**
```java
package com.campuscoord.service;

import com.campuscoord.dto.CreateEventRequest;
import com.campuscoord.exception.ResourceNotFoundException;
import com.campuscoord.model.Event;
import com.campuscoord.repository.EventRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@Transactional
public class EventService {
    
    private final EventRepository eventRepository;
    
    public EventService(EventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }
    
    public List<Event> getAllEvents() {
        return eventRepository.findAll();
    }
    
    public Page<Event> getEvents(Pageable pageable) {
        return eventRepository.findAll(pageable);
    }
    
    public Event getEventById(Integer id) {
        return eventRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Event", id));
    }
    
    public Event createEvent(CreateEventRequest request) {
        Event event = new Event();
        event.setTitle(request.getTitle());
        event.setDescription(request.getDescription());
        event.setOrganizerId(request.getOrganizerId());
        event.setStartTime(request.getStartTime());
        event.setEndTime(request.getEndTime());
        event.setVenue(request.getVenue());
        
        return eventRepository.save(event);
    }
    
    public Event updateEvent(Integer id, CreateEventRequest request) {
        Event event = getEventById(id);
        
        event.setTitle(request.getTitle());
        event.setDescription(request.getDescription());
        event.setStartTime(request.getStartTime());
        event.setEndTime(request.getEndTime());
        event.setVenue(request.getVenue());
        
        return eventRepository.save(event);
    }
    
    public void deleteEvent(Integer id) {
        if (!eventRepository.existsById(id)) {
            throw new ResourceNotFoundException("Event", id);
        }
        eventRepository.deleteById(id);
    }
    
    public List<Event> getUpcomingEvents() {
        return eventRepository.findByStartTimeAfter(LocalDateTime.now());
    }
    
    public List<Event> getEventsByOrganizer(Integer organizerId) {
        return eventRepository.findByOrganizerId(organizerId);
    }
}
```

#### E. Update Controllers to Use Services

**controller/EventController.java:**
```java
@RestController
@RequestMapping("/api/events")
public class EventController {
    
    private final EventService eventService;
    
    public EventController(EventService eventService) {
        this.eventService = eventService;
    }
    
    @GetMapping
    public ResponseEntity<List<Event>> getAllEvents(
        @RequestParam(required = false) Integer organizerId
    ) {
        if (organizerId != null) {
            return ResponseEntity.ok(eventService.getEventsByOrganizer(organizerId));
        }
        return ResponseEntity.ok(eventService.getAllEvents());
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Event> getEventById(@PathVariable Integer id) {
        return ResponseEntity.ok(eventService.getEventById(id));
    }
    
    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'ORGANIZER')")
    public ResponseEntity<Event> createEvent(@Valid @RequestBody CreateEventRequest request) {
        Event created = eventService.createEvent(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'ORGANIZER')")
    public ResponseEntity<Event> updateEvent(
        @PathVariable Integer id,
        @Valid @RequestBody CreateEventRequest request
    ) {
        Event updated = eventService.updateEvent(id, request);
        return ResponseEntity.ok(updated);
    }
    
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> deleteEvent(@PathVariable Integer id) {
        eventService.deleteEvent(id);
        return ResponseEntity.noContent().build();
    }
}
```

**Effort:** High (2-3 weeks)  
**Impact:** High (Better maintainability)  
**Priority:** P1 - High

---

### 6. API Documentation with Swagger/OpenAPI

**Recommended Solution:**

#### A. Add Dependency

**pom.xml:**
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.2.0</version>
</dependency>
```

#### B. Configure Swagger

**config/OpenApiConfig.java:**
```java
package com.campuscoord.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.Components;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {
    
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Campus Event System API")
                .version("1.0.0")
                .description("REST API for Campus Event & Resource Coordination System")
                .contact(new Contact()
                    .name("Development Team")
                    .email("support@campusevents.edu")
                )
            )
            .components(new Components()
                .addSecuritySchemes("bearer-jwt", new SecurityScheme()
                    .type(SecurityScheme.Type.HTTP)
                    .scheme("bearer")
                    .bearerFormat("JWT")
                    .description("JWT token authentication")
                )
            )
            .addSecurityItem(new SecurityRequirement().addList("bearer-jwt"));
    }
}
```

#### C. Add API Documentation Annotations

```java
@RestController
@RequestMapping("/api/events")
@Tag(name = "Events", description = "Event management APIs")
public class EventController {
    
    @Operation(
        summary = "Get all events",
        description = "Returns a list of all events. Optionally filter by organizer ID."
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Success"),
        @ApiResponse(responseCode = "401", description = "Unauthorized"),
        @ApiResponse(responseCode = "500", description = "Internal server error")
    })
    @GetMapping
    public ResponseEntity<List<Event>> getAllEvents(
        @Parameter(description = "Filter by organizer ID") 
        @RequestParam(required = false) Integer organizerId
    ) {
        // ...
    }
}
```

**Access Swagger UI:** `http://localhost:8080/swagger-ui.html`

**Effort:** Low (2-3 days)  
**Impact:** Medium (Better API documentation)  
**Priority:** P1 - High

---

### 7. Comprehensive Unit Testing

#### A. Add Test Dependencies

**pom.xml:**
```xml
<!-- Already have spring-boot-starter-test -->

<!-- Add additional test libraries -->
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>
```

#### B. Service Tests

**src/test/java/com/campuscoord/service/EventServiceTest.java:**
```java
package com.campuscoord.service;

import com.campuscoord.dto.CreateEventRequest;
import com.campuscoord.exception.ResourceNotFoundException;
import com.campuscoord.model.Event;
import com.campuscoord.repository.EventRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class EventServiceTest {
    
    @Mock
    private EventRepository eventRepository;
    
    @InjectMocks
    private EventService eventService;
    
    private Event testEvent;
    
    @BeforeEach
    void setUp() {
        testEvent = new Event();
        testEvent.setId(1);
        testEvent.setTitle("Test Event");
        testEvent.setDescription("Test Description");
        testEvent.setOrganizerId(1);
        testEvent.setStartTime(LocalDateTime.now().plusDays(1));
        testEvent.setEndTime(LocalDateTime.now().plusDays(1).plusHours(2));
        testEvent.setVenue("Test Hall");
    }
    
    @Test
    void getAllEvents_ReturnsAllEvents() {
        // Arrange
        List<Event> events = Arrays.asList(testEvent);
        when(eventRepository.findAll()).thenReturn(events);
        
        // Act
        List<Event> result = eventService.getAllEvents();
        
        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals("Test Event", result.get(0).getTitle());
        verify(eventRepository, times(1)).findAll();
    }
    
    @Test
    void getEventById_ExistingId_ReturnsEvent() {
        // Arrange
        when(eventRepository.findById(1)).thenReturn(Optional.of(testEvent));
        
        // Act
        Event result = eventService.getEventById(1);
        
        // Assert
        assertNotNull(result);
        assertEquals("Test Event", result.getTitle());
        verify(eventRepository, times(1)).findById(1);
    }
    
    @Test
    void getEventById_NonExistingId_ThrowsException() {
        // Arrange
        when(eventRepository.findById(999)).thenReturn(Optional.empty());
        
        // Act & Assert
        assertThrows(ResourceNotFoundException.class, () -> {
            eventService.getEventById(999);
        });
        verify(eventRepository, times(1)).findById(999);
    }
    
    @Test
    void createEvent_ValidRequest_ReturnsCreatedEvent() {
        // Arrange
        CreateEventRequest request = new CreateEventRequest();
        request.setTitle("New Event");
        request.setDescription("New Description");
        request.setOrganizerId(1);
        request.setStartTime(LocalDateTime.now().plusDays(1));
        request.setEndTime(LocalDateTime.now().plusDays(1).plusHours(2));
        request.setVenue("New Hall");
        
        when(eventRepository.save(any(Event.class))).thenReturn(testEvent);
        
        // Act
        Event result = eventService.createEvent(request);
        
        // Assert
        assertNotNull(result);
        verify(eventRepository, times(1)).save(any(Event.class));
    }
    
    @Test
    void deleteEvent_ExistingId_DeletesSuccessfully() {
        // Arrange
        when(eventRepository.existsById(1)).thenReturn(true);
        doNothing().when(eventRepository).deleteById(1);
        
        // Act
        eventService.deleteEvent(1);
        
        // Assert
        verify(eventRepository, times(1)).existsById(1);
        verify(eventRepository, times(1)).deleteById(1);
    }
}
```

#### C. Controller Tests

**src/test/java/com/campuscoord/controller/EventControllerTest.java:**
```java
package com.campuscoord.controller;

import com.campuscoord.model.Event;
import com.campuscoord.service.EventService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;
import java.util.Arrays;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(EventController.class)
class EventControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private EventService eventService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    @WithMockUser
    void getAllEvents_ReturnsEventList() throws Exception {
        // Arrange
        Event event = new Event();
        event.setId(1);
        event.setTitle("Test Event");
        
        when(eventService.getAllEvents()).thenReturn(Arrays.asList(event));
        
        // Act & Assert
        mockMvc.perform(get("/api/events"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].title").value("Test Event"));
    }
    
    @Test
    @WithMockUser(roles = "ADMIN")
    void createEvent_ValidRequest_ReturnsCreated() throws Exception {
        // Arrange
        CreateEventRequest request = new CreateEventRequest();
        request.setTitle("New Event");
        request.setDescription("Description");
        request.setOrganizerId(1);
        request.setStartTime(LocalDateTime.now().plusDays(1));
        request.setEndTime(LocalDateTime.now().plusDays(1).plusHours(2));
        request.setVenue("Hall A");
        
        Event created = new Event();
        created.setId(1);
        created.setTitle(request.getTitle());
        
        when(eventService.createEvent(any())).thenReturn(created);
        
        // Act & Assert
        mockMvc.perform(post("/api/events")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1));
    }
}
```

**Effort:** High (2-3 weeks)  
**Impact:** High (Ensures code quality)  
**Priority:** P1 - High

---

## 🟢 P2 - MEDIUM PRIORITY

### 8. Database Migrations with Flyway

**Add Dependency:**
```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-mysql</artifactId>
</dependency>
```

**Create Migrations:**

**src/main/resources/db/migration/V1__Initial_Schema.sql:**
```sql
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    organizer_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    venue VARCHAR(255),
    category VARCHAR(50),
    capacity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_organizer (organizer_id),
    INDEX idx_start_time (start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Add more tables...
```

**application.properties:**
```properties
# Flyway Configuration
spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration
spring.flyway.baseline-on-migrate=true
```

**Effort:** Medium (1 week)  
**Impact:** Medium (Version control for database)  
**Priority:** P2 - Medium

---

### 9. CORS Configuration

**config/CorsConfig.java:**
```java
package com.campuscoord.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

import java.util.Arrays;

@Configuration
public class CorsConfig {
    
    @Bean
    public CorsFilter corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        
        config.setAllowCredentials(true);
        config.setAllowedOrigins(Arrays.asList("http://localhost:3000", "http://localhost:8080"));
        config.setAllowedHeaders(Arrays.asList("*"));
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setMaxAge(3600L);
        
        source.registerCorsConfiguration("/api/**", config);
        
        return new CorsFilter(source);
    }
}
```

**Effort:** Low (1 day)  
**Impact:** Medium (Frontend can connect)  
**Priority:** P2 - Medium

---

## 📈 Implementation Timeline

### Weeks 1-2: Critical Security
- JWT authentication
- Input validation
- Exception handling
- Application properties
- CORS configuration

### Weeks 3-4: JPA Migration & Testing
- Migrate to Spring Data JPA
- Create repositories & services
- Write unit tests (target 70% coverage)
- Integration tests

### Week 5: Documentation & Optimization
- Add Swagger/OpenAPI
- Add logging framework
- Database migrations with Flyway
- Performance optimization

### Week 6+: Advanced Features
- Caching with Redis
- Rate limiting
- Monitoring with Actuator
- CI/CD setup

---

## 📊 Success Metrics

- **Test Coverage:** 70%+
- **API Response Time:** < 200ms average
- **Security:** All endpoints protected with JWT
- **Documentation:** 100% endpoints documented in Swagger
- **Code Quality:** SonarQube grade A

---

**Document Version:** 1.0  
**Last Updated:** October 10, 2025  
**Status:** Ready for Implementation
