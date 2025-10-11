package com.campuscoord.exception;

/**
 * Exception thrown when attempting to create a resource that already exists.
 * Results in HTTP 409 Conflict response.
 */
public class DuplicateResourceException extends RuntimeException {
    
    public DuplicateResourceException(String message) {
        super(message);
    }
    
    /**
     * Constructor with resource type and field
     * @param resource Type of resource (e.g., "User", "Event")
     * @param field Field that caused the duplicate (e.g., "email")
     * @param value Value of the duplicate field
     */
    public DuplicateResourceException(String resource, String field, String value) {
        super(String.format("%s with %s '%s' already exists", resource, field, value));
    }
}
