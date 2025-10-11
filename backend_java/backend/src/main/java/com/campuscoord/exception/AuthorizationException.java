package com.campuscoord.exception;

/**
 * Exception thrown when a user doesn't have permission to access a resource.
 * Results in HTTP 403 Forbidden response.
 */
public class AuthorizationException extends RuntimeException {
    
    public AuthorizationException(String message) {
        super(message);
    }
    
    public static AuthorizationException insufficientPermissions() {
        return new AuthorizationException("You don't have permission to perform this action");
    }
    
    public static AuthorizationException insufficientPermissions(String action) {
        return new AuthorizationException(String.format("You don't have permission to %s", action));
    }
}
