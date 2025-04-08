import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from admin import add_user, delete_user, modify_student_data, get_all_students, get_student_details
from ui_components import create_button, create_label, create_entry, create_frame, create_combobox

class AdminView:
    def __init__(self, user_data):
        self.root = tk.Tk()
        self.root.title("Admin Dashboard")
        self.root.geometry("1200x800")
        self.user_data = user_data
        
        self.create_widgets()
        self.load_students()
        
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
        
        # Create student management tab
        student_frame = create_frame(self.notebook)
        self.notebook.add(student_frame, text="Student Management")
        
        # Create student list
        list_frame = create_frame(student_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create treeview
        columns = ('username', 'full_name', 'email', 'department', 'year_of_study')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        self.tree.heading('username', text='Username')
        self.tree.heading('full_name', text='Full Name')
        self.tree.heading('email', text='Email')
        self.tree.heading('department', text='Department')
        self.tree.heading('year_of_study', text='Year')
        
        # Set column widths
        self.tree.column('username', width=100)
        self.tree.column('full_name', width=150)
        self.tree.column('email', width=200)
        self.tree.column('department', width=100)
        self.tree.column('year_of_study', width=50)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create buttons frame
        button_frame = create_frame(student_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        create_button(button_frame, "Add Student", self.show_add_student).pack(side=tk.LEFT, padx=5)
        create_button(button_frame, "Edit Student", self.show_edit_student).pack(side=tk.LEFT, padx=5)
        create_button(button_frame, "Delete Student", self.delete_student).pack(side=tk.LEFT, padx=5)
        create_button(button_frame, "View Details", self.view_student_details).pack(side=tk.LEFT, padx=5)
        
        # Create analytics tab
        analytics_frame = create_frame(self.notebook)
        self.notebook.add(analytics_frame, text="Analytics")
        
        # Create visualization frames
        viz_frame = create_frame(analytics_frame)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Department distribution
        dept_frame = create_frame(viz_frame)
        dept_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        create_label(dept_frame, "Department Distribution", font=('Arial', 12, 'bold')).pack()
        self.dept_canvas = self.create_department_chart(dept_frame)
        self.dept_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Year distribution
        year_frame = create_frame(viz_frame)
        year_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        create_label(year_frame, "Year of Study Distribution", font=('Arial', 12, 'bold')).pack()
        self.year_canvas = self.create_year_chart(year_frame)
        self.year_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Grade distribution
        grade_frame = create_frame(viz_frame)
        grade_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        create_label(grade_frame, "Grade Distribution", font=('Arial', 12, 'bold')).pack()
        self.grade_canvas = self.create_grade_chart(grade_frame)
        self.grade_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # ECA participation
        eca_frame = create_frame(viz_frame)
        eca_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        create_label(eca_frame, "ECA Participation", font=('Arial', 12, 'bold')).pack()
        self.eca_canvas = self.create_eca_chart(eca_frame)
        self.eca_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_department_chart(self, parent):
        fig, ax = plt.subplots(figsize=(8, 4))
        students = get_all_students()
        df = pd.DataFrame(students)
        if not df.empty:
            dept_counts = df['department'].value_counts()
            dept_counts.plot(kind='bar', ax=ax)
            ax.set_title('Student Distribution by Department')
            ax.set_xlabel('Department')
            ax.set_ylabel('Number of Students')
            plt.xticks(rotation=45)
            plt.tight_layout()
        return FigureCanvasTkAgg(fig, parent)
        
    def create_year_chart(self, parent):
        fig, ax = plt.subplots(figsize=(8, 4))
        students = get_all_students()
        df = pd.DataFrame(students)
        if not df.empty:
            year_counts = df['year_of_study'].value_counts().sort_index()
            year_counts.plot(kind='bar', ax=ax)
            ax.set_title('Student Distribution by Year')
            ax.set_xlabel('Year of Study')
            ax.set_ylabel('Number of Students')
            plt.tight_layout()
        return FigureCanvasTkAgg(fig, parent)
        
    def create_grade_chart(self, parent):
        fig, ax = plt.subplots(figsize=(8, 4))
        students = get_all_students()
        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        
        for student in students:
            grades = student.get('grades', [])
            for grade in grades:
                grade_value = grade.get('grade', '')
                if isinstance(grade_value, (int, float)):
                    if grade_value >= 90:
                        grade_counts['A'] += 1
                    elif grade_value >= 80:
                        grade_counts['B'] += 1
                    elif grade_value >= 70:
                        grade_counts['C'] += 1
                    elif grade_value >= 60:
                        grade_counts['D'] += 1
                    else:
                        grade_counts['F'] += 1
                elif grade_value in grade_counts:
                    grade_counts[grade_value] += 1
                    
        plt.bar(grade_counts.keys(), grade_counts.values())
        ax.set_title('Grade Distribution')
        ax.set_xlabel('Grade')
        ax.set_ylabel('Number of Students')
        plt.tight_layout()
        return FigureCanvasTkAgg(fig, parent)
        
    def create_eca_chart(self, parent):
        fig, ax = plt.subplots(figsize=(8, 4))
        students = get_all_students()
        eca_counts = {}
        
        for student in students:
            eca = student.get('eca', [])
            for activity in eca:
                activity_name = activity.get('activity', '')
                if activity_name:
                    eca_counts[activity_name] = eca_counts.get(activity_name, 0) + 1
                    
        if eca_counts:
            plt.bar(eca_counts.keys(), eca_counts.values())
            ax.set_title('ECA Participation')
            ax.set_xlabel('Activity')
            ax.set_ylabel('Number of Students')
            plt.xticks(rotation=45)
            plt.tight_layout()
        return FigureCanvasTkAgg(fig, parent)
        
    def update_visualizations(self):
        # Update all charts
        self.dept_canvas = self.create_department_chart(self.dept_canvas.get_tk_widget().master)
        self.year_canvas = self.create_year_chart(self.year_canvas.get_tk_widget().master)
        self.grade_canvas = self.create_grade_chart(self.grade_canvas.get_tk_widget().master)
        self.eca_canvas = self.create_eca_chart(self.eca_canvas.get_tk_widget().master)
        
    def load_students(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load students
        students = get_all_students()
        for student in students:
            self.tree.insert('', tk.END, values=(
                student.get('username', ''),
                student.get('full_name', ''),
                student.get('email', ''),
                student.get('department', ''),
                student.get('year_of_study', '')
            ))
            
        # Update visualizations
        self.update_visualizations()
        
    def show_add_student(self):
        # Create add student window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("400x500")
        
        # Create form
        form_frame = create_frame(add_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Username
        username_frame = create_frame(form_frame)
        username_frame.pack(fill=tk.X, pady=5)
        create_label(username_frame, "Username:").pack(side=tk.LEFT)
        username_entry = create_entry(username_frame)
        username_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Full Name
        name_frame = create_frame(form_frame)
        name_frame.pack(fill=tk.X, pady=5)
        create_label(name_frame, "Full Name:").pack(side=tk.LEFT)
        name_entry = create_entry(name_frame)
        name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Email
        email_frame = create_frame(form_frame)
        email_frame.pack(fill=tk.X, pady=5)
        create_label(email_frame, "Email:").pack(side=tk.LEFT)
        email_entry = create_entry(email_frame)
        email_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Phone
        phone_frame = create_frame(form_frame)
        phone_frame.pack(fill=tk.X, pady=5)
        create_label(phone_frame, "Phone:").pack(side=tk.LEFT)
        phone_entry = create_entry(phone_frame)
        phone_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Address
        address_frame = create_frame(form_frame)
        address_frame.pack(fill=tk.X, pady=5)
        create_label(address_frame, "Address:").pack(side=tk.LEFT)
        address_entry = create_entry(address_frame)
        address_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Department
        dept_frame = create_frame(form_frame)
        dept_frame.pack(fill=tk.X, pady=5)
        create_label(dept_frame, "Department:").pack(side=tk.LEFT)
        dept_entry = create_entry(dept_frame)
        dept_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Year of Study
        year_frame = create_frame(form_frame)
        year_frame.pack(fill=tk.X, pady=5)
        create_label(year_frame, "Year of Study:").pack(side=tk.LEFT)
        year_entry = create_entry(year_frame)
        year_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Password
        password_frame = create_frame(form_frame)
        password_frame.pack(fill=tk.X, pady=5)
        create_label(password_frame, "Password:").pack(side=tk.LEFT)
        password_entry = create_entry(password_frame, show="*")
        password_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        def add_student():
            username = username_entry.get().strip()
            full_name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_entry.get().strip()
            department = dept_entry.get().strip()
            year = year_entry.get().strip()
            password = password_entry.get().strip()
            
            if not all([username, full_name, password]):
                messagebox.showerror("Error", "Username, full name and password are required")
                return
                
            success, message = add_user(username, full_name, password, 'student')
            if success:
                # Update additional profile information
                data = {
                    'email': email,
                    'phone': phone,
                    'address': address,
                    'department': department,
                    'year_of_study': year
                }
                modify_student_data(username, data)
                messagebox.showinfo("Success", message)
                add_window.destroy()
                self.load_students()
            else:
                messagebox.showerror("Error", message)
                
        create_button(form_frame, "Add Student", add_student).pack(pady=20)
        
    def show_edit_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
            
        username = self.tree.item(selected[0])['values'][0]
        student = get_student_details(username)
        
        if not student:
            messagebox.showerror("Error", "Student not found")
            return
            
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Student")
        edit_window.geometry("400x500")
        
        # Create form
        form_frame = create_frame(edit_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Full Name
        name_frame = create_frame(form_frame)
        name_frame.pack(fill=tk.X, pady=5)
        create_label(name_frame, "Full Name:").pack(side=tk.LEFT)
        name_entry = create_entry(name_frame)
        name_entry.insert(0, student.get('full_name', ''))
        name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Email
        email_frame = create_frame(form_frame)
        email_frame.pack(fill=tk.X, pady=5)
        create_label(email_frame, "Email:").pack(side=tk.LEFT)
        email_entry = create_entry(email_frame)
        email_entry.insert(0, student.get('email', ''))
        email_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Phone
        phone_frame = create_frame(form_frame)
        phone_frame.pack(fill=tk.X, pady=5)
        create_label(phone_frame, "Phone:").pack(side=tk.LEFT)
        phone_entry = create_entry(phone_frame)
        phone_entry.insert(0, student.get('phone', ''))
        phone_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Address
        address_frame = create_frame(form_frame)
        address_frame.pack(fill=tk.X, pady=5)
        create_label(address_frame, "Address:").pack(side=tk.LEFT)
        address_entry = create_entry(address_frame)
        address_entry.insert(0, student.get('address', ''))
        address_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Department
        dept_frame = create_frame(form_frame)
        dept_frame.pack(fill=tk.X, pady=5)
        create_label(dept_frame, "Department:").pack(side=tk.LEFT)
        dept_entry = create_entry(dept_frame)
        dept_entry.insert(0, student.get('department', ''))
        dept_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Year of Study
        year_frame = create_frame(form_frame)
        year_frame.pack(fill=tk.X, pady=5)
        create_label(year_frame, "Year of Study:").pack(side=tk.LEFT)
        year_entry = create_entry(year_frame)
        year_entry.insert(0, student.get('year_of_study', ''))
        year_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Password
        password_frame = create_frame(form_frame)
        password_frame.pack(fill=tk.X, pady=5)
        create_label(password_frame, "New Password (leave blank to keep current):").pack(side=tk.LEFT)
        password_entry = create_entry(password_frame, show="*")
        password_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        def save_changes():
            data = {
                'full_name': name_entry.get().strip(),
                'email': email_entry.get().strip(),
                'phone': phone_entry.get().strip(),
                'address': address_entry.get().strip(),
                'department': dept_entry.get().strip(),
                'year_of_study': year_entry.get().strip()
            }
            
            password = password_entry.get().strip()
            if password:
                data['password'] = password
                
            success, message = modify_student_data(username, data)
            if success:
                messagebox.showinfo("Success", message)
                edit_window.destroy()
                self.load_students()
            else:
                messagebox.showerror("Error", message)
                
        create_button(form_frame, "Save Changes", save_changes).pack(pady=20)
        
    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
            
        username = self.tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {username}?"):
            success, message = delete_user(username)
            if success:
                messagebox.showinfo("Success", message)
                self.load_students()
            else:
                messagebox.showerror("Error", message)
                
    def view_student_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to view details")
            return
            
        username = self.tree.item(selected[0])['values'][0]
        student = get_student_details(username)
        
        if not student:
            messagebox.showerror("Error", "Student not found")
            return
            
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Student Details - {username}")
        details_window.geometry("600x400")
        
        # Create details view
        details_frame = create_frame(details_window)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(details_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Profile tab
        profile_frame = create_frame(notebook)
        notebook.add(profile_frame, text="Profile")
        
        # Profile details
        details = [
            ("Username", student.get('username', '')),
            ("Full Name", student.get('full_name', '')),
            ("Email", student.get('email', '')),
            ("Phone", student.get('phone', '')),
            ("Address", student.get('address', '')),
            ("Department", student.get('department', '')),
            ("Year of Study", student.get('year_of_study', '')),
            ("Enrollment Date", student.get('enrollment_date', ''))
        ]
        
        for label, value in details:
            row_frame = create_frame(profile_frame)
            row_frame.pack(fill=tk.X, pady=5)
            create_label(row_frame, f"{label}:").pack(side=tk.LEFT)
            create_label(row_frame, value).pack(side=tk.RIGHT)
            
        # Grades tab
        grades_frame = create_frame(notebook)
        notebook.add(grades_frame, text="Grades")
        
        # Create grades treeview
        columns = ('subject', 'grade', 'credits', 'semester', 'year')
        grades_tree = ttk.Treeview(grades_frame, columns=columns, show='headings')
        
        # Set column headings
        grades_tree.heading('subject', text='Subject')
        grades_tree.heading('grade', text='Grade')
        grades_tree.heading('credits', text='Credits')
        grades_tree.heading('semester', text='Semester')
        grades_tree.heading('year', text='Year')
        
        # Set column widths
        grades_tree.column('subject', width=150)
        grades_tree.column('grade', width=50)
        grades_tree.column('credits', width=50)
        grades_tree.column('semester', width=100)
        grades_tree.column('year', width=50)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(grades_frame, orient=tk.VERTICAL, command=grades_tree.yview)
        grades_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        grades_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load grades
        grades = student.get('grades', [])
        for grade in grades:
            grades_tree.insert('', tk.END, values=(
                grade.get('subject', ''),
                grade.get('grade', ''),
                grade.get('credits', ''),
                grade.get('semester', ''),
                grade.get('year', '')
            ))
            
        # ECA tab
        eca_frame = create_frame(notebook)
        notebook.add(eca_frame, text="ECA")
        
        # Create ECA treeview
        columns = ('activity', 'role', 'hours', 'start_date', 'end_date')
        eca_tree = ttk.Treeview(eca_frame, columns=columns, show='headings')
        
        # Set column headings
        eca_tree.heading('activity', text='Activity')
        eca_tree.heading('role', text='Role')
        eca_tree.heading('hours', text='Hours/Week')
        eca_tree.heading('start_date', text='Start Date')
        eca_tree.heading('end_date', text='End Date')
        
        # Set column widths
        eca_tree.column('activity', width=150)
        eca_tree.column('role', width=100)
        eca_tree.column('hours', width=100)
        eca_tree.column('start_date', width=100)
        eca_tree.column('end_date', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(eca_frame, orient=tk.VERTICAL, command=eca_tree.yview)
        eca_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        eca_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load ECA
        eca = student.get('eca', [])
        for activity in eca:
            eca_tree.insert('', tk.END, values=(
                activity.get('activity', ''),
                activity.get('role', ''),
                activity.get('hours', ''),
                activity.get('start_date', ''),
                activity.get('end_date', '')
            ))
            
    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            self.root.destroy()
            
    def run(self):
        self.root.mainloop() 