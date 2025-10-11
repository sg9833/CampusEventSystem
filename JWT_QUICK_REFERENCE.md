# JWT Authentication Quick Reference

## For Backend Developers

### Testing JWT Authentication

#### 1. Register New User
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Name",
    "email": "your.email@campus.com",
    "password": "YourPassword123!",
    "role": "student"
  }'
```

#### 2. Login
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@campus.com",
    "password": "YourPassword123!"
  }'
```

Both will return a response like:
```json
{
  "id": 1,
  "name": "Your Name",
  "email": "your.email@campus.com",
  "role": "student",
  "token": "eyJhbGciOiJIUzUxMiJ9..."
}
```

#### 3. Use JWT Token in Requests
```bash
TOKEN="eyJhbGciOiJIUzUxMiJ9..."

curl -X GET http://localhost:8080/api/events \
  -H "Authorization: Bearer $TOKEN"
```

---

## For Frontend Developers

### How JWT Works in the Frontend

#### 1. Login Flow
```python
# In pages/login_page.py
response = self.api.post('auth/login', {
    'email': email,
    'password': password
})

# Extract token
token = response.get('token', '')

# Store in session
self.session.store_user(
    user_id=response['id'],
    name=response['name'],
    email=response['email'],
    role=response['role'],
    token=token,
    token_expires_in=86400  # 24 hours
)

# Set in API client
self.api.set_auth_token(token)
```

#### 2. Register Flow
```python
# In pages/register_page.py
response = self.api.post('auth/register', data)

# Extract token (registration returns JWT directly)
token = response.get('token', '')

# Store and set token (same as login)
self.session.store_user(...)
self.api.set_auth_token(token)
```

#### 3. Token Restoration on App Startup
```python
# In main.py __init__
if self.session.is_logged_in():
    token = self.session.get_token()
    if token:
        self.api.set_auth_token(token)
```

#### 4. Handling Token Expiration
```python
# API client automatically handles 401/403 errors
# In main.py, we set up a callback:
def on_auth_error(status_code):
    self.session.clear_session()
    self.navigate('login')
    messagebox.showerror("Session Expired", "Please login again.")

self.api.set_auth_error_callback(on_auth_error)
```

---

## API Client Usage

### Making Authenticated Requests

```python
# The API client automatically includes the JWT token
# in the Authorization header for all requests

# GET request
events = self.api.get('events')

# POST request
new_event = self.api.post('events', {
    'title': 'My Event',
    'description': 'Event description',
    ...
})

# PUT request
updated_event = self.api.put(f'events/{event_id}', data)

# DELETE request
self.api.delete(f'events/{event_id}')
```

### No need to manually add Authorization header!
The `APIClient._get_headers()` method automatically adds:
```python
headers['Authorization'] = f'Bearer {self.auth_token}'
```

---

## Session Manager Methods

### Token Management
```python
# Store token
session.store_user(
    user_id=1,
    name="User",
    email="user@campus.com",
    role="student",
    token="eyJhbGciOiJIUzUxMiJ9...",
    token_expires_in=86400
)

# Get token (returns None if expired)
token = session.get_token()

# Check if token is expiring soon (within 5 minutes)
if session.is_token_expiring_soon():
    # Refresh token logic
    pass

# Refresh token
session.refresh_token(new_token, expires_in=86400)

# Clear session (logout)
session.clear_session()
```

---

## Security Configuration

### Backend Endpoints Access Rules

#### Public Endpoints (No Authentication Required)
- `POST /api/auth/register`
- `POST /api/auth/login`

#### Authenticated Endpoints (Any Logged-In User)
- `GET /api/events`
- `GET /api/events/{id}`
- `GET /api/bookings`
- `POST /api/bookings`
- `PUT /api/bookings/{id}`
- `DELETE /api/bookings/{id}`

#### ORGANIZER/ADMIN Only
- `POST /api/events`
- `PUT /api/events/{id}`

#### ADMIN Only
- `DELETE /api/events/{id}`
- `GET /api/users`
- `PUT /api/users/{id}`
- `DELETE /api/users/{id}`
- `POST /api/resources`
- `PUT /api/resources/{id}`
- `DELETE /api/resources/{id}`

---

## JWT Token Structure

### Header
```json
{
  "alg": "HS512"
}
```

### Payload
```json
{
  "sub": "user@campus.com",    // Subject (user email)
  "userId": 123,                // User ID
  "role": "student",            // User role
  "iat": 1760155973,           // Issued at (Unix timestamp)
  "exp": 1760242373            // Expiration (Unix timestamp)
}
```

### Signature
- Algorithm: HMAC-SHA512
- Secret: Configured in `application.properties`

---

## Configuration Files

### Backend: `application.properties`
```properties
jwt.secret=your-secret-key-here-make-it-at-least-256-bits-long-for-security
jwt.expiration=86400000
```

### Frontend: No configuration needed
- Token storage handled by SessionManager
- Token transmission handled by APIClient
- All automatic!

---

## Troubleshooting

### Problem: Getting 403 Forbidden
**Cause:** Token not included in request or token is invalid/expired

**Solution:**
1. Check if user is logged in: `session.is_logged_in()`
2. Check if token exists: `session.get_token()`
3. Verify token is set in API client: `api.auth_token`
4. Try logging in again

### Problem: Getting 401 Unauthorized
**Cause:** Token expired or user doesn't have permission

**Solution:**
- Frontend automatically clears session and redirects to login
- User just needs to log in again

### Problem: Token Not Persisting Across App Restarts
**Cause:** Token not being restored in `main.py`

**Solution:**
- Check `main.py` initialization
- Verify token restoration code is present:
  ```python
  if self.session.is_logged_in():
      token = self.session.get_token()
      if token:
          self.api.set_auth_token(token)
  ```

---

## Best Practices

### ✅ DO
- Always use the provided `APIClient` methods for API calls
- Store tokens using `SessionManager.store_user()`
- Let the API client handle authentication headers automatically
- Handle authentication errors gracefully in UI

### ❌ DON'T
- Don't manually add Authorization headers (API client does this)
- Don't store tokens in plain text files
- Don't share JWT secrets between environments
- Don't ignore 401/403 errors

---

## Development Workflow

### 1. Start Backend
```bash
cd backend_java/backend
java -jar target/backend-0.0.1-SNAPSHOT.jar
```

### 2. Test with curl
```bash
# Register
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@campus.com","password":"Test123!","role":"student"}'

# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@campus.com","password":"Test123!"}'

# Use token
TOKEN="<token-from-login>"
curl -X GET http://localhost:8080/api/events \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Start Frontend
```bash
cd frontend_tkinter
python main.py
```

### 4. Test Frontend
- Click Register → Should automatically log in
- Login → Should receive token
- Navigate pages → Token should persist
- Restart app → Token should be restored
- Wait 24 hours → Token expires, redirects to login

---

## Summary

### Backend
✅ JWT generation on login/register  
✅ Token validation on all protected endpoints  
✅ Role-based access control  
✅ 24-hour token expiration  

### Frontend
✅ Automatic token extraction and storage  
✅ Automatic token inclusion in requests  
✅ Session persistence across restarts  
✅ Automatic logout on token expiration  

**Everything is fully automated! Developers just need to use the standard API methods.**
