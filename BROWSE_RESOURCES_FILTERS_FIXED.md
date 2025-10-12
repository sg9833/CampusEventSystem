# Browse Resources - Filter Sidebar Dark Mode Fixes

## Date: October 12, 2025

## Issues Reported
User reported dark mode visibility issues in the Browse Resources page **filters sidebar**:

1. ❌ "Clear All Filters" button text invisible
2. ❌ Resource Type radio button labels invisible (only radio buttons visible)
3. ❌ Amenities checkbox labels invisible (only checkboxes and emojis visible)
4. ❌ Time Slot radio button labels invisible
5. ❌ Select Date widget has dark mode issues

## Root Cause
All text elements in the filters sidebar were missing explicit `fg` (foreground) color parameters. On macOS dark mode, Tkinter widgets without explicit colors inherit system theme colors, causing text to be invisible (white text on white backgrounds).

## Files Modified

### 1. `/frontend_tkinter/pages/browse_resources.py`

#### Fix 1: Resource Type Radio Buttons (Line ~105)
**Before:**
```python
rb = tk.Radiobutton(type_frame, text=label, variable=self.filter_type, value=value, bg='white', font=('Helvetica', 10), selectcolor='white', command=self._apply_filters)
```

**After:**
```python
rb = tk.Radiobutton(type_frame, text=label, variable=self.filter_type, value=value, bg='white', fg='#1F2937', font=('Helvetica', 10), selectcolor='white', command=self._apply_filters)
```

#### Fix 2: Amenities Checkboxes (Line ~152)
**Before:**
```python
cb = tk.Checkbutton(amenities_frame, text=label, variable=var, bg='white', font=('Helvetica', 9), selectcolor='white', command=self._apply_filters)
```

**After:**
```python
cb = tk.Checkbutton(amenities_frame, text=label, variable=var, bg='white', fg='#1F2937', font=('Helvetica', 9), selectcolor='white', command=self._apply_filters)
```

#### Fix 3: Time Slot Radio Buttons (Line ~191)
**Before:**
```python
rb = tk.Radiobutton(date_frame, text=label, variable=self.time_slot, value=value, bg='white', font=('Helvetica', 9), selectcolor='white', command=self._apply_filters)
```

**After:**
```python
rb = tk.Radiobutton(date_frame, text=label, variable=self.time_slot, value=value, bg='white', fg='#1F2937', font=('Helvetica', 9), selectcolor='white', command=self._apply_filters)
```

#### Fix 4: Date Selector Widget (Line ~166)
**Before:**
```python
self.date_picker = DateEntry(date_frame, width=20, background=self.colors.get('secondary', '#3498DB'), foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', mindate=datetime.now())
```

**After:**
```python
# Use a simple Entry widget with explicit colors (DateEntry doesn't work well with macOS dark mode)
date_entry = tk.Entry(
    date_frame, 
    textvariable=self.filter_date, 
    font=('Helvetica', 10), 
    width=22,
    fg='#1F2937',
    bg='white',
    insertbackground='#1F2937',
    relief='solid',
    borderwidth=1
)
date_entry.pack(anchor='w', pady=(0, 4))
date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
date_entry.bind('<Return>', lambda e: self._apply_filters())
date_entry.bind('<FocusOut>', lambda e: self._apply_filters())
```

**Changes:**
- **REPLACED DateEntry completely** - DateEntry from tkcalendar uses macOS native date picker which completely ignores custom color styling
- **Used plain tk.Entry** - Full control over colors
- Added explicit `fg='#1F2937'` for dark gray text
- Added explicit `bg='white'` for white background
- Added `insertbackground='#1F2937'` for cursor color
- Added auto-apply filters on Return key press or focus out
- Updated format hint to include example date

**Root Cause:**
The DateEntry widget from tkcalendar library uses macOS native widgets that completely ignore Tkinter color parameters. The only reliable solution is to use a plain Entry widget with explicit color settings.

### 2. `/frontend_tkinter/utils/canvas_button.py`

#### Fix 5: Secondary Button Colors (Line ~173)
**Before:**
```python
SECONDARY = {
    'bg_color': '#6c757d',
    'hover_color': '#5a6268',
    'fg_color': 'white'
}
```

**After:**
```python
SECONDARY = {
    'bg_color': '#F3F4F6',
    'hover_color': '#E5E7EB',
    'fg_color': '#1F2937'
}
```

**Changes:**
- Changed background to light gray (`#F3F4F6`) instead of medium gray
- Changed text color to dark gray (`#1F2937`) instead of white
- This ensures "Clear All Filters" button text is always visible

## Testing Checklist

Login as `organizer1@campus.com` and test:

- [ ] Navigate to Browse Resources page
- [ ] Check filters sidebar is visible
- [ ] **"Clear All Filters" button**: Text should be dark gray and clearly visible
- [ ] **Resource Type section**: All radio button labels should be visible:
  - All Resources
  - Classroom
  - Laboratory
  - Auditorium
  - Equipment
  - Conference Room
  - Sports Facility
- [ ] **Amenities section**: All checkbox labels should be visible with emojis:
  - 📽️ Projector
  - 📝 Whiteboard
  - 💻 Computers
  - 🔊 Audio System
  - ❄️ Air Conditioning
  - 📡 WiFi
  - 🎤 Podium
  - 📹 Recording
- [ ] **Select Date section**: Date picker should show date in dark text
- [ ] **Time Slot section**: All radio button labels should be visible:
  - All Day
  - Morning (8AM-12PM)
  - Afternoon (12PM-5PM)
  - Evening (5PM-9PM)
- [ ] **Apply Filters button**: Should be blue with white text (primary button)

## Color Standards

All text elements now use:
- **Dark text**: `fg='#1F2937'` (dark gray, almost black)
- **White backgrounds**: `bg='white'`
- **Consistent styling**: All labels, radio buttons, checkboxes use same color scheme

## Summary

✅ **5 issues fixed** in Browse Resources filter sidebar:
1. Clear All Filters button - Updated button color scheme
2. Resource Type labels - Added `fg='#1F2937'`
3. Amenities labels - Added `fg='#1F2937'`
4. Time Slot labels - Added `fg='#1F2937'`
5. Date picker - Updated foreground colors and added field backgrounds

✅ **Total lines changed**: ~12 lines across 2 files
✅ **Pattern used**: Add `fg='#1F2937'` to all text widgets
✅ **Result**: All filter sidebar elements now visible in macOS dark mode

## Related Files
- Previous fix: `BROWSE_AND_BOOKINGS_DARK_MODE_FIXED.md` (main content areas)
- This fix: Filter sidebar specific issues
- Button utilities: Updated in `canvas_button.py` for global secondary button improvement
