# Input Validation Quick Reference Guide

## For Backend Developers

### Adding Validation to a New DTO

**Step 1**: Import validation annotations
```java
import jakarta.validation.constraints.*;
```

**Step 2**: Add annotations to fields
```java
public class MyRequest {
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be 2-100 characters")
    private String name;
    
    @Email(message = "Invalid email format")
    private String email;
    
    @Positive(message = "ID must be positive")
    private Integer id;
}
```

**Step 3**: Use @Valid in controller
```java
@PostMapping
public ResponseEntity<?> create(@Valid @RequestBody MyRequest request) {
    // If we reach here, request is valid!
    // Process the validated data
}
```

That's it! No manual validation code needed.

---

## Common Validation Annotations

### String Validation

```java
@NotNull                    // Cannot be null
@NotBlank                   // Cannot be null, empty, or whitespace
@NotEmpty                   // Cannot be null or empty

@Size(min = 3, max = 100)   // Length constraints
@Email                      // Valid email format
@Pattern(regexp = "...")    // Regex pattern matching
```

### Number Validation

```java
@NotNull                    // Cannot be null
@Positive                   // Must be > 0
@PositiveOrZero            // Must be >= 0
@Negative                   // Must be < 0
@NegativeOrZero            // Must be <= 0
@Min(5)                     // Minimum value
@Max(100)                   // Maximum value
```

### Date/Time Validation

```java
@NotNull                    // Cannot be null
@Future                     // Must be in the future
@FutureOrPresent           // Must be now or in the future
@Past                       // Must be in the past
@PastOrPresent             // Must be now or in the past
```

### Custom Validation

```java
@AssertTrue(message = "Custom error message")
public boolean isValid() {
    // Return true if valid, false if invalid
    return this.fieldA != null && this.fieldB > 0;
}
```

---

## Real Examples from Campus Event System

### 1. Registration Validation

```java
public class RegisterRequest {
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100)
    private String name;
    
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;
    
    @NotBlank(message = "Password is required")
    @Size(min = 6, max = 128)
    @Pattern(
        regexp = "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d@$!%*#?&]{6,}$",
        message = "Password must contain at least one letter and one number"
    )
    private String password;
    
    @Pattern(regexp = "^(student|organizer|admin)$")
    private String role;
}
```

**Usage**:
```java
@PostMapping("/register")
public ResponseEntity<?> register(@Valid @RequestBody RegisterRequest request) {
    // request is validated automatically
    String name = request.getName();
    // ...
}
```

---

### 2. Event Creation Validation

```java
public class CreateEventRequest {
    @NotBlank(message = "Title is required")
    @Size(min = 3, max = 255)
    private String title;
    
    @NotBlank(message = "Description is required")
    @Size(min = 10, max = 5000)
    private String description;
    
    @NotNull(message = "Organizer ID is required")
    @Positive
    private Integer organizerId;
    
    @NotNull(message = "Start time is required")
    private LocalDateTime startTime;
    
    @NotNull(message = "End time is required")
    private LocalDateTime endTime;
    
    @NotBlank(message = "Venue is required")
    @Size(max = 255)
    private String venue;
    
    // Custom validation: end must be after start
    @AssertTrue(message = "End time must be after start time")
    public boolean isEndTimeAfterStartTime() {
        if (startTime == null || endTime == null) {
            return true;
        }
        return endTime.isAfter(startTime);
    }
}
```

---

### 3. Booking Validation

```java
public class BookingRequest {
    @Positive
    private Integer eventId; // optional
    
    @NotNull(message = "User ID is required")
    @Positive
    private Integer userId;
    
    @NotNull(message = "Resource ID is required")
    @Positive
    private Integer resourceId;
    
    @NotBlank(message = "Start time is required")
    @Pattern(regexp = "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.*$")
    private String startTime;
    
    @NotBlank(message = "End time is required")
    @Pattern(regexp = "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.*$")
    private String endTime;
}
```

---

## Testing Validation

### Test Invalid Input

```bash
# Test missing required field
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!"}'
  
# Response:
{
  "status": "error",
  "message": "Validation failed",
  "errors": {
    "name": "Name is required"
  }
}
```

### Test Invalid Format

```bash
# Test invalid email
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"notanemail","password":"Test123!"}'
  
# Response:
{
  "status": "error",
  "message": "Validation failed",
  "errors": {
    "email": "Email must be a valid email address"
  }
}
```

### Test Valid Input

```bash
# Test valid registration
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","password":"Test123!","role":"student"}'
  
# Response:
{
  "id": 1,
  "name": "Test User",
  "email": "test@test.com",
  "role": "student",
  "token": "eyJhbGciOiJIUzUxMiJ9..."
}
```

---

## Error Response Format

### Validation Error

All validation errors follow this format:

```json
{
  "status": "error",
  "message": "Validation failed",
  "timestamp": "2025-10-11T10:13:02.152790",
  "errors": {
    "fieldName1": "Error message for field 1",
    "fieldName2": "Error message for field 2"
  }
}
```

**HTTP Status**: 400 Bad Request

---

