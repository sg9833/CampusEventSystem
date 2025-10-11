package com.campuscoord;

import com.campuscoord.exception.*;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.MalformedJwtException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.validation.FieldError;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

@ControllerAdvice
public class GlobalExceptionHandler {
    
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    /**
     * Handle ResourceNotFoundException - 404 Not Found
     */
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
    
    /**
     * Handle DuplicateResourceException - 409 Conflict
     */
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
    
    /**
     * Handle BookingConflictException - 409 Conflict
     */
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
    
    /**
     * Handle AuthenticationException - 401 Unauthorized
     */
    @ExceptionHandler(AuthenticationException.class)
    public ResponseEntity<Map<String, Object>> handleAuthenticationException(
            AuthenticationException ex,
            WebRequest request
    ) {
        logger.warn("Authentication failed: {}", ex.getMessage());
        
        return buildErrorResponse(
            HttpStatus.UNAUTHORIZED,
            "Authentication Failed",
            ex.getMessage(),
            request.getDescription(false)
        );
    }
    
    /**
     * Handle JWT Exceptions - 401 Unauthorized
     * Catches all JWT-related errors from token parsing/validation
     */
    @ExceptionHandler({JwtException.class, ExpiredJwtException.class, MalformedJwtException.class})
    public ResponseEntity<Map<String, Object>> handleJwtException(
            Exception ex,
            WebRequest request
    ) {
        logger.warn("JWT validation failed: {}", ex.getMessage());
        
        String message = "Invalid or expired authentication token";
        if (ex instanceof ExpiredJwtException) {
            message = "Authentication token has expired";
        } else if (ex instanceof MalformedJwtException) {
            message = "Invalid authentication token format";
        }
        
        return buildErrorResponse(
            HttpStatus.UNAUTHORIZED,
            "Authentication Failed",
            message,
            request.getDescription(false)
        );
    }
    
    /**
     * Handle AuthorizationException - 403 Forbidden
     */
    @ExceptionHandler(AuthorizationException.class)
    public ResponseEntity<Map<String, Object>> handleAuthorizationException(
            AuthorizationException ex,
            WebRequest request
    ) {
        logger.warn("Authorization failed: {}", ex.getMessage());
        
        return buildErrorResponse(
            HttpStatus.FORBIDDEN,
            "Access Denied",
            ex.getMessage(),
            request.getDescription(false)
        );
    }
    
    /**
     * Handle Spring Security AccessDeniedException - 403 Forbidden
     */
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
    
    /**
     * Handle IllegalArgumentException - 400 Bad Request
     */
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

    /**
     * Handle validation errors from @Valid annotation
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidationExceptions(
            MethodArgumentNotValidException ex
    ) {
        Map<String, String> fieldErrors = new HashMap<>();
        
        // Extract field errors
        for (FieldError error : ex.getBindingResult().getFieldErrors()) {
            fieldErrors.put(error.getField(), error.getDefaultMessage());
        }
        
        // Extract global errors (like custom @AssertTrue validations)
        for (ObjectError error : ex.getBindingResult().getGlobalErrors()) {
            fieldErrors.put(error.getObjectName(), error.getDefaultMessage());
        }
        
        Map<String, Object> response = new HashMap<>();
        response.put("status", "error");
        response.put("message", "Validation failed");
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("errors", fieldErrors);
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }
    
    /**
     * Handle constraint violation exceptions
     */
    @ExceptionHandler(jakarta.validation.ConstraintViolationException.class)
    public ResponseEntity<Map<String, Object>> handleConstraintViolationException(
            jakarta.validation.ConstraintViolationException ex
    ) {
        Map<String, String> errors = ex.getConstraintViolations().stream()
            .collect(Collectors.toMap(
                violation -> violation.getPropertyPath().toString(),
                violation -> violation.getMessage()
            ));
        
        Map<String, Object> response = new HashMap<>();
        response.put("status", "error");
        response.put("message", "Validation failed");
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("errors", errors);
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    /**
     * Handle IllegalStateException - typically used for booking conflicts
     * @deprecated Use BookingConflictException instead
     */
    @ExceptionHandler(IllegalStateException.class)
    public ResponseEntity<Map<String, Object>> handleIllegalState(
            IllegalStateException ex,
            WebRequest request
    ) {
        logger.warn("Illegal state: {}", ex.getMessage());
        
        return buildErrorResponse(
            HttpStatus.CONFLICT,
            "Conflict",
            ex.getMessage() != null ? ex.getMessage() : "Resource already booked for requested time range",
            request.getDescription(false)
        );
    }

    /**
     * Handle all other uncaught exceptions - 500 Internal Server Error
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleGlobalException(
            Exception ex,
            WebRequest request
    ) {
        logger.error("Unexpected error occurred", ex);
        
        return buildErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR,
            "Internal Server Error",
            "An unexpected error occurred. Please try again later.",
            request.getDescription(false)
        );
    }
    
    /**
     * Build a standardized error response
     */
    private ResponseEntity<Map<String, Object>> buildErrorResponse(
            HttpStatus status,
            String error,
            String message,
            String path
    ) {
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("status", status.value());
        response.put("error", error);
        response.put("message", message);
        response.put("path", path.replace("uri=", "")); // Clean up path
        
        return ResponseEntity.status(status).body(response);
    }
}