package com.campuscoord.exception;

/**
 * Exception thrown when a booking conflicts with an existing booking.
 * Results in HTTP 409 Conflict response.
 */
public class BookingConflictException extends RuntimeException {
    
    public BookingConflictException(String message) {
        super(message);
    }
    
    /**
     * Constructor with resource and time range
     * @param resourceName Name of the resource being booked
     * @param startTime Start time of the conflict
     * @param endTime End time of the conflict
     */
    public BookingConflictException(String resourceName, String startTime, String endTime) {
        super(String.format("Resource '%s' is already booked between %s and %s", 
            resourceName, startTime, endTime));
    }
}
