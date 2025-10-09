package com.campuscoord.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.HashMap;

@RestController
@RequestMapping("/api/notifications")
@CrossOrigin(origins = "*")
public class NotificationController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    /**
     * Send email notification
     * POST /api/notifications/email
     * Body: {
     *   "to": "user@example.com",
     *   "subject": "Email subject",
     *   "type": "event_registration|event_reminder|booking_confirmation|approval_notification|weekly_digest",
     *   "data": { ... event/booking details ... }
     * }
     */
    @PostMapping("/email")
    public ResponseEntity<?> sendEmail(@RequestBody Map<String, Object> request) {
        try {
            String to = (String) request.get("to");
            String subject = (String) request.get("subject");
            String type = (String) request.get("type");
            @SuppressWarnings("unchecked")
            Map<String, Object> data = (Map<String, Object>) request.getOrDefault("data", new HashMap<>());

            if (to == null || to.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "Recipient email is required"));
            }

            if (subject == null || subject.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "Email subject is required"));
            }

            if (type == null || type.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "Email type is required"));
            }

            // Generate email body based on type
            String body = generateEmailBody(type, data);

            // Log the email (in production, this would send actual email via SMTP)
            logEmailNotification(to, subject, body, type);

            // In a real application, integrate with email service (SendGrid, AWS SES, etc.)
            System.out.println("========================================");
            System.out.println("EMAIL NOTIFICATION");
            System.out.println("========================================");
            System.out.println("To: " + to);
            System.out.println("Subject: " + subject);
            System.out.println("Type: " + type);
            System.out.println("----------------------------------------");
            System.out.println(body);
            System.out.println("========================================");

            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "Email notification sent successfully");
            response.put("to", to);
            response.put("subject", subject);
            response.put("type", type);
            response.put("timestamp", LocalDateTime.now().toString());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(Map.of("error", "Failed to send email: " + e.getMessage()));
        }
    }

    /**
     * Send bulk email notifications
     * POST /api/notifications/email/bulk
     */
    @PostMapping("/email/bulk")
    public ResponseEntity<?> sendBulkEmail(@RequestBody Map<String, Object> request) {
        try {
            @SuppressWarnings("unchecked")
            java.util.List<String> recipients = (java.util.List<String>) request.get("recipients");
            String subject = (String) request.get("subject");
            String type = (String) request.get("type");
            @SuppressWarnings("unchecked")
            Map<String, Object> data = (Map<String, Object>) request.getOrDefault("data", new HashMap<>());

            if (recipients == null || recipients.isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "Recipients list is required"));
            }

            int successCount = 0;
            int failureCount = 0;

            for (String recipient : recipients) {
                try {
                    String body = generateEmailBody(type, data);
                    logEmailNotification(recipient, subject, body, type);
                    successCount++;
                } catch (Exception e) {
                    failureCount++;
                    System.err.println("Failed to send email to " + recipient + ": " + e.getMessage());
                }
            }

            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("total", recipients.size());
            response.put("sent", successCount);
            response.put("failed", failureCount);
            response.put("timestamp", LocalDateTime.now().toString());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(Map.of("error", "Failed to send bulk emails: " + e.getMessage()));
        }
    }

    /**
     * Get email notification history for a user
     * GET /api/notifications/email/history?userId={userId}
     */
    @GetMapping("/email/history")
    public ResponseEntity<?> getEmailHistory(@RequestParam(required = false) Integer userId) {
        try {
            String sql;
            java.util.List<Map<String, Object>> history;

            if (userId != null) {
                sql = "SELECT * FROM email_notifications WHERE recipient_email IN " +
                      "(SELECT email FROM users WHERE user_id = ?) ORDER BY sent_at DESC LIMIT 50";
                history = jdbcTemplate.queryForList(sql, userId);
            } else {
                sql = "SELECT * FROM email_notifications ORDER BY sent_at DESC LIMIT 100";
                history = jdbcTemplate.queryForList(sql);
            }

            return ResponseEntity.ok(Map.of("history", history, "count", history.size()));

        } catch (Exception e) {
            // Table might not exist yet, return empty list
            return ResponseEntity.ok(Map.of("history", java.util.Collections.emptyList(), "count", 0));
        }
    }

    /**
     * Generate email body based on type and data
     */
    private String generateEmailBody(String type, Map<String, Object> data) {
        switch (type) {
            case "event_registration":
                return generateEventRegistrationEmail(data);
            case "event_reminder":
                return generateEventReminderEmail(data);
            case "booking_confirmation":
                return generateBookingConfirmationEmail(data);
            case "approval_notification":
                return generateApprovalNotificationEmail(data);
            case "weekly_digest":
                return generateWeeklyDigestEmail(data);
            default:
                return "Email notification from Campus Event System";
        }
    }

    private String generateEventRegistrationEmail(Map<String, Object> data) {
        String eventTitle = (String) data.getOrDefault("event_title", "Event");
        String eventDate = (String) data.getOrDefault("event_date", "TBD");
        String eventTime = (String) data.getOrDefault("event_time", "TBD");
        String eventLocation = (String) data.getOrDefault("event_location", "TBD");
        String userName = (String) data.getOrDefault("user_name", "Student");

        return String.format(
            "Dear %s,\n\n" +
            "You have successfully registered for the following event:\n\n" +
            "Event: %s\n" +
            "Date: %s\n" +
            "Time: %s\n" +
            "Location: %s\n\n" +
            "We look forward to seeing you there!\n\n" +
            "If you need to cancel your registration, please log in to your account.\n\n" +
            "Best regards,\n" +
            "Campus Event System Team",
            userName, eventTitle, eventDate, eventTime, eventLocation
        );
    }

    private String generateEventReminderEmail(Map<String, Object> data) {
        String eventTitle = (String) data.getOrDefault("event_title", "Event");
        String eventDate = (String) data.getOrDefault("event_date", "Tomorrow");
        String eventTime = (String) data.getOrDefault("event_time", "TBD");
        String eventLocation = (String) data.getOrDefault("event_location", "TBD");
        String userName = (String) data.getOrDefault("user_name", "Student");

        return String.format(
            "Dear %s,\n\n" +
            "This is a reminder that you are registered for the following event:\n\n" +
            "Event: %s\n" +
            "Date: %s\n" +
            "Time: %s\n" +
            "Location: %s\n\n" +
            "Don't forget to attend! We're looking forward to seeing you.\n\n" +
            "Best regards,\n" +
            "Campus Event System Team",
            userName, eventTitle, eventDate, eventTime, eventLocation
        );
    }

    private String generateBookingConfirmationEmail(Map<String, Object> data) {
        String resourceName = (String) data.getOrDefault("resource_name", "Resource");
        String bookingDate = (String) data.getOrDefault("booking_date", "TBD");
        String bookingTime = (String) data.getOrDefault("booking_time", "TBD");
        String userName = (String) data.getOrDefault("user_name", "Student");
        String status = (String) data.getOrDefault("status", "confirmed");

        return String.format(
            "Dear %s,\n\n" +
            "Your booking has been %s:\n\n" +
            "Resource: %s\n" +
            "Date: %s\n" +
            "Time: %s\n\n" +
            "Please arrive on time. If you need to cancel, please do so at least 24 hours in advance.\n\n" +
            "Best regards,\n" +
            "Campus Event System Team",
            userName, status, resourceName, bookingDate, bookingTime
        );
    }

    private String generateApprovalNotificationEmail(Map<String, Object> data) {
        String itemType = (String) data.getOrDefault("item_type", "request");
        String itemName = (String) data.getOrDefault("item_name", "Your submission");
        String status = (String) data.getOrDefault("status", "reviewed");
        String reason = (String) data.getOrDefault("reason", "");
        String userName = (String) data.getOrDefault("user_name", "Student");

        StringBuilder body = new StringBuilder();
        body.append(String.format("Dear %s,\n\n", userName));
        body.append(String.format("Your %s '%s' has been %s.\n\n", itemType, itemName, status));
        
        if (reason != null && !reason.trim().isEmpty()) {
            body.append(String.format("Reason: %s\n\n", reason));
        }
        
        body.append("Thank you for using Campus Event System.\n\n");
        body.append("Best regards,\n");
        body.append("Campus Event System Team");

        return body.toString();
    }

    private String generateWeeklyDigestEmail(Map<String, Object> data) {
        String userName = (String) data.getOrDefault("user_name", "Student");
        @SuppressWarnings("unchecked")
        java.util.List<String> events = (java.util.List<String>) data.getOrDefault("events", java.util.Collections.emptyList());

        StringBuilder body = new StringBuilder();
        body.append(String.format("Dear %s,\n\n", userName));
        body.append("Here are the upcoming events this week:\n\n");

        if (events.isEmpty()) {
            body.append("No upcoming events this week.\n\n");
        } else {
            for (int i = 0; i < events.size(); i++) {
                body.append(String.format("%d. %s\n", i + 1, events.get(i)));
            }
            body.append("\n");
        }

        body.append("Log in to view more details and register for events.\n\n");
        body.append("Best regards,\n");
        body.append("Campus Event System Team");

        return body.toString();
    }

    /**
     * Log email notification to database (optional - requires table creation)
     */
    private void logEmailNotification(String recipient, String subject, String body, String type) {
        try {
            String sql = "INSERT INTO email_notifications (recipient_email, subject, body, type, sent_at, status) " +
                        "VALUES (?, ?, ?, ?, NOW(), 'sent')";
            jdbcTemplate.update(sql, recipient, subject, body, type);
        } catch (Exception e) {
            // Table might not exist, just log to console
            System.out.println("Note: email_notifications table not found. Email logged to console only.");
        }
    }
}
