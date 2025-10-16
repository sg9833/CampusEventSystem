package com.campuscoord.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import java.time.LocalDateTime;

@Entity
public class EventRegistration {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private int eventId;
    private int userId;
    private LocalDateTime registeredAt;
    private String status;

    public EventRegistration() {}

    public EventRegistration(int id, int eventId, int userId, LocalDateTime registeredAt, String status) {
        this.id = id;
        this.eventId = eventId;
        this.userId = userId;
        this.registeredAt = registeredAt;
        this.status = status;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public int getEventId() { return eventId; }
    public void setEventId(int eventId) { this.eventId = eventId; }

    public int getUserId() { return userId; }
    public void setUserId(int userId) { this.userId = userId; }

    public LocalDateTime getRegisteredAt() { return registeredAt; }
    public void setRegisteredAt(LocalDateTime registeredAt) { this.registeredAt = registeredAt; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    @Override
    public String toString() {
        return "EventRegistration{" +
                "id=" + id +
                ", eventId=" + eventId +
                ", userId=" + userId +
                ", registeredAt=" + registeredAt +
                ", status='" + status + '\'' +
                '}';
    }
}
