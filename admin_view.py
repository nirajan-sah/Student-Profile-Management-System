import tkinter as tk
from tkinter import ttk, messagebox
from admin import add_user, remove_user, list_all_users, get_user_details
from student import add_student_grade, add_student_eca, get_student_grades, get_student_eca
from mat import StudentAnalytics
from PIL import Image, ImageTk
import os

class AdminView:
    """
    Admin View - Main interface for administrators to manage the system.
    This class creates a window with multiple tabs for different administrative tasks.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the Admin View window.
        Args:
            parent: The parent window (if any)
        """
        # Create the main window
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title("Admin Dashboard")
        self.root.geometry("1000x800")
        
        # Initialize analytics
        self.analytics = StudentAnalytics()
        
        # Center the window on screen
        self._center_window()
        
        # Create all the UI elements
        self._create_interface()
        
        # Start the main loop if this is the main window
        if not parent:
            self.root.mainloop()
    
    def _center_window(self):
        """Center the window on the screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1000x800+{x}+{y}")
    
    def _create_interface(self):
        """Create the main interface with all tabs"""
        # Create the tab container
        tab_container = ttk.Notebook(self.root)
        tab_container.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create each tab
        self._create_users_tab(tab_container)
        self._create_add_user_tab(tab_container)
        self._create_add_grade_tab(tab_container)
        self._create_add_eca_tab(tab_container)
        self._create_student_stats_tab(tab_container)
        self._create_overall_stats_tab(tab_container)
        
        # Add logout button
        logout_btn = ttk.Button(self.root, text="Logout", command=self._handle_logout)
        logout_btn.pack(pady=10)
    
    def _create_users_tab(self, parent):
        """Create the Users Management tab"""
        # Create the tab frame
        tab = ttk.Frame(parent, padding="10")
        parent.add(tab, text="Users")
        
        # Create the users list
        self._create_users_list(tab)
        
        # Create action buttons
        self._create_user_actions(tab)
    
    def _create_users_list(self, parent):
        """Create the list of users"""
        # Define columns
        columns = ('Username', 'Full Name', 'Role', 'Email', 'Department', 'Level')
        
        # Create the treeview (list)
        self.users_list = ttk.Treeview(parent, columns=columns, show='headings')
        
        # Set up each column
        for col in columns:
            self.users_list.heading(col, text=col)
            self.users_list.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.users_list.yview)
        self.users_list.configure(yscrollcommand=scrollbar.set)
        
        # Place the list and scrollbar
        self.users_list.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load initial data
        self._load_users()
    
    def _create_user_actions(self, parent):
        """Create buttons for user management actions"""
        # Create button container
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=10)
        
        # Create buttons
        ttk.Button(button_frame, text="Refresh", command=self._load_users).pack(side='left', padx=5)
        ttk.Button(button_frame, text="View Details", command=self._view_user_details).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Remove User", command=self._remove_user).pack(side='left', padx=5)
    
    def _create_add_user_tab(self, parent):
        """Create the Add User tab"""
        # Create the tab frame
        tab = ttk.Frame(parent, padding="10")
        parent.add(tab, text="Add User")
        
        # Create the form
        self._create_user_form(tab)
    
    def _create_user_form(self, parent):
        """Create the form for adding a new user"""
        # Create form container
        form = ttk.LabelFrame(parent, text="Add New User", padding="10")
        form.pack(fill='x', expand=True)
        
        # Define form fields
        fields = [
            ('username', 'Username:'),
            ('full_name', 'Full Name:'),
            ('password', 'Password:', True),  # True indicates password field
            ('email', 'Email:'),
            ('phone', 'Phone:'),
            ('address', 'Address:'),
            ('department', 'Department:'),
            ('level', 'Level (0-4):')
        ]
        
        # Create form fields
        self.user_form_vars = {}
        for i, (field, label, *args) in enumerate(fields):
            # Create label
            ttk.Label(form, text=label).grid(row=i, column=0, sticky='w', pady=2)
            
            # Create entry field
            var = tk.StringVar()
            self.user_form_vars[field] = var
            entry = ttk.Entry(form, textvariable=var, show="*" if args and args[0] else "")
            entry.grid(row=i, column=1, sticky='ew', padx=5, pady=2)
        
        # Add role dropdown separately
        ttk.Label(form, text="Role:").grid(row=len(fields), column=0, sticky='w', pady=2)
        self.user_form_vars['role'] = tk.StringVar(value='student')  # Default to student
        role_dropdown = ttk.Combobox(
            form, 
            textvariable=self.user_form_vars['role'],
            values=['admin', 'student'],
            state='readonly',
            width=17
        )
        role_dropdown.grid(row=len(fields), column=1, sticky='ew', padx=5, pady=2)
        
        # Add submit button
        ttk.Button(parent, text="Add User", command=self._add_user).pack(pady=10)
    
    def _create_add_grade_tab(self, parent):
        """Create the Add Grade tab"""
        # Create the tab frame
        tab = ttk.Frame(parent, padding="10")
        parent.add(tab, text="Add Grade")
        
        # Create the form
        self._create_grade_form(tab)
    
    def _create_grade_form(self, parent):
        """Create the form for adding a grade"""
        # Create form container
        form = ttk.LabelFrame(parent, text="Add Student Grade", padding="10")
        form.pack(fill='x', expand=True)
        
        # Define form fields
        fields = [
            ('username', 'Student Username:'),
            ('grade', 'Grade (0-100):')
        ]
        
        # Create form fields
        self.grade_form_vars = {}
        for i, (field, label) in enumerate(fields):
            # Create label
            ttk.Label(form, text=label).grid(row=i, column=0, sticky='w', pady=2)
            
            # Create entry field
            var = tk.StringVar()
            self.grade_form_vars[field] = var
            entry = ttk.Entry(form, textvariable=var)
            entry.grid(row=i, column=1, sticky='ew', padx=5, pady=2)
        
        # Add subject dropdown
        ttk.Label(form, text="Subject:").grid(row=len(fields), column=0, sticky='w', pady=2)
        self.grade_form_vars['subject'] = tk.StringVar(value='Physics')  # Default to Physics
        subject_dropdown = ttk.Combobox(
            form, 
            textvariable=self.grade_form_vars['subject'],
            values=['Physics', 'Math', 'Chemistry', 'Biology', 'English'],
            state='readonly',
            width=17
        )
        subject_dropdown.grid(row=len(fields), column=1, sticky='ew', padx=5, pady=2)
        
        # Add submit button
        ttk.Button(parent, text="Add Grade", command=self._add_grade).pack(pady=10)
    
    def _create_add_eca_tab(self, parent):
        """Create the Add ECA tab"""
        # Create the tab frame
        tab = ttk.Frame(parent, padding="10")
        parent.add(tab, text="Add ECA")
        
        # Create the form
        self._create_eca_form(tab)
    
    def _create_eca_form(self, parent):
        """Create the form for adding an ECA"""
        # Create form container
        form = ttk.LabelFrame(parent, text="Add Student ECA", padding="10")
        form.pack(fill='x', expand=True)
        
        # Define form fields
        fields = [
            ('username', 'Student Username:'),
            ('activity', 'Activity Name:'),
            ('role', 'Role in Activity:'),
            ('hours_per_week', 'Hours per Week:'),
            ('description', 'Description:')
        ]
        
        # Create form fields
        self.eca_form_vars = {}
        for i, (field, label) in enumerate(fields):
            # Create label
            ttk.Label(form, text=label).grid(row=i, column=0, sticky='w', pady=2)
            
            # Create entry field
            var = tk.StringVar()
            self.eca_form_vars[field] = var
            entry = ttk.Entry(form, textvariable=var, width=40 if field == 'description' else None)
            entry.grid(row=i, column=1, sticky='ew', padx=5, pady=2)
        
        # Add submit button
        ttk.Button(parent, text="Add ECA", command=self._add_eca).pack(pady=10)
    
    def _create_student_stats_tab(self, parent):
        """Create the Student Statistics tab"""
        # Create the tab frame
        tab = ttk.Frame(parent, padding="10")
        parent.add(tab, text="Student Statistics")
        
        # Create the interface
        self._create_student_stats_interface(tab)
    
    def _create_student_stats_interface(self, parent):
        """Create the student statistics interface"""
        # Create main container
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True)
        
        # Create left panel (controls)
        left_panel = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        left_panel.pack(side='left', fill='y', padx=5)
        
        # Add student selector
        ttk.Label(left_panel, text="Select Student:").pack(pady=5)
        self.student_selector = ttk.Combobox(left_panel)
        self.student_selector.pack(pady=5)
        
        # Add refresh button
        ttk.Button(left_panel, text="Refresh Data", command=self._refresh_student_stats).pack(pady=10)
        
        # Create right panel (statistics and charts)
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side='right', fill='both', expand=True, padx=5)
        
        # Add statistics display
        stats_frame = ttk.LabelFrame(right_panel, text="Statistics", padding="10")
        stats_frame.pack(fill='x', pady=5)
        self.stats_display = tk.Text(stats_frame, height=10, width=50)
        self.stats_display.pack(fill='x')
        
        # Add chart display
        chart_frame = ttk.LabelFrame(right_panel, text="Charts", padding="10")
        chart_frame.pack(fill='both', expand=True, pady=5)
        self.chart_canvas = tk.Canvas(chart_frame, width=600, height=400)
        self.chart_canvas.pack(fill='both', expand=True)
        
        # Load initial data
        self._load_student_list()
    
    def _create_overall_stats_tab(self, parent):
        """Create the Overall Statistics tab"""
        # Create the tab frame
        tab = ttk.Frame(parent, padding="10")
        parent.add(tab, text="Overall Statistics")
        
        # Create the interface
        self._create_overall_stats_interface(tab)
    
    def _create_overall_stats_interface(self, parent):
        """Create the overall statistics interface"""
        # Create main container
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True)
        
        # Create left panel (statistics)
        left_panel = ttk.LabelFrame(main_frame, text="Overall Statistics", padding="10")
        left_panel.pack(side='left', fill='y', padx=5)
        
        # Add statistics display
        self.overall_stats_display = tk.Text(left_panel, height=20, width=40)
        self.overall_stats_display.pack(fill='x')
        
        # Add refresh button
        ttk.Button(left_panel, text="Refresh Statistics", 
                  command=self._refresh_overall_stats).pack(pady=10)
        
        # Create right panel (charts)
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side='right', fill='both', expand=True, padx=5)
        
        # Create chart tabs
        chart_tabs = ttk.Notebook(right_panel)
        chart_tabs.pack(fill='both', expand=True)
        
        # Create each chart tab
        self._create_chart_tab(chart_tabs, "Grades Distribution", 'grades')
        self._create_chart_tab(chart_tabs, "Subject Performance", 'subjects')
        self._create_chart_tab(chart_tabs, "ECA Distribution", 'eca')
        self._create_chart_tab(chart_tabs, "Hours Distribution", 'hours')
        
        # Load initial data
        self._refresh_overall_stats()
    
    def _create_chart_tab(self, parent, title, chart_type):
        """Create a tab for displaying a chart"""
        # Create tab frame
        tab = ttk.Frame(parent)
        parent.add(tab, text=title)
        
        # Create canvas for chart
        canvas = tk.Canvas(tab, width=600, height=400)
        canvas.pack(fill='both', expand=True)
        
        # Store canvas reference
        if chart_type == 'grades':
            self.grades_chart = canvas
        elif chart_type == 'subjects':
            self.subjects_chart = canvas
        elif chart_type == 'eca':
            self.eca_chart = canvas
        elif chart_type == 'hours':
            self.hours_chart = canvas
    
    # Data handling methods
    def _load_users(self):
        """Load the list of users"""
        # Clear existing items
        for item in self.users_list.get_children():
            self.users_list.delete(item)
        
        # Load users from database
        users = list_all_users()
        if users:
            for user in users:
                self.users_list.insert('', 'end', values=(
                    user['username'],
                    user['full_name'],
                    user['role'],
                    user.get('email', ''),
                    user.get('department', ''),
                    user.get('level', '')
                ))
    
    def _load_student_list(self):
        """Load the list of students for the selector"""
        users = list_all_users()
        if users:
            students = [user['username'] for user in users if user['role'] == 'student']
            self.student_selector['values'] = students
            if students:
                self.student_selector.set(students[0])
                self._refresh_student_stats()
    
    def _refresh_student_stats(self):
        """Refresh the statistics for the selected student"""
        username = self.student_selector.get()
        if not username:
            return
        
        # Clear previous statistics
        self.stats_display.delete('1.0', tk.END)
        
        # Get student data
        grades = get_student_grades(username)
        eca = get_student_eca(username)
        
        if not grades and not eca:
            self.stats_display.insert(tk.END, "No data available for this student.")
            return
        
        # Calculate statistics
        gpa = self.analytics.calculate_gpa(username)
        grade_stats = self.analytics.get_grade_statistics(username)
        eca_summary = self.analytics.get_eca_summary(username)
        
        # Display statistics
        stats_text = f"""Student: {username}

