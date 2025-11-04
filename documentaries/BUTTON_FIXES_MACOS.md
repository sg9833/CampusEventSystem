# Button Fixes - macOS Canvas Rendering

## Summary
**Total tk.Button instances with bg parameter: 93 buttons across 12 files**

These buttons don't render properly on macOS because tk.Button ignores custom bg colors on macOS.

## Status
- ✅ **book_resource.py**: Fixed (6 buttons) - Issue 1
- ⏳ **my_bookings.py**: In progress (12 buttons) - Issue 3
- ❌ **Remaining**: 75 buttons across 10 files - Issue 4

## Files Requiring Fixes

### High Priority (User-Facing Pages)
1. **my_bookings.py** - 12 buttons ⏳
   - Refresh, View Toggle, New Booking
   - Tab navigation buttons
   - Calendar navigation (Prev, Next, Today)
   - Booking actions (View Details, Cancel, Download, Rebook)
   - Modal Close button

2. **booking_approvals.py** - 11 buttons
   - Refresh, View Toggle, Bulk Approve/Reject
   - Action buttons per booking
   - Calendar navigation
   - Modal approval/rejection buttons

3. **my_events.py** - 7 buttons
   - Refresh, Create New Event
   - Tab navigation
   - Export, Close, Send Announcement

4. **event_details_modal.py** - 5 buttons
   - Close, Register Now, Cancel Registration
   - Event Full (disabled state)

5. **notifications_page.py** - 7 buttons
   - Refresh, Mark All Read
   - Filter buttons (All, Unread, Read)
   - Mark as Read, Delete per notification

### Medium Priority (Admin/Organizer Pages)
6. **manage_resources.py** - 12 buttons
   - Refresh, Add Resource, Clear Filters
   - Action buttons (View, Edit, Bookings, Maintenance, Delete)
   - Upload Photo, Save/Cancel in modal

7. **manage_users.py** - 11 buttons
   - Refresh, Export CSV
   - User actions (Edit, Block/Unblock, Reset Password, Send Email)
   - Modal buttons

8. **event_approvals.py** - 11 buttons
   - Refresh, Bulk Approve/Reject
   - Per-event actions
   - Modal approval/rejection

9. **create_event.py** - 4 buttons
   - Save as Draft, Previous, Next, Cancel

10. **analytics_page.py** - 5 buttons
    - Refresh, Export, Apply Date Range
    - PDF, Excel export

## Solution Approach

### Step 1: Add Imports
Add to each file:
```python
from utils.canvas_button import create_primary_button, create_secondary_button, create_success_button, create_danger_button, create_warning_button
```

### Step 2: Replace Buttons
Map colors to button types:
- `#27AE60` (green) → `create_success_button`
- `#E74C3C` (red) → `create_danger_button`
- `#3498DB` (blue) → `create_primary_button`
- `#F39C12` (orange) → `create_warning_button`
- `#6B7280`, `#F3F4F6`, `#E5E7EB` (gray) → `create_secondary_button`

### Step 3: Handle Special Cases
- **Tab navigation buttons**: Need active/inactive state management
- **Calendar navigation buttons**: Small size, arrows
- **Disabled buttons**: Use `btn.config(state='disabled')`
- **Variable assignments**: `self.btn = create_...()`

## Testing Checklist
After fixing each file:
- [ ] All buttons visible on macOS
- [ ] Hover effects work
- [ ] Click events trigger correctly
- [ ] Disabled states work (if applicable)
- [ ] Text is readable
- [ ] Layout not broken

## Automation Script
Created: `tools/convert_buttons_to_canvas.py`
- Scans all page files
- Reports button counts
- Manual conversion still recommended for accuracy

## Next Steps
1. ✅ Fix my_bookings.py buttons (Issue 3)
2. Fix remaining 75 buttons systematically (Issue 4)
3. Test each page after conversion
4. Update this document with progress
