# 🔧 BACKEND DELETE ENDPOINT - Implementation Guide

## 📋 WHAT'S NEEDED

To enable the **Delete Event** button, you need to add a DELETE endpoint to your backend.

**Frontend is READY!** ✅  
**Backend needs implementation** ⚠️

---

## 🚀 IMPLEMENTATION

### Step 1: Add to `EventController.java`

**File:** `backend_java/backend/src/main/java/com/campuscoord/controller/EventController.java`

```java
@DeleteMapping("/{id}")
@PreAuthorize("hasAnyRole('ADMIN', 'ORGANIZER')")
public ResponseEntity<?> deleteEvent(
    @PathVariable int id,
    @AuthenticationPrincipal User user
) {
    try {
        // Optional: Verify user owns this event
        Event event = eventDao.findById(id);
        
        // Check if user is the organizer or an admin
        if (event.getOrganizerId() != user.getId() && 
            !user.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"))) {
            return ResponseEntity.status(403)
                .body(Map.of("error", "You do not have permission to delete this event"));
        }
        
        // Delete the event
        eventDao.delete(id);
        
        return ResponseEntity.ok()
            .body(Map.of("message", "Event deleted successfully"));
            
    } catch (EmptyResultDataAccessException e) {
        return ResponseEntity.status(404)
            .body(Map.of("error", "Event not found"));
            
    } catch (Exception e) {
        return ResponseEntity.status(500)
            .body(Map.of("error", "Failed to delete event", "details", e.getMessage()));
    }
}
```

### Step 2: Add to `EventDao.java`

**File:** `backend_java/backend/src/main/java/com/campuscoord/dao/EventDao.java`

```java
/**
 * Delete an event by ID
 * @param id Event ID to delete
 * @return Number of rows affected
 */
public int delete(int id) {
    String sql = "DELETE FROM events WHERE id = ?";
    return jdbc.update(sql, id);
}
```

### Step 3: (Optional) Add CASCADE DELETE

If you want to also delete related data (registrations, etc.) when deleting an event:

**File:** `database_sql/schema.sql`

```sql
-- Add foreign key with CASCADE DELETE to registrations table
ALTER TABLE registrations 
DROP FOREIGN KEY IF EXISTS fk_registrations_event;

ALTER TABLE registrations 
ADD CONSTRAINT fk_registrations_event 
FOREIGN KEY (event_id) REFERENCES events(id) 
ON DELETE CASCADE;
```

---

## 🧪 TESTING THE DELETE ENDPOINT

### Test with curl:

```bash
# First, login to get JWT token
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"organizer1@campus.com","password":"test123"}' \
  | jq -r '.token')

# Test DELETE endpoint
curl -X DELETE http://localhost:8080/api/events/5 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

### Expected Response:

**Success (200):**
```json
{
  "message": "Event deleted successfully"
}
```

**Not Found (404):**
```json
{
  "error": "Event not found"
}
```

**Forbidden (403):**
```json
{
  "error": "You do not have permission to delete this event"
}
```

---

## 🔒 SECURITY CONSIDERATIONS

### 1. **Authorization Check**
```java
// Only allow:
// - Event organizer (creator)
// - System admins
if (event.getOrganizerId() != user.getId() && !user.isAdmin()) {
    return ResponseEntity.status(403).body(Map.of("error", "Not authorized"));
}
```

### 2. **Soft Delete (Optional)**

Instead of permanently deleting, mark as deleted:

```sql
-- Add deleted_at column
ALTER TABLE events ADD COLUMN deleted_at TIMESTAMP NULL;

-- Soft delete
UPDATE events SET deleted_at = NOW() WHERE id = ?;

-- Query only non-deleted events
SELECT * FROM events WHERE deleted_at IS NULL;
```

---

## 📊 COMPLETE EVENTCONTROLLER.JAVA

Here's the full controller with all CRUD operations:

```java
@RestController
@RequestMapping("/api/events")
public class EventController {

    private final EventDao eventDao;

    public EventController(EventDao eventDao) {
        this.eventDao = eventDao;
    }

    // GET /api/events - List all events
    @GetMapping
    public ResponseEntity<List<Event>> listEvents() {
        return ResponseEntity.ok(eventDao.findAll());
    }