GPA: {gpa if gpa else 'N/A'}

Grade Statistics:
"""
        if grade_stats:
            stats_text += f"""Mean: {grade_stats['mean']}
Median: {grade_stats['median']}
Min: {grade_stats['min']}
Max: {grade_stats['max']}
Standard Deviation: {grade_stats['std_dev']}

"""
        
        if eca_summary:
            stats_text += f"""ECA Summary:
Total Activities: {eca_summary['total_activities']}
Total Hours per Week: {eca_summary['total_hours']}
"""
        
        self.stats_display.insert(tk.END, stats_text)
        
        # Create and display charts
        if grades and eca:
            chart_path = self.analytics.create_performance_summary(grades, eca, username)
        elif grades:
            chart_path = self.analytics.create_grades_chart(grades, username)
        elif eca:
            chart_path = self.analytics.create_eca_chart(eca, username)
        else:
            return
        
        self._display_chart(self.chart_canvas, chart_path)
    
    def _refresh_overall_stats(self):
        """Refresh the overall statistics and charts"""
        # Get statistics
        stats = self.analytics.get_overall_statistics()
        if not stats:
            self.overall_stats_display.delete('1.0', tk.END)
            self.overall_stats_display.insert(tk.END, "No data available.")
            return
        
        # Display statistics
        stats_text = f"""Overall Statistics:

