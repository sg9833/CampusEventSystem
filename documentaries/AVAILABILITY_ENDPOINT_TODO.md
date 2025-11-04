# Resource Availability Endpoint - Missing Implementation

## Issue
The frontend's "Book Resource" page tries to call `GET /api/resources/{id}/availability?date=YYYY-MM-DD` to check which time slots are already booked, but this endpoint **doesn't exist in the backend**.

## Current Workaround
The frontend now gracefully handles the missing endpoint by:
- Catching the 500 error from the backend
- Showing **all time slots as available** (green)
- Printing a warning to the console
- **Not showing an error popup** to the user

## Proper Solution (TODO)
You should implement the availability endpoint in the backend:

### Backend Implementation Needed

**File**: `backend_java/backend/src/main/java/com/campuscoord/controller/ResourceController.java`

Add this endpoint:

```java
@GetMapping("/{resourceId}/availability")
public ResponseEntity<Map<String, Object>> getResourceAvailability(
    @PathVariable Long resourceId,
    @RequestParam String date
) {
    // Query bookings table for this resource on the given date
    List<Booking> bookings = bookingDao.findByResourceIdAndDate(resourceId, date);
    
    // Extract booked time slots
    List<String> bookedSlots = bookings.stream()
        .map(booking -> booking.getStartTime()) // e.g., "09:00", "14:00"
        .collect(Collectors.toList());
    
    // Optional: Add unavailable slots (e.g., maintenance, holidays)
    List<String> unavailableSlots = new ArrayList<>();
    
    Map<String, Object> availability = new HashMap<>();
    availability.put("booked_slots", bookedSlots);
    availability.put("unavailable_slots", unavailableSlots);
    
    return ResponseEntity.ok(availability);
}
```

### Database Query Needed

**File**: `backend_java/backend/src/main/java/com/campuscoord/dao/BookingDao.java`

Add this method:

```java
@Query("SELECT b FROM Booking b WHERE b.resourceId = :resourceId AND b.bookingDate = :date")
List<Booking> findByResourceIdAndDate(@Param("resourceId") Long resourceId, @Param("date") String date);
```

## Testing After Implementation

1. Login as organizer
2. Browse Resources → Click "Book Now" on projector
3. Click "Check Availability"
4. Verify:
   - ✅ Time slots show correct colors (green = available, red = booked)
   - ✅ Cannot select booked slots
   - ✅ Can select available slots

## Current Behavior

**With this workaround**:
- ✅ No error popup shown
- ✅ All time slots appear as available (green)
- ✅ Users can select any time slot
- ⚠️ **Warning**: Users might double-book a resource if slots are actually booked

**After implementing the backend endpoint**:
- ✅ Real-time availability checking
- ✅ Prevents double bookings
- ✅ Shows accurate slot availability
