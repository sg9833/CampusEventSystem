# Quick Start Guide - Campus Event System Frontend

Get up and running with the Campus Event System in 5 minutes!

## 🚀 Quick Installation

### 1. Prerequisites Check

```bash
# Check Python version (need 3.8+)
python3 --version

# Check pip
pip3 --version
```

### 2. Install Dependencies

```bash
cd frontend_tkinter
pip3 install -r requirements.txt
```

**What gets installed:**
- `requests` - API communication
- `Pillow` - Image handling
- `matplotlib` - Charts and graphs
- `tkcalendar` - Date picker widgets

### 3. Configure API

Edit `config.py`:

```python
API_BASE_URL = "http://localhost:8080/api"  # Your backend URL
```

### 4. Run the Application

```bash
python3 main.py
```

## 📱 First Use

### Default Login Credentials

**Admin Account:**
- Email: `admin@campus.edu`
- Password: `admin123`

**Student Account:**
- Email: `student@campus.edu`
- Password: `student123`

**Organizer Account:**
- Email: `organizer@campus.edu`
- Password: `org123`

### Navigation

**Students can:**
1. Browse Events (with advanced search)
2. Register for events
3. Browse Resources
4. Book resources
5. View notifications
6. Manage profile

**Organizers can (all student features +):**
1. Create events
2. Manage their events
3. View registrations
4. Send notifications

**Admins can (all features +):**
1. Approve/reject events
2. Approve/reject bookings
3. Manage all users
4. View analytics dashboard
5. Manage resources
6. System-wide controls

## 🧩 Using SearchComponent (NEW!)

The SearchComponent is a powerful reusable widget for advanced searching and filtering.

### Basic Usage

```python
from components import SearchComponent

def handle_search(search_text, filters):
    print(f"Search: {search_text}")
    print(f"Filters: {filters}")
    # Apply to your data...

config = {
    'categories': ['Type1', 'Type2', 'Type3'],
    'statuses': ['Active', 'Inactive'],
    'sort_options': ['Name', 'Date'],
    'placeholder': 'Search...'
}

search = SearchComponent(
    parent_frame,
    on_search_callback=handle_search,
    config=config
)
search.pack(fill='x', padx=20, pady=10)
```

### Where It's Used

✅ **Browse Events Page** - Search events by name, organizer, filter by category, date, status  
✅ **Browse Resources Page** - Search resources by name, location, filter by type, amenities  
🔜 **Manage Users Page** - Coming soon!

### Features

- 🔍 **Debounced Search** - Waits 500ms after typing stops
- 📅 **Date Range Filter** - Pick start and end dates
- 🏷️ **Category Filter** - Multi-select checkboxes
- ✅ **Status Filter** - Single-select radio buttons
- 🔄 **Sort Options** - Dropdown for sorting
- 🏷️ **Filter Tags** - Visual chips showing active filters
- ❌ **Remove Filters** - Click X on tags to remove
- 🗂️ **Advanced Filters Modal** - Clean modal dialog

## 📊 Key Pages

### 1. Browse Events (`browse_events.py`)

**Features:**
- Grid layout (3x3)
- SearchComponent integration
- Event cards with details
- Registration functionality
- Pagination

**Try it:**
1. Login as student
2. Click "Browse Events" in sidebar
3. Type in search box
4. Click "Advanced Filters" button
5. Select filters and apply
6. Click on event card for details

### 2. Browse Resources (`browse_resources.py`)

**Features:**
- 2-column grid
- SearchComponent + sidebar filters
- Resource cards with amenities
- Booking functionality

**Try it:**
1. Login as student
2. Click "Book Resources"
3. Use search or sidebar filters
4. Click "Book Now" on a resource

### 3. Analytics Dashboard (`analytics_page.py`)

**Features:**
- 4 overview stat cards
- 5 interactive charts (matplotlib)
- Date range selector
- Export options

**Try it:**
1. Login as admin
2. Click "Analytics" in sidebar
3. View charts and stats
4. Try export buttons

### 4. Booking Approvals (`booking_approvals.py`)

**Features:**
- Pending bookings list
- Conflict detection
- Calendar view
- Bulk operations

**Try it:**
1. Login as admin
2. Click "Booking Approvals"
3. Review pending bookings
4. Approve or reject

### 5. Notifications Center (`notifications_page.py`)

**Features:**
- Grouped by date
- 8 notification types
- Filter buttons
- Real-time updates (30s)

**Try it:**
1. Login as any user
2. Click bell icon or "Notifications"
3. Filter by All/Unread/Read
4. Mark as read or delete

## 🎨 Customization

### Colors

Edit colors in your page's `__init__`:

```python
self.colors = {
    'primary': '#2C3E50',
    'secondary': '#3498DB',
    'success': '#27AE60',
    'warning': '#F39C12',
    'danger': '#E74C3C',
    'background': '#ECF0F1'
}
```

### SearchComponent Config

```python
config = {
    'categories': ['Your', 'Categories'],
    'statuses': ['Status1', 'Status2'],
    'sort_options': ['Sort1', 'Sort2'],
    'show_date_filter': True,      # Enable date picker
    'show_category_filter': True,  # Enable categories
    'show_status_filter': True,    # Enable status
    'placeholder': 'Custom placeholder...'
}
```

## 🐛 Common Issues

### "Module not found" errors

```bash
# Reinstall dependencies
pip3 install -r requirements.txt --upgrade
```

### "Cannot connect to API" errors

1. Check backend is running
2. Verify `config.py` has correct API_BASE_URL
3. Test with: `curl http://localhost:8080/api/health`

### Tkinter not found (macOS)

```bash
# Install Python with tkinter
brew install python-tk@3.9
```

### SearchComponent not working

1. Ensure `components/__init__.py` exists
2. Check import: `from components import SearchComponent`
3. Verify callback function signature: `def callback(search_text, filters):`

## 📚 Next Steps

### For Users
1. Explore all pages
2. Try creating events (as organizer)
3. Book resources
4. Check notifications

### For Developers
1. Read full `README.md`
2. Review `search_component_examples.py`
3. Check `CHANGELOG.md` for recent changes
4. Add your own pages (see "Adding a New Page" in README)

### Learn More

- **Full Documentation**: `README.md`
- **API Reference**: See backend documentation
- **Component Examples**: `components/search_component_examples.py`
- **Recent Changes**: `CHANGELOG.md`

## 🆘 Getting Help

### Documentation
- `README.md` - Full documentation
- `CHANGELOG.md` - Recent changes and updates
- `components/search_component_examples.py` - Component usage examples

### Code Examples
- Check existing pages for patterns
- Review `utils/` for helper functions
- Look at `components/` for reusable widgets

### Troubleshooting
1. Check terminal for error messages
2. Verify all dependencies installed
3. Ensure backend is running
4. Check `config.py` settings
5. Review API endpoint responses

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Application starts without errors
- [ ] Login page appears
- [ ] Can login with test credentials
- [ ] Dashboard loads with data
- [ ] Search functionality works
- [ ] Modal dialogs open correctly
- [ ] Charts render (analytics page)
- [ ] Notifications load
- [ ] Profile page shows user data

If all checked, you're ready to go! 🎉

---

**Need more help?** See full documentation in `README.md` or contact support.

**Version**: 1.2.0  
**Last Updated**: October 2025