Total Students: {stats['total_students']}
Total Grades: {stats['total_grades']}
Total ECAs: {stats['total_ecas']}

Grade Statistics:
Average Grade: {stats['average_grade']:.2f}
Median Grade: {stats['median_grade']:.2f}
Standard Deviation: {stats['grade_std_dev']:.2f}

ECA Statistics:
Average Hours per Week: {stats['average_hours']:.2f}
Total Hours: {stats['total_hours']:.2f}
Unique Activities: {stats['unique_activities']}
Unique Subjects: {stats['unique_subjects']}
"""
        self.overall_stats_display.delete('1.0', tk.END)
        self.overall_stats_display.insert(tk.END, stats_text)
        
        # Create and display charts
        self._display_chart(self.grades_chart, self.analytics.create_overall_grades_distribution())
        self._display_chart(self.subjects_chart, self.analytics.create_subject_performance_comparison())
        self._display_chart(self.eca_chart, self.analytics.create_eca_distribution())
        self._display_chart(self.hours_chart, self.analytics.create_hours_distribution())
    
    def _display_chart(self, canvas, chart_path):
        """Display a chart in the given canvas"""
        if not chart_path or not os.path.exists(chart_path):
            # Clear the canvas if no chart is available
            canvas.delete("all")
            return
        
        try:
            # Load and display the chart
            image = Image.open(chart_path)
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Update canvas
            canvas.delete("all")  # Clear previous content
            canvas.create_image(0, 0, anchor='nw', image=photo)
            canvas.image = photo  # Keep a reference
            
        except Exception as e:
            print(f"Error displaying chart: {e}")
            canvas.delete("all")  # Clear canvas on error
    
    # Action handlers
    def _handle_logout(self):
        """Handle the logout action"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if isinstance(self.root, tk.Toplevel):
                self.root.master.destroy()
            else:
                self.root.destroy()
    
    def _view_user_details(self):
        """View details of the selected user"""
        selected = self.users_list.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to view")
            return
        
        username = self.users_list.item(selected[0])['values'][0]
        user = get_user_details(username)
        
        if user:
            details = f"""
            Username: {user['username']}
            Full Name: {user['full_name']}
            Role: {user['role']}
            Email: {user.get('email', 'Not set')}
            Phone: {user.get('phone', 'Not set')}
            Address: {user.get('address', 'Not set')}
            Department: {user.get('department', 'Not set')}
            Level: {user.get('level', 'Not set')}
            """
            messagebox.showinfo("User Details", details)
        else:
            messagebox.showerror("Error", "Failed to get user details")
    
    def _remove_user(self):
        """Remove the selected user"""
        selected = self.users_list.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to remove")
            return
        
        username = self.users_list.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove user '{username}'?"):
            if remove_user(username):
                messagebox.showinfo("Success", "User removed successfully")
                self._load_users()
            else:
                messagebox.showerror("Error", "Failed to remove user")
    
    def _add_user(self):
        """Add a new user"""
        # Collect form data
        data = {field: var.get() for field, var in self.user_form_vars.items()}
        
        # Validate required fields
        if not all([data['username'], data['full_name'], data['password'], data['role']]):
            messagebox.showwarning("Warning", "Username, full name, password, and role are required")
            return
        
        # Add user
        if add_user(
            data['username'],
            data['full_name'],
            data['password'],
            data['role'],
            data['email'],
            data['phone'],
            data['address'],
            data['department'],
            data['level']
        ):
            messagebox.showinfo("Success", "User added successfully")
            # Clear form
            for var in self.user_form_vars.values():
                var.set('')
            # Refresh users list
            self._load_users()
        else:
            messagebox.showerror("Error", "Failed to add user")
    
    def _add_grade(self):
        """Add a new grade"""
        # Collect form data
        data = {field: var.get() for field, var in self.grade_form_vars.items()}
        
        # Validate required fields
        if not all([data['username'], data['subject'], data['grade']]):
            messagebox.showwarning("Warning", "All fields are required")
            return
        
        # Validate grade is numeric and between 0-100
        try:
            grade = float(data['grade'])
            if not (0 <= grade <= 100):
                messagebox.showwarning("Warning", "Grade must be between 0 and 100")
                return
        except ValueError:
            messagebox.showwarning("Warning", "Grade must be a number")
            return
        
        # Add grade
        if add_student_grade(data['username'], data['subject'], grade):
            messagebox.showinfo("Success", f"Grade {grade} added successfully for {data['username']} in {data['subject']}")
            # Clear form
            for var in self.grade_form_vars.values():
                var.set('')
        else:
            messagebox.showerror("Error", "Failed to add grade. Please check if the student exists and all data is valid.")
    
    def _add_eca(self):
        """Add a new ECA"""
        # Collect form data
        data = {field: var.get() for field, var in self.eca_form_vars.items()}
        
        # Validate required fields
        if not all([data['username'], data['activity'], data['role'], data['hours_per_week']]):
            messagebox.showwarning("Warning", "Username, activity, role, and hours are required")
            return
        
        # Validate hours is numeric and positive
        try:
            hours = float(data['hours_per_week'])
            if hours < 0:
                messagebox.showwarning("Warning", "Hours per week must be positive")
                return
        except ValueError:
            messagebox.showwarning("Warning", "Hours per week must be a number")
            return
        
        # Add ECA
        if add_student_eca(
            data['username'],
            data['activity'],
            data['role'],
            data['hours_per_week'],
            data.get('description', '')
        ):
            messagebox.showinfo("Success", f"ECA '{data['activity']}' added successfully for {data['username']}")
            # Clear form
            for var in self.eca_form_vars.values():
                var.set('')
        else:
            messagebox.showerror("Error", "Failed to add ECA. Please check if the student exists and all data is valid.")