## Frontend Integration

### Handling Validation Errors in Python

```python
def create_event(data):
    try:
        response = api.post('events', data)
        return response
    except requests.HTTPError as e:
        if e.response.status_code == 400:
            error_data = e.response.json()
            
            if error_data.get('status') == 'error':
                # Multiple field errors
                errors = error_data.get('errors', {})
                for field, message in errors.items():
                    print(f"Validation error in {field}: {message}")
            else:
                # Generic error
                print(error_data.get('message', 'Unknown error'))
```

### Handling Validation Errors in JavaScript

```javascript
try {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
  if (response.status === 400) {
    const error = await response.json();
    
    if (error.status === 'error' && error.errors) {
      // Show field-specific errors
      Object.entries(error.errors).forEach(([field, message]) => {
        showFieldError(field, message);
      });
    }
  }
} catch (error) {
  console.error('Request failed:', error);
}
```

---

## Best Practices

### ✅ DO

1. **Use specific annotations**: Choose the right annotation for each field
2. **Provide clear messages**: Help users understand what's wrong
3. **Validate at DTO level**: Keep validation in one place
4. **Test edge cases**: Verify validation works for all scenarios
5. **Use custom validators**: For complex business rules

### ❌ DON'T

1. **Don't skip validation**: Always use @Valid
2. **Don't validate in controllers**: Keep controllers thin
3. **Don't use generic messages**: Be specific about what's wrong
4. **Don't duplicate validation**: Define rules once in DTO
5. **Don't catch validation exceptions**: Let the handler deal with them

---

## Common Patterns

### Pattern 1: Required Field with Length

```java
@NotBlank(message = "Field is required")
@Size(min = 3, max = 100, message = "Must be 3-100 characters")
private String field;
```

### Pattern 2: Optional Field with Validation

```java
@Size(max = 255, message = "Must not exceed 255 characters")
private String optionalField;  // Can be null, but if present, must be <= 255
```

### Pattern 3: Email Field

```java
@NotBlank(message = "Email is required")
@Email(message = "Invalid email format")
@Size(max = 255)
private String email;
```

### Pattern 4: Positive ID

```java
@NotNull(message = "ID is required")
@Positive(message = "ID must be positive")
private Integer id;
```

### Pattern 5: Date Range Validation

```java
@NotNull
private LocalDateTime startDate;

@NotNull
private LocalDateTime endDate;

@AssertTrue(message = "End date must be after start date")
public boolean isValidDateRange() {
    if (startDate == null || endDate == null) return true;
    return endDate.isAfter(startDate);
}
```

### Pattern 6: Password Strength

```java
@NotBlank(message = "Password is required")
@Size(min = 8, message = "Password must be at least 8 characters")
@Pattern(
    regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$",
    message = "Password must contain uppercase, lowercase, number, and special character"
)
private String password;
```

---

## Troubleshooting

### Problem: Validation not working

**Cause**: Missing @Valid annotation

**Solution**:
```java
// Wrong
public ResponseEntity<?> create(@RequestBody MyRequest request) { ... }

// Correct
public ResponseEntity<?> create(@Valid @RequestBody MyRequest request) { ... }
```

---

### Problem: Getting 500 error instead of 400

**Cause**: ValidationExceptionHandler not registered

**Solution**: Ensure ValidationExceptionHandler has @RestControllerAdvice annotation

---

### Problem: Custom validation not working

**Cause**: Method must be public and return boolean

**Solution**:
```java
// Wrong
private boolean isValid() { ... }

// Correct
@AssertTrue(message = "Validation failed")
public boolean isValid() { ... }
```

---

## Performance Considerations

### Validation is Fast
- Validation happens in memory
- No database queries
- Typical validation: <1ms per request
- Fail fast: Invalid requests rejected immediately

### Optimization Tips
- Use simple validators when possible
- Avoid complex regex patterns for large inputs
- Don't validate fields that will be validated elsewhere
- Cache compiled regex patterns (Java does this automatically)

---

## Summary

### What You Get
✅ Automatic validation with annotations  
✅ Clear, consistent error messages  
✅ No manual validation code  
✅ Protection against invalid input  
✅ Easy to test and maintain  

### What You Need to Do
1. Add validation annotations to DTO fields
2. Add @Valid to controller parameters
3. Handle validation errors in frontend

**That's it! Validation is now automatic.**

---

## Quick Reference Card

| Need | Annotation | Example |
|------|------------|---------|
| Required field | `@NotBlank` | `@NotBlank(message = "Required")` |
| Length limit | `@Size` | `@Size(min = 3, max = 100)` |
| Email format | `@Email` | `@Email(message = "Invalid email")` |
| Positive number | `@Positive` | `@Positive` |
| Regex pattern | `@Pattern` | `@Pattern(regexp = "...")` |
| Custom rule | `@AssertTrue` | See examples above |
| Future date | `@Future` | `@Future` |
| Min/Max value | `@Min` / `@Max` | `@Min(1)` `@Max(100)` |

---

**Remember**: Add `@Valid` in the controller, and validation happens automatically! 🎉
