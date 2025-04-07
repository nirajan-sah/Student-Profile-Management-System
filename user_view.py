import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from auth import authenticate, get_user_details, get_student_grades, get_student_eca, update_student_profile
from user_management import add_user, delete_user
from student_data import calculate_average_grades, calculate_eca_activity, update_student_data
from ui_components import (
    COLORS, FONTS, create_styled_button, create_styled_label,
    create_styled_entry, create_styled_frame, create_styled_combobox
)

def create_styled_button(parent, text, command, bg_color=COLORS["primary"]):
    """
    Create a styled button with consistent appearance.
    """
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg="white",
        font=FONTS["normal"],
        relief=tk.FLAT,
        padx=20,
        pady=10
    )
    button.bind("<Enter>", lambda e: button.config(bg=adjust_color(bg_color, -20)))
    button.bind("<Leave>", lambda e: button.config(bg=bg_color))
    return button

def create_styled_label(parent, text, font=FONTS["normal"], fg=COLORS["dark"]):
    """
    Create a styled label with consistent appearance.
    """
    return tk.Label(
        parent,
        text=text,
        font=font,
        fg=fg,
        bg=COLORS["light"]
    )

def create_styled_entry(parent, show=None):
    """
    Create a styled entry field with consistent appearance.
    """
    return tk.Entry(
        parent,
        font=FONTS["normal"],
        relief=tk.SOLID,
        borderwidth=1,
        show=show
    )

def create_styled_frame(parent, bg=COLORS["light"]):
    """
    Create a styled frame with consistent appearance.
    """
    return tk.Frame(
        parent,
        bg=bg,
        padx=20,
        pady=20
    )

def adjust_color(color, amount):
    """
    Adjust the brightness of a color by the given amount.
    """
    # Convert hex to RGB
    color = color.lstrip('#')
    r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    
    # Adjust each component
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    
    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}'

def create_styled_combobox(parent, values):
    """
    Create a styled combobox with consistent appearance.
    """
    style = ttk.Style()
    style.configure(
        "Custom.TCombobox",
        fieldbackground=COLORS["light"],
        background=COLORS["light"],
        arrowcolor=COLORS["dark"]
    )
    
    combo = ttk.Combobox(
        parent,
        values=values,
        style="Custom.TCombobox",
        font=FONTS["normal"]
    )
    return combo

def login_window():
    """
    Create and show the login window.
    """
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        user = authenticate(username, password)
        if user:
            login_window.destroy()
            if user.role == "admin":
                admin_dashboard(user)
            else:
                student_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    login_window = tk.Tk()
    login_window.title("Student Profile Management System")
    login_window.geometry("400x500")
    login_window.configure(bg=COLORS["light"])
    
    # Create main frame
    main_frame = create_styled_frame(login_window)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    create_styled_label(
        main_frame,
        "Student Profile\nManagement System",
        FONTS["heading"],
        fg=COLORS["primary"]
    ).pack(pady=20)
    
    # Login form
    form_frame = create_styled_frame(main_frame)
    form_frame.pack(fill=tk.BOTH, expand=True)
    
    create_styled_label(form_frame, "Username:", FONTS["normal"]).pack(anchor=tk.W)
    username_entry = create_styled_entry(form_frame)
    username_entry.pack(fill=tk.X, pady=(0, 20))
    
    create_styled_label(form_frame, "Password:", FONTS["normal"]).pack(anchor=tk.W)
    password_entry = create_styled_entry(form_frame, show="*")
    password_entry.pack(fill=tk.X, pady=(0, 20))
    
    create_styled_button(
        form_frame,
        "Login",
        handle_login,
        COLORS["primary"]
    ).pack(fill=tk.X, pady=10)
    
    # Demo credentials
    create_styled_label(
        form_frame,
        "Demo Credentials:\nAdmin: admin/admin123\nStudent: student1/student123",
        FONTS["small"],
        fg=COLORS["dark"]
    ).pack(pady=20)
    
    login_window.mainloop()

