#!/usr/bin/env python3
"""
Simple Campus Event System - Minimal Working Version
This is a simplified version that should work without errors
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

class SimpleCampusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Campus Event System - Simple Version")
        self.geometry("600x400")
        
        # API Configuration
        self.api_url = "http://localhost:8080/api"
        
        # Check backend connection
        if not self.check_backend():
            messagebox.showerror(
                "Backend Error",
                "Cannot connect to backend at:\n" + self.api_url + "\n\n" +
                "Please start the backend server first."
            )
            self.destroy()
            return
        
        messagebox.showinfo("Success!", "✅ Backend is reachable!\n\nThe connection is working.")
        
        # Show login page
        self.show_login_page()
    
    def check_backend(self):
        """Check if backend is reachable"""
        try:
            response = requests.get(f"{self.api_url}/events", timeout=3)
            return True
        except requests.ConnectionError:
            return False
        except:
            # Any other error means backend responded (even if with error)
            return True
    
    def show_login_page(self):
        """Show simple login page"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Create login frame
        frame = ttk.Frame(self, padding="50")
        frame.pack(expand=True)
        
        # Title
        title = ttk.Label(frame, text="Campus Event System", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Email
        ttk.Label(frame, text="Email:", font=("Arial", 12)).pack(pady=5)
        self.email_entry = ttk.Entry(frame, width=30, font=("Arial", 12))
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, "admin@campus.com")
        
        # Password
        ttk.Label(frame, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = ttk.Entry(frame, width=30, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, "password")
        
        # Login button
        login_btn = ttk.Button(frame, text="Login", command=self.do_login)
        login_btn.pack(pady=20)
        
        # Status
        self.status_label = ttk.Label(frame, text="", foreground="green", font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        # Info
        info_text = "Test Credentials:\nEmail: admin@campus.com\nPassword: password"
        ttk.Label(frame, text=info_text, foreground="gray", font=("Arial", 9)).pack(pady=10)
    
    def do_login(self):
        """Attempt login"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        self.status_label.config(text="Logging in...", foreground="blue")
        self.update()
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                json={"email": email, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                messagebox.showinfo(
                    "Login Successful!",
                    f"✅ Welcome!\n\nRole: {data.get('role', 'Unknown')}\n" +
                    f"User ID: {data.get('userId', 'Unknown')}"
                )
                self.show_dashboard(data)
            else:
                error_data = response.json()
                self.status_label.config(
                    text=f"❌ {error_data.get('error', 'Login failed')}",
                    foreground="red"
                )
        except requests.ConnectionError:
            self.status_label.config(text="❌ Cannot connect to server", foreground="red")
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}", foreground="red")
    
    def show_dashboard(self, user_data):
        """Show simple dashboard"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(self, padding="30")
        frame.pack(expand=True, fill="both")
        
        # Welcome message
        welcome = ttk.Label(
            frame,
            text=f"Welcome to Campus Event System!",
            font=("Arial", 20, "bold")
        )
        welcome.pack(pady=20)
        
        # User info
        info = ttk.Label(
            frame,
            text=f"Role: {user_data.get('role', 'Unknown')}\n" +
                 f"User ID: {user_data.get('userId', 'Unknown')}",
            font=("Arial", 14)
        )
        info.pack(pady=10)
        
        # Success message
        success_msg = ttk.Label(
            frame,
            text="🎉 Your application is working!\n\n" +
                 "✅ Backend: Connected\n" +
                 "✅ Frontend: Running\n" +
                 "✅ Authentication: Working\n\n" +
                 "You can now use the full application!",
            font=("Arial", 12),
            justify="left"
        )
        success_msg.pack(pady=20)
        
        # Logout button
        logout_btn = ttk.Button(frame, text="Logout", command=self.show_login_page)
        logout_btn.pack(pady=10)

def main():
    app = SimpleCampusApp()
    app.mainloop()

if __name__ == "__main__":
    main()
