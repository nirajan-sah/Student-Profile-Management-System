import tkinter as tk
from tkinter import ttk, messagebox
from student import get_student_grades, get_student_eca, update_student_profile
from auth import get_user_details
from mat import StudentAnalytics
from PIL import Image, ImageTk
import os


class StudentView:
    def __init__(self, username, parent=None):
        self.username = username
        self.user_details = get_user_details(username)
        self.analytics = StudentAnalytics()
        
        # Create main window
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title(f"Student View - {self.user_details['full_name']}")
        self.root.geometry("800x600")  # Increased size for charts
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"800x600+{x}+{y}")
        
        self.create_widgets()
        
        if not parent:
            self.root.mainloop()
            
    def create_widgets(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Profile tab
        profile_frame = ttk.Frame(notebook, padding="10")
        notebook.add(profile_frame, text="Profile")
        self.setup_profile_tab(profile_frame)
        
        # Grades tab
        grades_frame = ttk.Frame(notebook, padding="10")
        notebook.add(grades_frame, text="Grades")
        self.setup_grades_tab(grades_frame)
        
        # ECA tab
        eca_frame = ttk.Frame(notebook, padding="10")
        notebook.add(eca_frame, text="ECA")
        self.setup_eca_tab(eca_frame)
        
        # Analytics tab
        analytics_frame = ttk.Frame(notebook, padding="10")
        notebook.add(analytics_frame, text="Analytics")
        self.setup_analytics_tab(analytics_frame)
        
        # Logout button
        logout_btn = ttk.Button(self.root, text="Logout", command=self.logout)
        logout_btn.pack(pady=10)
        
    def setup_profile_tab(self, parent):
        # Profile information
        info_frame = ttk.LabelFrame(parent, text="Profile Information", padding="10")
        info_frame.pack(fill='x', expand=True)
        
        # Create and populate fields
        fields = [
            ('Username:', self.user_details['username']),
            ('Full Name:', self.user_details['full_name']),
            ('Email:', self.user_details.get('email', 'Not set')),
            ('Phone:', self.user_details.get('phone', 'Not set')),
            ('Address:', self.user_details.get('address', 'Not set')),
            ('Department:', self.user_details.get('department', 'Not set')),
            ('Level:', self.user_details.get('level', 'Not set'))
        ]
        
        self.profile_vars = {}
        row = 0
        for label, value in fields:
            ttk.Label(info_frame, text=label).grid(row=row, column=0, sticky='w', pady=2)
            var = tk.StringVar(value=value)
            self.profile_vars[label] = var
            if label != 'Username:':  # Username is not editable
                entry = ttk.Entry(info_frame, textvariable=var)
            else:
                entry = ttk.Label(info_frame, text=value)
            entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
            row += 1
            
        # Update button
        update_btn = ttk.Button(parent, text="Update Profile", command=self.update_profile)
        update_btn.pack(pady=10)
        
    def setup_grades_tab(self, parent):
        # Create treeview for grades
        columns = ('Subject', 'Grade')
        self.grades_tree = ttk.Treeview(parent, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.grades_tree.heading(col, text=col)
            self.grades_tree.column(col, width=100)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.grades_tree.yview)
        self.grades_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.grades_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load grades
        self.load_grades()
        
    def setup_eca_tab(self, parent):
        # Create treeview for ECA
        columns = ('Activity', 'Role', 'Hours/Week', 'Description')
        self.eca_tree = ttk.Treeview(parent, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.eca_tree.heading(col, text=col)
            self.eca_tree.column(col, width=100)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.eca_tree.yview)
        self.eca_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.eca_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load ECA
        self.load_eca()
        
    def setup_analytics_tab(self, parent):
        """Setup the analytics tab with performance charts and statistics"""
        # Create left frame for statistics
        stats_frame = ttk.LabelFrame(parent, text="Performance Statistics", padding="10")
        stats_frame.pack(side='left', fill='y', padx=5)
        
        # Create statistics display
        self.stats_display = tk.Text(stats_frame, width=40, height=20, wrap=tk.WORD)
        self.stats_display.pack(fill='both', expand=True)
        
        # Create right frame for charts
        charts_frame = ttk.LabelFrame(parent, text="Performance Charts", padding="10")
        charts_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        # Create canvas for charts
        self.chart_canvas = tk.Canvas(charts_frame, width=400, height=400)
        self.chart_canvas.pack(fill='both', expand=True)
        
        # Load analytics
        self.load_analytics()
    
    def load_grades(self):
        # Clear existing items
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)
            
        # Load grades from database
        grades = get_student_grades(self.username)
        if grades:
            for grade in grades:
                self.grades_tree.insert('', 'end', values=(
                    grade['subject'],
                    grade['grade']
                ))
                
    def load_eca(self):
        # Clear existing items
        for item in self.eca_tree.get_children():
            self.eca_tree.delete(item)
            
        # Load ECA from database
        eca = get_student_eca(self.username)
        if eca:
            for activity in eca:
                self.eca_tree.insert('', 'end', values=(
                    activity['activity'],
                    activity['role'],
                    activity['hours_per_week'],
                    activity['description']
                ))
                
    def update_profile(self):
        # Collect updated data
        data = {
            'full_name': self.profile_vars['Full Name:'].get(),
            'email': self.profile_vars['Email:'].get(),
            'phone': self.profile_vars['Phone:'].get(),
            'address': self.profile_vars['Address:'].get(),
            'department': self.profile_vars['Department:'].get(),
            'level': self.profile_vars['Level:'].get()
        }
        
        # Update profile
        if update_student_profile(self.username, data):
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.user_details.update(data)
        else:
            messagebox.showerror("Error", "Failed to update profile")
            
    def load_analytics(self):
        """Load and display analytics data"""
        # Clear previous data
        self.stats_display.delete('1.0', tk.END)
        
        # Get data
        grades = get_student_grades(self.username)
        eca = get_student_eca(self.username)
        
        if not grades and not eca:
            self.stats_display.insert(tk.END, "No data available.")
            return
        
        # Calculate statistics
        gpa = self.analytics.calculate_gpa(self.username)
        grade_stats = self.analytics.get_grade_statistics(self.username)
        eca_summary = self.analytics.get_eca_summary(self.username)
        
        
        # Display statistics
        stats_text = f"""Performance Summary

GPA: {gpa if gpa else 'N/A'}

"""
        if grade_stats:
            stats_text += f"""Grade Statistics:
Mean: {grade_stats['mean']}
Median: {grade_stats['median']}
Minimum: {grade_stats['min']}
Maximum: {grade_stats['max']}
Standard Deviation: {grade_stats['std_dev']}

"""
        
        if eca_summary:
            stats_text += f"""Extracurricular Activities:
Total Activities: {eca_summary['total_activities']}
Total Hours per Week: {eca_summary['total_hours']}

"""
        
        
        self.stats_display.insert(tk.END, stats_text)
        
        # Create and display chart
        if grades and eca:
            chart_path = self.analytics.create_performance_summary(grades, eca, self.username)
        elif grades:
            chart_path = self.analytics.create_grades_chart(grades, self.username)
        elif eca:
            chart_path = self.analytics.create_eca_chart(eca, self.username)
        else:
            return
            
        self._display_chart(chart_path)
    
    def _display_chart(self, chart_path):
        """Display a chart in the canvas"""
        if not chart_path or not os.path.exists(chart_path):
            # Clear the canvas if no chart is available
            self.chart_canvas.delete("all")
            return
            
        try:
            # Load and resize the chart
            image = Image.open(chart_path)
            image = image.resize((400, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Update canvas
            self.chart_canvas.delete("all")  # Clear previous content
            self.chart_canvas.create_image(0, 0, anchor='nw', image=photo)
            self.chart_canvas.image = photo  # Keep a reference
            
        except Exception as e:
            print(f"Error displaying chart: {e}")
            self.chart_canvas.delete("all")  # Clear canvas on error
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if isinstance(self.root, tk.Toplevel):
                self.root.master.destroy()  # Close the entire application
            else:
                self.root.destroy()  # Close just this window 