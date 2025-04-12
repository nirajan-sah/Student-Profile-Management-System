import tkinter as tk
from tkinter import ttk, messagebox
from student import get_student_grades, get_student_eca, update_student_profile
from auth import get_user_details


class StudentView:
    def __init__(self, username, parent=None):
        self.username = username
        self.user_details = get_user_details(username)
        
        # Create main window
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title(f"Student View - {self.user_details['full_name']}")
        self.root.geometry("600x400")
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"600x400+{x}+{y}")
        
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
            
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if isinstance(self.root, tk.Toplevel):
                self.root.master.destroy()  # Close the entire application
            else:
                self.root.destroy()  # Close just this window 