    // GET /api/events/{id} - Get single event
    @GetMapping("/{id}")
    public ResponseEntity<?> getEvent(@PathVariable int id) {
        try {
            Event event = eventDao.findById(id);
            return ResponseEntity.ok(event);
        } catch (EmptyResultDataAccessException e) {
            return ResponseEntity.status(404)
                .body(Map.of("error", "Event not found"));
        }
    }

    // POST /api/events - Create event
    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'ORGANIZER')")
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
            Map<String, Object> resp = new HashMap<>();
            resp.put("id", id);
            resp.put("message", "Event created successfully");
            return ResponseEntity.ok(resp);
        } catch (Exception ex) {
            return ResponseEntity.status(500)
                .body(Map.of("error", "Failed to create event", "message", ex.getMessage()));
        }
    }

    // PUT /api/events/{id} - Update event (FUTURE)
    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'ORGANIZER')")
    public ResponseEntity<?> updateEvent(
        @PathVariable int id,
        @Valid @RequestBody CreateEventRequest request,
        @AuthenticationPrincipal User user
    ) {
        try {
            Event existing = eventDao.findById(id);
            
            // Check permission
            if (existing.getOrganizerId() != user.getId() && !user.isAdmin()) {
                return ResponseEntity.status(403)
                    .body(Map.of("error", "Not authorized"));
            }
            
            Event event = new Event(
                id,
                request.getTitle(),
                request.getDescription(),
                request.getOrganizerId(),
                request.getStartTime(),
                request.getEndTime(),
                request.getVenue(),
                existing.getCreatedAt()
            );
            
            eventDao.update(event);
            return ResponseEntity.ok(Map.of("message", "Event updated successfully"));
            
        } catch (EmptyResultDataAccessException e) {
            return ResponseEntity.status(404)
                .body(Map.of("error", "Event not found"));
        }
    }

    // DELETE /api/events/{id} - Delete event
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'ORGANIZER')")
    public ResponseEntity<?> deleteEvent(
        @PathVariable int id,
        @AuthenticationPrincipal User user
    ) {
        try {
            Event event = eventDao.findById(id);
            
            // Check permission
            if (event.getOrganizerId() != user.getId() && !user.isAdmin()) {
                return ResponseEntity.status(403)
                    .body(Map.of("error", "Not authorized"));
            }
            
            eventDao.delete(id);
            return ResponseEntity.ok(Map.of("message", "Event deleted successfully"));
            
        } catch (EmptyResultDataAccessException e) {
            return ResponseEntity.status(404)
                .body(Map.of("error", "Event not found"));
                
        } catch (Exception e) {
            return ResponseEntity.status(500)
                .body(Map.of("error", "Failed to delete event", "details", e.getMessage()));
        }
    }
}
```

---

## 🎯 WHAT HAPPENS WITHOUT BACKEND

If you click **Delete** button without implementing the backend:

```
┌─────────────────────────────────────┐
│    Feature Not Available            │
├─────────────────────────────────────┤
│ Delete functionality is not yet     │
│ implemented in the backend.         │
│                                     │
│ To enable this feature, add the     │
│ following to EventController.java:  │
│                                     │
│ @DeleteMapping("/{id}")             │
│ public ResponseEntity<?> ...        │
│                                     │
│            [ OK ]                   │
└─────────────────────────────────────┘
```

**The frontend gracefully handles it!** ✅

---

## 📋 CHECKLIST

To fully enable Delete functionality:

- [ ] Add `@DeleteMapping("/{id}")` to `EventController.java`
- [ ] Add `delete(int id)` method to `EventDao.java`
- [ ] (Optional) Add CASCADE DELETE to database schema
- [ ] Test with curl or Postman
- [ ] Restart backend: `./run.sh` or `mvn spring-boot:run`
- [ ] Test in frontend by clicking 🗑️ Delete button

---

## ✅ SUMMARY

| Component | Status | Notes |
|-----------|--------|-------|
| Frontend UI | ✅ DONE | Delete button with confirmation |
| API Client | ✅ DONE | Has `delete()` method |
| Error Handling | ✅ DONE | Handles all error cases |
| Backend Endpoint | ⚠️ TODO | Need to implement |
| Database DAO | ⚠️ TODO | Need to implement |

**Frontend is 100% ready!** Just add backend endpoint and it will work! 🚀

---

**Last Updated:** October 12, 2025  
**Status:** Frontend complete, backend pending  
**Priority:** Medium (nice to have feature)