def admin_dashboard(user):
    """
    Create and show the admin dashboard.
    """
    def handle_logout():
        admin_window.destroy()
        login_window()
    
    def add_user_ui():
        def submit():
            new_username = username_entry.get()
            new_full_name = full_name_entry.get()
            new_password = password_entry.get()
            new_role = role_var.get()
            
            if not all([new_username, new_full_name, new_password, new_role]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if add_user(new_username, new_full_name, new_password, new_role):
                messagebox.showinfo("Success", "User added successfully!")
                add_user_window.destroy()
                admin_dashboard(user)  # Refresh dashboard
            else:
                messagebox.showerror("Error", "Failed to add user. Username might already exist.")
        
        add_user_window = tk.Toplevel()
        add_user_window.title("Add User")
        add_user_window.geometry("500x400")
        add_user_window.configure(bg=COLORS["light"])
        
        # Create main frame
        main_frame = create_styled_frame(add_user_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        create_styled_label(
            main_frame,
            "Add New User",
            FONTS["subheading"],
            fg=COLORS["primary"]
        ).pack(pady=(0, 20))
        
        # Username field
        create_styled_label(main_frame, "Username:", FONTS["normal"]).pack(anchor=tk.W)
        username_entry = create_styled_entry(main_frame)
        username_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Full Name field
        create_styled_label(main_frame, "Full Name:", FONTS["normal"]).pack(anchor=tk.W)
        full_name_entry = create_styled_entry(main_frame)
        full_name_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Password field
        create_styled_label(main_frame, "Password:", FONTS["normal"]).pack(anchor=tk.W)
        password_entry = create_styled_entry(main_frame, show="*")
        password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Role field
        create_styled_label(main_frame, "Role:", FONTS["normal"]).pack(anchor=tk.W)
        role_var = tk.StringVar(value="student")
        role_menu = create_styled_combobox(main_frame, ["admin", "student"])
        role_menu.set("student")
        role_menu.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = create_styled_frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        create_styled_button(
            button_frame,
            "Submit",
            submit,
            COLORS["success"]
        ).pack(side=tk.RIGHT, padx=5)
        
        create_styled_button(
            button_frame,
            "Cancel",
            add_user_window.destroy,
            COLORS["secondary"]
        ).pack(side=tk.RIGHT, padx=5)
    
    def delete_user_ui():
        def submit():
            username_to_delete = username_entry.get()
            if not username_to_delete:
                messagebox.showerror("Error", "Please enter a username")
                return
            
            if delete_user(username_to_delete):
                messagebox.showinfo("Success", "User deleted successfully!")
                delete_user_window.destroy()
                admin_dashboard(user)  # Refresh dashboard
            else:
                messagebox.showerror("Error", "Failed to delete user. Username might not exist.")
        
        delete_user_window = tk.Toplevel()
        delete_user_window.title("Delete User")
        delete_user_window.geometry("500x300")
        delete_user_window.configure(bg=COLORS["light"])
        
        # Create main frame
        main_frame = create_styled_frame(delete_user_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        create_styled_label(
            main_frame,
            "Delete User",
            FONTS["subheading"],
            fg=COLORS["primary"]
        ).pack(pady=(0, 20))
        
        create_styled_label(
            main_frame,
            "Warning: This action cannot be undone!",
            FONTS["normal"],
            fg=COLORS["danger"]
        ).pack(pady=(0, 20))
        
        # Username field
        create_styled_label(main_frame, "Username to delete:", FONTS["normal"]).pack(anchor=tk.W)
        username_entry = create_styled_entry(main_frame)
        username_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = create_styled_frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        create_styled_button(
            button_frame,
            "Delete",
            submit,
            COLORS["danger"]
        ).pack(side=tk.RIGHT, padx=5)
        
        create_styled_button(
            button_frame,
            "Cancel",
            delete_user_window.destroy,
            COLORS["secondary"]
        ).pack(side=tk.RIGHT, padx=5)
    
    def view_average_grades():
        try:
            # Get average grades data
            averages = calculate_average_grades()
            
            # Create visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(range(1, len(averages) + 1), averages.values())
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}',
                       ha='center', va='bottom')
            
            ax.set_xlabel('Subject')
            ax.set_ylabel('Average Grade')
            ax.set_title('Average Grades per Subject')
            ax.set_xticks(range(1, len(averages) + 1))
            ax.set_xticklabels(averages.keys())
            
            # Create new window for the plot
            plot_window = tk.Toplevel()
            plot_window.title("Average Grades per Subject")
            plot_window.geometry("800x600")
            
            # Embed the plot in the window
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add save button
            save_button = create_styled_button(plot_window, "Save and Return", lambda: plot_window.destroy(), COLORS["success"])
            save_button.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate average grades: {str(e)}")
    
    def view_eca_activity():
        try:
            # Get ECA activity data
            activity_data = calculate_eca_activity()
            
            # Create visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(range(1, len(activity_data) + 1), activity_data.values())
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.0f}',
                       ha='center', va='bottom')
            
            ax.set_xlabel('Student')
            ax.set_ylabel('Number of Activities')
            ax.set_title('ECA Activity by Student')
            ax.set_xticks(range(1, len(activity_data) + 1))
            ax.set_xticklabels(activity_data.keys(), rotation=45)
            
            # Create new window for the plot
            plot_window = tk.Toplevel()
            plot_window.title("ECA Activity Analysis")
            plot_window.geometry("800x600")
            
            # Embed the plot in the window
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add save button
            save_button = create_styled_button(plot_window, "Save and Return", lambda: plot_window.destroy(), COLORS["success"])
            save_button.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate ECA activity: {str(e)}")
    
    def modify_student_data():
        def load_student_data():
            username = student_var.get()
            if not username:
                messagebox.showerror("Error", "Please select a student")
                return
            
            # Load student data
            student_data = get_user_details(username)
            if student_data:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, student_data.full_name)
                
                # Load grades
                grades = get_student_grades(username)
                if grades:
                    for i, grade in enumerate(grades):
                        grade_entries[i].delete(0, tk.END)
                        grade_entries[i].insert(0, grade)
                
                # Load ECA
                eca = get_student_eca(username)
                if eca:
                    for i, activity in enumerate(eca):
                        eca_entries[i].delete(0, tk.END)
                        eca_entries[i].insert(0, activity)
        
        def save_changes():
            username = student_var.get()
            if not username:
                messagebox.showerror("Error", "Please select a student")
                return
            
            # Get values
            new_name = name_entry.get()
            new_grades = [entry.get() for entry in grade_entries]
            new_eca = [entry.get() for entry in eca_entries]
            
            # Update data
            if update_student_data(username, new_name, new_grades, new_eca):
                messagebox.showinfo("Success", "Student data updated successfully!")
                modify_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to update student data")
        
        modify_window = tk.Toplevel()
        modify_window.title("Modify Student Data")
        modify_window.geometry("600x800")
        modify_window.configure(bg=COLORS["light"])
        
        # Create main frame
        main_frame = create_styled_frame(modify_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        create_styled_label(
            main_frame,
            "Modify Student Data",
            FONTS["subheading"],
            fg=COLORS["primary"]
        ).pack(pady=(0, 20))
        
        # Student selection
        create_styled_label(main_frame, "Select Student:", FONTS["normal"]).pack(anchor=tk.W)
        student_var = tk.StringVar()
        student_menu = create_styled_combobox(main_frame, get_student_list())
        student_menu.pack(fill=tk.X, pady=(0, 20))
        
        # Load button
        create_styled_button(
            main_frame,
            "Load Student Data",
            load_student_data,
            COLORS["primary"]
        ).pack(fill=tk.X, pady=(0, 20))
        
        # Personal info
        create_styled_label(main_frame, "Personal Information", FONTS["normal"]).pack(anchor=tk.W)
        create_styled_label(main_frame, "Full Name:", FONTS["normal"]).pack(anchor=tk.W)
        name_entry = create_styled_entry(main_frame)
        name_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Grades
        create_styled_label(main_frame, "Grades", FONTS["normal"]).pack(anchor=tk.W)
        grade_entries = []
        for i in range(5):
            create_styled_label(main_frame, f"Subject {i+1}:", FONTS["normal"]).pack(anchor=tk.W)
            entry = create_styled_entry(main_frame)
            entry.pack(fill=tk.X, pady=(0, 10))
            grade_entries.append(entry)
        
        # ECA
        create_styled_label(main_frame, "Extracurricular Activities", FONTS["normal"]).pack(anchor=tk.W)
        eca_entries = []
        for i in range(3):
            create_styled_label(main_frame, f"Activity {i+1}:", FONTS["normal"]).pack(anchor=tk.W)
            entry = create_styled_entry(main_frame)
            entry.pack(fill=tk.X, pady=(0, 10))
            eca_entries.append(entry)
        
        # Buttons
        button_frame = create_styled_frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        create_styled_button(
            button_frame,
            "Save Changes",
            save_changes,
            COLORS["success"]
        ).pack(side=tk.RIGHT, padx=5)
        
        create_styled_button(
            button_frame,
            "Cancel",
            modify_window.destroy,
            COLORS["secondary"]
        ).pack(side=tk.RIGHT, padx=5)
    
    def view_student_details():
        def load_details():
            username = student_var.get()
            if not username:
                messagebox.showerror("Error", "Please select a student")
                return
            
            # Get student details
            student = get_user_details(username)
            if student:
                # Update personal info
                name_label.config(text=f"Full Name: {student.full_name}")
                
                # Update grades
                grades = get_student_grades(username)
                if grades:
                    grades_text = "\n".join([f"Subject {i+1}: {grade}" for i, grade in enumerate(grades)])
                    grades_label.config(text=grades_text)
                else:
                    grades_label.config(text="No grades found.")
                
                # Update ECA
                eca = get_student_eca(username)
                if eca:
                    eca_text = "\n".join([f"Activity {i+1}: {activity}" for i, activity in enumerate(eca)])
                    eca_label.config(text=eca_text)
                else:
                    eca_label.config(text="No extracurricular activities found.")
        
        details_window = tk.Toplevel()
        details_window.title("Student Details")
        details_window.geometry("500x600")
        details_window.configure(bg=COLORS["light"])
        
        # Create main frame
        main_frame = create_styled_frame(details_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        create_styled_label(
            main_frame,
            "Student Details",
            FONTS["subheading"],
            fg=COLORS["primary"]
        ).pack(pady=(0, 20))
        
        # Student selection
        create_styled_label(main_frame, "Select Student:", FONTS["normal"]).pack(anchor=tk.W)
        student_var = tk.StringVar()
        student_menu = create_styled_combobox(main_frame, get_student_list())
        student_menu.pack(fill=tk.X, pady=(0, 20))
        
        # Load button
        create_styled_button(
            main_frame,
            "Load Details",
            load_details,
            COLORS["primary"]
        ).pack(fill=tk.X, pady=(0, 20))
        
        # Details labels
        name_label = create_styled_label(main_frame, "Full Name: ", FONTS["normal"])
        name_label.pack(anchor=tk.W)
        
        create_styled_label(main_frame, "Grades:", FONTS["normal"]).pack(anchor=tk.W, pady=(20, 10))
        grades_label = create_styled_label(main_frame, "", FONTS["normal"])
        grades_label.pack(anchor=tk.W)
        
        create_styled_label(main_frame, "Extracurricular Activities:", FONTS["normal"]).pack(anchor=tk.W, pady=(20, 10))
        eca_label = create_styled_label(main_frame, "", FONTS["normal"])
        eca_label.pack(anchor=tk.W)
        
        # Close button
        create_styled_button(
            main_frame,
            "Close",
            details_window.destroy,
            COLORS["secondary"]
        ).pack(fill=tk.X, pady=20)
    
    def get_student_list():
        try:
            df = pd.read_csv("data/users.csv")
            return df[df['role'] == 'student']['username'].tolist()
        except:
            return []
    
    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("800x600")
    admin_window.configure(bg=COLORS["light"])
    
    # Create main frame
    main_frame = create_styled_frame(admin_window)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Header
    header_frame = create_styled_frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 20))
    
    create_styled_label(
        header_frame,
        f"Welcome, {user.full_name}",
        FONTS["subheading"],
        fg=COLORS["primary"]
    ).pack(side=tk.LEFT)
    
    create_styled_button(
        header_frame,
        "Logout",
        handle_logout,
        COLORS["danger"]
    ).pack(side=tk.RIGHT)
    
    # Admin functions
    functions_frame = create_styled_frame(main_frame)
    functions_frame.pack(fill=tk.BOTH, expand=True)
    
    # User management
    user_frame = create_styled_frame(functions_frame)
    user_frame.pack(fill=tk.X, pady=10)
    
    create_styled_label(
        user_frame,
        "User Management",
        FONTS["normal"],
        fg=COLORS["primary"]
    ).pack(anchor=tk.W)
    
    button_frame = create_styled_frame(user_frame)
    button_frame.pack(fill=tk.X, pady=10)
    
    create_styled_button(
        button_frame,
        "Add User",
        add_user_ui,
        COLORS["success"]
    ).pack(side=tk.LEFT, padx=5)
    
    create_styled_button(
        button_frame,
        "Delete User",
        delete_user_ui,
        COLORS["danger"]
    ).pack(side=tk.LEFT, padx=5)
    
    # Student data
    data_frame = create_styled_frame(functions_frame)
    data_frame.pack(fill=tk.X, pady=10)
    
    create_styled_label(
        data_frame,
        "Student Data",
        FONTS["normal"],
        fg=COLORS["primary"]
    ).pack(anchor=tk.W)
    
    button_frame = create_styled_frame(data_frame)
    button_frame.pack(fill=tk.X, pady=10)
    
    create_styled_button(
        button_frame,
        "View Student Details",
        view_student_details,
        COLORS["primary"]
    ).pack(side=tk.LEFT, padx=5)
    
    create_styled_button(
        button_frame,
        "Modify Student Data",
        modify_student_data,
        COLORS["warning"]
    ).pack(side=tk.LEFT, padx=5)
    
    # Analytics
    analytics_frame = create_styled_frame(functions_frame)
    analytics_frame.pack(fill=tk.X, pady=10)
    
    create_styled_label(
        analytics_frame,
        "Analytics",
        FONTS["normal"],
        fg=COLORS["primary"]
    ).pack(anchor=tk.W)
    
    button_frame = create_styled_frame(analytics_frame)
    button_frame.pack(fill=tk.X, pady=10)
    
    create_styled_button(
        button_frame,
        "View Average Grades",
        view_average_grades,
        COLORS["primary"]
    ).pack(side=tk.LEFT, padx=5)
    
    create_styled_button(
        button_frame,
        "View ECA Activity",
        view_eca_activity,
        COLORS["secondary"]
    ).pack(side=tk.LEFT, padx=5)
    
    admin_window.mainloop()

