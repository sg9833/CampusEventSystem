package com.campuscoord.exception;

/**
 * Exception thrown when a requested resource is not found.
 * Results in HTTP 404 Not Found response.
 */
public class ResourceNotFoundException extends RuntimeException {
    
    public ResourceNotFoundException(String message) {
        super(message);
    }
    
    /**
     * Constructor with resource type and ID
     * @param resource Type of resource (e.g., "Event", "User", "Booking")
     * @param id ID of the resource
     */
    public ResourceNotFoundException(String resource, Integer id) {
        super(String.format("%s with ID %d not found", resource, id));
    }
    
    /**
     * Constructor with resource type, field, and value
     * @param resource Type of resource
     * @param field Field name (e.g., "email", "name")
     * @param value Field value
     */
    public ResourceNotFoundException(String resource, String field, String value) {
        super(String.format("%s with %s '%s' not found", resource, field, value));
    }
}
