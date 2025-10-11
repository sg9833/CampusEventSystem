package com.campuscoord.exception;

/**
 * Exception thrown when authentication fails.
 * Results in HTTP 401 Unauthorized response.
 */
public class AuthenticationException extends RuntimeException {
    
    public AuthenticationException(String message) {
        super(message);
    }
    
    public static AuthenticationException invalidCredentials() {
        return new AuthenticationException("Invalid email or password");
    }
    
    public static AuthenticationException tokenExpired() {
        return new AuthenticationException("Authentication token has expired");
    }
    
    public static AuthenticationException tokenInvalid() {
        return new AuthenticationException("Invalid authentication token");
    }
}
