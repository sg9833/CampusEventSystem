package com.campuscoord.dto;

import jakarta.validation.constraints.*;

public class LoginRequest {

    @NotBlank(message = "Email or Username is required")
    private String email;  // This field can contain either email or username
    
    @NotBlank(message = "Password is required")
    @Size(min = 6, message = "Password must be at least 6 characters")
    private String password;

    public LoginRequest() {}

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
}
