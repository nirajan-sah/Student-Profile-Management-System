import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
from student import get_student_profile, update_student_profile, get_student_grades, update_student_grades, get_student_eca, update_student_eca
from ui_components import create_button, create_label, create_entry, create_frame, create_combobox

class StudentView:
    def __init__(self, user_data):
        self.root = tk.Tk()
        self.root.title("Student Dashboard")
        self.root.geometry("800x600")
        self.user_data = user_data
        
        self.create_widgets()
        self.load_profile()
        self.load_grades()
        self.load_eca()
        
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
        
        # Department
        dept_frame = create_frame(form_frame)
        dept_frame.pack(fill=tk.X, pady=5)
        create_label(dept_frame, "Department:").pack(side=tk.LEFT)
        self.dept_entry = create_entry(dept_frame)
        self.dept_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Year of Study
        year_frame = create_frame(form_frame)
        year_frame.pack(fill=tk.X, pady=5)
        create_label(year_frame, "Year of Study:").pack(side=tk.LEFT)
        self.year_entry = create_entry(year_frame)
        self.year_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        create_button(form_frame, "Save Profile", self.save_profile).pack(pady=20)
        
        # Create grades tab
        grades_frame = create_frame(self.notebook)
        self.notebook.add(grades_frame, text="Grades")
        
        # Grades form
        grades_form = create_frame(grades_frame)
        grades_form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Subject grades
        self.grade_entries = {}
        subjects = ['Mathematics', 'Physics', 'Computer Science', 'English', 'History']
        for subject in subjects:
            subject_frame = create_frame(grades_form)
            subject_frame.pack(fill=tk.X, pady=5)
            create_label(subject_frame, f"{subject}:").pack(side=tk.LEFT)
            self.grade_entries[subject] = create_entry(subject_frame)
            self.grade_entries[subject].pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
            
        create_button(grades_form, "Save Grades", self.save_grades).pack(pady=20)
        
        # Create ECA tab
        eca_frame = create_frame(self.notebook)
        self.notebook.add(eca_frame, text="ECA")
        
        # ECA form
        eca_form = create_frame(eca_frame)
        eca_form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ECA activities
        self.eca_entries = {}
        activities = ['Football', 'Debate Club', 'Chess Club', 'Sports']
        for activity in activities:
            activity_frame = create_frame(eca_form)
            activity_frame.pack(fill=tk.X, pady=5)
            create_label(activity_frame, f"{activity}:").pack(side=tk.LEFT)
            self.eca_entries[activity] = create_entry(activity_frame)
            self.eca_entries[activity].pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
            
        create_button(eca_form, "Save ECA", self.save_eca).pack(pady=20)
        
    def load_profile(self):
        profile = get_student_profile(self.user_data['username'])
        if profile:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, profile.get('full_name', ''))
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, profile.get('email', ''))
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, profile.get('phone', ''))
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, profile.get('address', ''))
            self.dept_entry.delete(0, tk.END)
            self.dept_entry.insert(0, profile.get('department', ''))
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, profile.get('year_of_study', ''))
            
    def load_grades(self):
        grades = get_student_grades(self.user_data['username'])
        if grades:
            for grade in grades:
                subject = grade.get('subject')
                if subject in self.grade_entries:
                    self.grade_entries[subject].delete(0, tk.END)
                    self.grade_entries[subject].insert(0, grade.get('grade', ''))
                
    def load_eca(self):
        eca = get_student_eca(self.user_data['username'])
        if eca:
            for activity in eca:
                name = activity.get('activity')
                if name in self.eca_entries:
                    self.eca_entries[name].delete(0, tk.END)
                    self.eca_entries[name].insert(0, activity.get('role', ''))
                
    def save_profile(self):
        data = {
            'full_name': self.name_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'phone': self.phone_entry.get().strip(),
            'address': self.address_entry.get().strip(),
            'department': self.dept_entry.get().strip(),
            'year_of_study': self.year_entry.get().strip()
        }
        
        if not data['full_name']:
            messagebox.showerror("Error", "Full name is required")
            return
            
        success, message = update_student_profile(self.user_data['username'], data)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
            
    def save_grades(self):
        grades = {}
        for subject, entry in self.grade_entries.items():
            grade = entry.get().strip()
            if grade:
                grades[subject] = grade
                
        success, message = update_student_grades(self.user_data['username'], grades)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
            
    def save_eca(self):
        eca = {}
        for activity, entry in self.eca_entries.items():
            role = entry.get().strip()
            if role:
                eca[activity] = {'activity': activity, 'role': role, 'hours': 2}
                
        success, message = update_student_eca(self.user_data['username'], eca)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
            
    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            self.root.destroy()
            
    def run(self):
        self.root.mainloop() 