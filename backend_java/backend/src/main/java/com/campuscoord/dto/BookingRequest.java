package com.campuscoord.dto;

import jakarta.validation.constraints.*;

public class BookingRequest {

    @Positive(message = "Event ID must be positive")
    private Integer eventId; // optional
    
    @NotNull(message = "User ID is required")
    @Positive(message = "User ID must be positive")
    private Integer userId;
    
    @NotNull(message = "Resource ID is required")
    @Positive(message = "Resource ID must be positive")
    private Integer resourceId;
    
    @NotBlank(message = "Start time is required")
    @Pattern(regexp = "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.*$", message = "Start time must be in ISO-8601 format")
    private String startTime; // ISO-8601 string
    
    @NotBlank(message = "End time is required")
    @Pattern(regexp = "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.*$", message = "End time must be in ISO-8601 format")
    private String endTime;   // ISO-8601 string

    public BookingRequest() {}

    public Integer getEventId() { return eventId; }
    public void setEventId(Integer eventId) { this.eventId = eventId; }

    public Integer getUserId() { return userId; }
    public void setUserId(Integer userId) { this.userId = userId; }

    public Integer getResourceId() { return resourceId; }
    public void setResourceId(Integer resourceId) { this.resourceId = resourceId; }

    public String getStartTime() { return startTime; }
    public void setStartTime(String startTime) { this.startTime = startTime; }

    public String getEndTime() { return endTime; }
    public void setEndTime(String endTime) { this.endTime = endTime; }
}