def student_dashboard(user):
    """
    Create and show the student dashboard.
    """
    def handle_logout():
        student_window.destroy()
        login_window()
    
    def update_profile():
        def save_changes():
            new_name = name_entry.get()
            if not new_name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            try:
                update_student_profile(user.username, new_name)
                messagebox.showinfo("Success", "Profile updated successfully!")
                update_window.destroy()
                student_dashboard(user)  # Refresh dashboard
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {str(e)}")
        
        update_window = tk.Toplevel()
        update_window.title("Update Profile")
        update_window.geometry("400x300")
        update_window.configure(bg=COLORS["light"])
        
        main_frame = create_styled_frame(update_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        create_styled_label(main_frame, "Update Profile", FONTS["subheading"]).pack(pady=20)
        
        create_styled_label(main_frame, "Full Name:", FONTS["normal"]).pack(anchor=tk.W)
        name_entry = create_styled_entry(main_frame)
        name_entry.insert(0, user.full_name)
        name_entry.pack(fill=tk.X, pady=(0, 20))
        
        create_styled_button(
            main_frame,
            "Save Changes",
            save_changes,
            COLORS["success"]
        ).pack(fill=tk.X, pady=10)
    
    student_window = tk.Tk()
    student_window.title("Student Dashboard")
    student_window.geometry("800x600")
    student_window.configure(bg=COLORS["light"])
    
    # Create main frame
    main_frame = create_styled_frame(student_window)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Header
    header_frame = create_styled_frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 20))
    
    create_styled_label(
        header_frame,
        f"Welcome, {user.full_name}",
        FONTS["subheading"],
        fg=COLORS["primary"]
    ).pack(side=tk.LEFT)
    
    create_styled_button(
        header_frame,
        "Logout",
        handle_logout,
        COLORS["danger"]
    ).pack(side=tk.RIGHT)
    
    # Student info
    info_frame = create_styled_frame(main_frame)
    info_frame.pack(fill=tk.BOTH, expand=True)
    
    # Personal info
    personal_frame = create_styled_frame(info_frame)
    personal_frame.pack(fill=tk.X, pady=10)
    
    create_styled_label(
        personal_frame,
        "Personal Information",
        FONTS["normal"],
        fg=COLORS["primary"]
    ).pack(anchor=tk.W)
    
    create_styled_label(
        personal_frame,
        f"Username: {user.username}",
        FONTS["normal"]
    ).pack(anchor=tk.W)
    
    create_styled_label(
        personal_frame,
        f"Full Name: {user.full_name}",
        FONTS["normal"]
    ).pack(anchor=tk.W)
    
    create_styled_button(
        personal_frame,
        "Update Profile",
        update_profile,
        COLORS["primary"]
    ).pack(anchor=tk.W, pady=10)
    
    # Grades
    grades_frame = create_styled_frame(info_frame)
    grades_frame.pack(fill=tk.X, pady=10)
    
    create_styled_label(
        grades_frame,
        "Grades",
        FONTS["normal"],
        fg=COLORS["primary"]
    ).pack(anchor=tk.W)
    
    grades = get_student_grades(user.username)
    if grades:
        for i, grade in enumerate(grades):
            create_styled_label(
                grades_frame,
                f"Subject {i+1}: {grade}",
                FONTS["normal"]
            ).pack(anchor=tk.W)
    else:
        create_styled_label(
            grades_frame,
            "No grades found.",
            FONTS["normal"]
        ).pack(anchor=tk.W)
    
    # ECA
    eca_frame = create_styled_frame(info_frame)
    eca_frame.pack(fill=tk.X, pady=10)
    
    create_styled_label(
        eca_frame,
        "Extracurricular Activities",
        FONTS["normal"],
        fg=COLORS["primary"]
    ).pack(anchor=tk.W)
    
    eca = get_student_eca(user.username)
    if eca:
        for i, activity in enumerate(eca):
            create_styled_label(
                eca_frame,
                f"Activity {i+1}: {activity}",
                FONTS["normal"]
            ).pack(anchor=tk.W)
    else:
        create_styled_label(
            eca_frame,
            "No extracurricular activities found.",
            FONTS["normal"]
        ).pack(anchor=tk.W)
    
    student_window.mainloop()

if __name__ == "__main__":
    login_window()