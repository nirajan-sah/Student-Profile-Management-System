import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
from student import get_student_profile, update_student_profile, get_student_grades, get_student_eca
from mat import create_grades_chart, create_eca_chart
from ui_components import create_button, create_label, create_entry, create_frame, create_combobox

class UserView:
    def __init__(self, user_data):
        self.root = tk.Tk()
        self.root.title("User Dashboard")
        self.root.geometry("800x600")
        self.user_data = user_data
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main container
        main_container = create_frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create header
        header_frame = create_frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        create_label(header_frame, f"Welcome, {self.user_data['username']}", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        create_button(header_frame, "Logout", self.logout).pack(side=tk.RIGHT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create profile tab
        profile_frame = create_frame(self.notebook)
        self.notebook.add(profile_frame, text="Profile")
        
        # Profile form
        form_frame = create_frame(profile_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Full Name
        name_frame = create_frame(form_frame)
        name_frame.pack(fill=tk.X, pady=5)
        create_label(name_frame, "Full Name:").pack(side=tk.LEFT)
        self.name_entry = create_entry(name_frame)
        self.name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Email
        email_frame = create_frame(form_frame)
        email_frame.pack(fill=tk.X, pady=5)
        create_label(email_frame, "Email:").pack(side=tk.LEFT)
        self.email_entry = create_entry(email_frame)
        self.email_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Phone
        phone_frame = create_frame(form_frame)
        phone_frame.pack(fill=tk.X, pady=5)
        create_label(phone_frame, "Phone:").pack(side=tk.LEFT)
        self.phone_entry = create_entry(phone_frame)
        self.phone_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Address
        address_frame = create_frame(form_frame)
        address_frame.pack(fill=tk.X, pady=5)
        create_label(address_frame, "Address:").pack(side=tk.LEFT)
        self.address_entry = create_entry(address_frame)
        self.address_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        create_button(form_frame, "Save Profile", self.save_profile).pack(pady=20)
        
        # Create view student tab
        view_frame = create_frame(self.notebook)
        self.notebook.add(view_frame, text="View Student")
        
        # Search form
        search_frame = create_frame(view_frame)
        search_frame.pack(fill=tk.X, padx=20, pady=20)
        
        create_label(search_frame, "Student ID:").pack(side=tk.LEFT)
        self.search_entry = create_entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        create_button(search_frame, "Search", self.search_student).pack(side=tk.LEFT)
        
        # Student info
        self.info_frame = create_frame(view_frame)
        self.info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def save_profile(self):
        data = {
            'full_name': self.name_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'phone': self.phone_entry.get().strip(),
            'address': self.address_entry.get().strip()
        }
        
        if not data['full_name']:
            messagebox.showerror("Error", "Full name is required")
            return
            
        success, message = update_student_profile(self.user_data['username'], data)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
            
    def search_student(self):
        student_id = self.search_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a student ID")
            return
            
        # Clear previous results
        for widget in self.info_frame.winfo_children():
            widget.destroy()
            
        # Get student profile
        profile = get_student_profile(student_id)
        if not profile:
            create_label(self.info_frame, "Student not found").pack()
            return
            
        # Display profile
        create_label(self.info_frame, f"Name: {profile.get('full_name', '')}").pack(anchor=tk.W)
        create_label(self.info_frame, f"Email: {profile.get('email', '')}").pack(anchor=tk.W)
        create_label(self.info_frame, f"Phone: {profile.get('phone', '')}").pack(anchor=tk.W)
        create_label(self.info_frame, f"Address: {profile.get('address', '')}").pack(anchor=tk.W)
        
        # Get and display grades
        grades = get_student_grades(student_id)
        if grades:
            create_label(self.info_frame, "\nGrades:", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
            for grade in grades:
                create_label(self.info_frame, f"{grade['subject']}: {grade['grade']}").pack(anchor=tk.W)
                
        # Get and display ECA
        eca = get_student_eca(student_id)
        if eca:
            create_label(self.info_frame, "\nExtracurricular Activities:", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
            for activity in eca:
                create_label(self.info_frame, f"{activity['activity']}: {activity.get('role', '')}").pack(anchor=tk.W)
                
    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            self.root.destroy()
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    from auth import login_window
    login_window()
