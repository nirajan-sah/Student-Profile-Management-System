import tkinter as tk
from tkinter import messagebox, ttk
from auth import authenticate, get_user_details, add_user, delete_user, get_student_grades, get_student_eca, update_student_profile

# Define color scheme
COLORS = {
    "primary": "#4a6fa5",
    "secondary": "#6c757d",
    "success": "#28a745",
    "danger": "#dc3545",
    "light": "#f8f9fa",
    "dark": "#343a40",
    "white": "#ffffff"
}

# Define fonts
FONTS = {
    "heading": ("Arial", 18, "bold"),
    "subheading": ("Arial", 14, "bold"),
    "normal": ("Arial", 12),
    "small": ("Arial", 10)
}

def apply_style(widget, bg_color=None, fg_color=None, font=None, width=None, height=None):
    """Apply consistent styling to widgets"""
    if bg_color:
        widget.configure(bg=bg_color)
    if fg_color:
        widget.configure(fg=fg_color)
    if font:
        widget.configure(font=font)
    if width:
        widget.configure(width=width)
    if height:
        widget.configure(height=height)
    return widget

def create_styled_button(parent, text, command, bg_color=COLORS["primary"], fg_color=COLORS["white"]):
    """Create a consistently styled button"""
    button = tk.Button(parent, text=text, command=command, 
                      bg=bg_color, fg=fg_color, font=FONTS["normal"],
                      relief=tk.RAISED, borderwidth=1, padx=10, pady=5)
    return button

def create_styled_entry(parent, show=None):
    """Create a consistently styled entry field"""
    entry = tk.Entry(parent, show=show, font=FONTS["normal"], width=30)
    return entry

def create_styled_label(parent, text, font=FONTS["normal"]):
    """Create a consistently styled label"""
    label = tk.Label(parent, text=text, font=font, bg=COLORS["light"])
    return label

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Authenticate the user
    role = authenticate(username, password)
    if role:
        user = get_user_details(username)
        if user:
            messagebox.showinfo("Login Successful",
                                f"Welcome, {user.full_name} ({user.role})!")
            if role == "admin":
                admin_dashboard(user)
            elif role == "student":
                student_dashboard(user)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def admin_dashboard(user):
    """
    Admin dashboard functionality.
    """
    def add_user_ui():
        """
        UI for adding a new user.
        """
        def submit():
            new_username = username_entry.get()
            new_full_name = full_name_entry.get()
            new_password = password_entry.get()
            new_role = role_var.get()

            if add_user(new_username, new_full_name, new_password, new_role):
                messagebox.showinfo("Success", "User added successfully!")
                add_user_window.destroy()
            else:
                messagebox.showerror(
                    "Error", "Failed to add user. Username might already exist.")

        add_user_window = tk.Toplevel()
        add_user_window.title("Add User")
        add_user_window.geometry("500x400")
        add_user_window.configure(bg=COLORS["light"])
        
        # Center the window
        add_user_window.update_idletasks()
        width = add_user_window.winfo_width()
        height = add_user_window.winfo_height()
        x = (add_user_window.winfo_screenwidth() // 2) - (width // 2)
        y = (add_user_window.winfo_screenheight() // 2) - (height // 2)
        add_user_window.geometry(f'{width}x{height}+{x}+{y}')

        # Create a frame for the form
        form_frame = tk.Frame(add_user_window, bg=COLORS["light"], padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        create_styled_label(form_frame, "Add New User", FONTS["heading"]).pack(pady=(0, 20))

        # Username field
        username_frame = tk.Frame(form_frame, bg=COLORS["light"])
        username_frame.pack(fill=tk.X, pady=5)
        create_styled_label(username_frame, "Username:").pack(side=tk.LEFT, padx=(0, 10))
        username_entry = create_styled_entry(username_frame)
        username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Full Name field
        name_frame = tk.Frame(form_frame, bg=COLORS["light"])
        name_frame.pack(fill=tk.X, pady=5)
        create_styled_label(name_frame, "Full Name:").pack(side=tk.LEFT, padx=(0, 10))
        full_name_entry = create_styled_entry(name_frame)
        full_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Password field
        password_frame = tk.Frame(form_frame, bg=COLORS["light"])
        password_frame.pack(fill=tk.X, pady=5)
        create_styled_label(password_frame, "Password:").pack(side=tk.LEFT, padx=(0, 10))
        password_entry = create_styled_entry(password_frame, show="*")
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Role field
        role_frame = tk.Frame(form_frame, bg=COLORS["light"])
        role_frame.pack(fill=tk.X, pady=5)
        create_styled_label(role_frame, "Role:").pack(side=tk.LEFT, padx=(0, 10))
        role_var = tk.StringVar(value="student")
        role_menu = tk.OptionMenu(role_frame, role_var, "admin", "student")
        role_menu.config(font=FONTS["normal"], bg=COLORS["white"], width=15)
        role_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Buttons
        button_frame = tk.Frame(form_frame, bg=COLORS["light"])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        create_styled_button(button_frame, "Submit", submit, COLORS["success"]).pack(side=tk.RIGHT, padx=5)
        create_styled_button(button_frame, "Cancel", add_user_window.destroy, COLORS["secondary"]).pack(side=tk.RIGHT, padx=5)

    def delete_user_ui():
        """
        UI for deleting a user.
        """
        def submit():
            username_to_delete = username_entry.get()
            if delete_user(username_to_delete):
                messagebox.showinfo("Success", "User deleted successfully!")
                delete_user_window.destroy()
            else:
                messagebox.showerror(
                    "Error", "Failed to delete user. Username might not exist.")

        delete_user_window = tk.Toplevel()
        delete_user_window.title("Delete User")
        delete_user_window.geometry("500x300")
        delete_user_window.configure(bg=COLORS["light"])
        
        # Center the window
        delete_user_window.update_idletasks()
        width = delete_user_window.winfo_width()
        height = delete_user_window.winfo_height()
        x = (delete_user_window.winfo_screenwidth() // 2) - (width // 2)
        y = (delete_user_window.winfo_screenheight() // 2) - (height // 2)
        delete_user_window.geometry(f'{width}x{height}+{x}+{y}')

        # Create a frame for the form
        form_frame = tk.Frame(delete_user_window, bg=COLORS["light"], padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        create_styled_label(form_frame, "Delete User", FONTS["heading"]).pack(pady=(0, 20))
        create_styled_label(form_frame, "Warning: This action cannot be undone!", FONTS["normal"]).pack(pady=(0, 20))

        # Username field
        username_frame = tk.Frame(form_frame, bg=COLORS["light"])
        username_frame.pack(fill=tk.X, pady=5)
        create_styled_label(username_frame, "Username to delete:").pack(side=tk.LEFT, padx=(0, 10))
        username_entry = create_styled_entry(username_frame)
        username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Buttons
        button_frame = tk.Frame(form_frame, bg=COLORS["light"])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        create_styled_button(button_frame, "Delete", submit, COLORS["danger"]).pack(side=tk.RIGHT, padx=5)
        create_styled_button(button_frame, "Cancel", delete_user_window.destroy, COLORS["secondary"]).pack(side=tk.RIGHT, padx=5)

    admin_window = tk.Toplevel()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("600x500")
    admin_window.configure(bg=COLORS["light"])
    
    # Center the window
    admin_window.update_idletasks()
    width = admin_window.winfo_width()
    height = admin_window.winfo_height()
    x = (admin_window.winfo_screenwidth() // 2) - (width // 2)
    y = (admin_window.winfo_screenheight() // 2) - (height // 2)
    admin_window.geometry(f'{width}x{height}+{x}+{y}')

    # Create a header frame
    header_frame = tk.Frame(admin_window, bg=COLORS["primary"], height=100)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    create_styled_label(header_frame, f"Welcome, {user.full_name}!", FONTS["heading"]).pack(pady=20)
    create_styled_label(header_frame, "Admin Dashboard", FONTS["subheading"]).pack()

    # Create a content frame
    content_frame = tk.Frame(admin_window, bg=COLORS["light"], padx=20, pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create a card-like frame for each action
    card_frame = tk.Frame(content_frame, bg=COLORS["white"], padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
    card_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    create_styled_label(card_frame, "User Management", FONTS["subheading"]).pack(pady=(0, 20))
    
    # Buttons in a row
    button_frame = tk.Frame(card_frame, bg=COLORS["white"])
    button_frame.pack(fill=tk.X)
    
    create_styled_button(button_frame, "Add User", add_user_ui, COLORS["success"]).pack(side=tk.LEFT, padx=10)
    create_styled_button(button_frame, "Delete User", delete_user_ui, COLORS["danger"]).pack(side=tk.LEFT, padx=10)


def student_dashboard(user):
    """
    Student dashboard functionality.
    """
    def view_details():
        """
        View personal details, grades, and extracurricular activities.
        """
        grades = get_student_grades(user.username)
        eca = get_student_eca(user.username)

        details_window = tk.Toplevel()
        details_window.title("Student Details")
        details_window.geometry("600x500")
        details_window.configure(bg=COLORS["light"])
        
        # Center the window
        details_window.update_idletasks()
        width = details_window.winfo_width()
        height = details_window.winfo_height()
        x = (details_window.winfo_screenwidth() // 2) - (width // 2)
        y = (details_window.winfo_screenheight() // 2) - (height // 2)
        details_window.geometry(f'{width}x{height}+{x}+{y}')

        # Create a header frame
        header_frame = tk.Frame(details_window, bg=COLORS["primary"], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        create_styled_label(header_frame, "Student Details", FONTS["heading"]).pack(pady=20)

        # Create a content frame
        content_frame = tk.Frame(details_window, bg=COLORS["light"], padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Personal details card
        personal_card = tk.Frame(content_frame, bg=COLORS["white"], padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
        personal_card.pack(fill=tk.X, pady=10)
        
        create_styled_label(personal_card, "Personal Information", FONTS["subheading"]).pack(pady=(0, 10))
        create_styled_label(personal_card, f"Full Name: {user.full_name}").pack(anchor=tk.W)
        create_styled_label(personal_card, f"Username: {user.username}").pack(anchor=tk.W)
        create_styled_label(personal_card, f"Role: {user.role}").pack(anchor=tk.W)
        
        # Grades card
        grades_card = tk.Frame(content_frame, bg=COLORS["white"], padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
        grades_card.pack(fill=tk.X, pady=10)
        
        create_styled_label(grades_card, "Grades", FONTS["subheading"]).pack(pady=(0, 10))
        
        if grades:
            for i, grade in enumerate(grades, 1):
                create_styled_label(grades_card, f"Subject {i}: {grade}").pack(anchor=tk.W)
        else:
            create_styled_label(grades_card, "No grades found.").pack(anchor=tk.W)
        
        # ECA card
        eca_card = tk.Frame(content_frame, bg=COLORS["white"], padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
        eca_card.pack(fill=tk.X, pady=10)
        
        create_styled_label(eca_card, "Extracurricular Activities", FONTS["subheading"]).pack(pady=(0, 10))
        
        if eca:
            for activity in eca:
                create_styled_label(eca_card, f"• {activity}").pack(anchor=tk.W)
        else:
            create_styled_label(eca_card, "No extracurricular activities found.").pack(anchor=tk.W)
        
        # Close button
        create_styled_button(content_frame, "Close", details_window.destroy).pack(pady=10)

    def update_profile():
        """
        Update the student's profile information.
        """
        def submit():
            new_full_name = full_name_entry.get()
            if update_student_profile(user.username, new_full_name):
                messagebox.showinfo("Success", "Profile updated successfully!")
                update_window.destroy()
                # Update the user object
                user.full_name = new_full_name
            else:
                messagebox.showerror("Error", "Failed to update profile.")

        update_window = tk.Toplevel()
        update_window.title("Update Profile")
        update_window.geometry("500x300")
        update_window.configure(bg=COLORS["light"])
        
        # Center the window
        update_window.update_idletasks()
        width = update_window.winfo_width()
        height = update_window.winfo_height()
        x = (update_window.winfo_screenwidth() // 2) - (width // 2)
        y = (update_window.winfo_screenheight() // 2) - (height // 2)
        update_window.geometry(f'{width}x{height}+{x}+{y}')

        # Create a frame for the form
        form_frame = tk.Frame(update_window, bg=COLORS["light"], padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        create_styled_label(form_frame, "Update Profile", FONTS["heading"]).pack(pady=(0, 20))

        # Full Name field
        name_frame = tk.Frame(form_frame, bg=COLORS["light"])
        name_frame.pack(fill=tk.X, pady=5)
        create_styled_label(name_frame, "Full Name:").pack(side=tk.LEFT, padx=(0, 10))
        full_name_entry = create_styled_entry(name_frame)
        full_name_entry.insert(0, user.full_name)  # Pre-fill with current name
        full_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Buttons
        button_frame = tk.Frame(form_frame, bg=COLORS["light"])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        create_styled_button(button_frame, "Submit", submit, COLORS["success"]).pack(side=tk.RIGHT, padx=5)
        create_styled_button(button_frame, "Cancel", update_window.destroy, COLORS["secondary"]).pack(side=tk.RIGHT, padx=5)

    student_window = tk.Toplevel()
    student_window.title("Student Dashboard")
    student_window.geometry("600x500")
    student_window.configure(bg=COLORS["light"])
    
    # Center the window
    student_window.update_idletasks()
    width = student_window.winfo_width()
    height = student_window.winfo_height()
    x = (student_window.winfo_screenwidth() // 2) - (width // 2)
    y = (student_window.winfo_screenheight() // 2) - (height // 2)
    student_window.geometry(f'{width}x{height}+{x}+{y}')

    # Create a header frame
    header_frame = tk.Frame(student_window, bg=COLORS["primary"], height=100)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    create_styled_label(header_frame, f"Welcome, {user.full_name}!", FONTS["heading"]).pack(pady=20)
    create_styled_label(header_frame, "Student Dashboard", FONTS["subheading"]).pack()

    # Create a content frame
    content_frame = tk.Frame(student_window, bg=COLORS["light"], padx=20, pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create a card-like frame for each action
    card_frame = tk.Frame(content_frame, bg=COLORS["white"], padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
    card_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    create_styled_label(card_frame, "Student Options", FONTS["subheading"]).pack(pady=(0, 20))
    
    # Buttons in a row
    button_frame = tk.Frame(card_frame, bg=COLORS["white"])
    button_frame.pack(fill=tk.X)
    
    create_styled_button(button_frame, "View Details", view_details, COLORS["primary"]).pack(side=tk.LEFT, padx=10)
    create_styled_button(button_frame, "Update Profile", update_profile, COLORS["success"]).pack(side=tk.LEFT, padx=10)


def main():
    root = tk.Tk()
    root.title("Student Profile Management System")
    root.geometry("600x500")
    root.configure(bg=COLORS["light"])
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Create a header frame
    header_frame = tk.Frame(root, bg=COLORS["primary"], height=100)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    create_styled_label(header_frame, "Student Profile Management System", FONTS["heading"]).pack(pady=20)
    create_styled_label(header_frame, "Please login to continue", FONTS["subheading"]).pack()

    # Create a content frame
    content_frame = tk.Frame(root, bg=COLORS["light"], padx=20, pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create a card-like frame for login
    login_card = tk.Frame(content_frame, bg=COLORS["white"], padx=20, pady=20, relief=tk.RAISED, borderwidth=1)
    login_card.pack(fill=tk.BOTH, expand=True, pady=10)
    
    create_styled_label(login_card, "Login", FONTS["subheading"]).pack(pady=(0, 20))

    # Username field
    username_frame = tk.Frame(login_card, bg=COLORS["white"])
    username_frame.pack(fill=tk.X, pady=5)
    create_styled_label(username_frame, "Username:").pack(side=tk.LEFT, padx=(0, 10))
    global username_entry
    username_entry = create_styled_entry(username_frame)
    username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Password field
    password_frame = tk.Frame(login_card, bg=COLORS["white"])
    password_frame.pack(fill=tk.X, pady=5)
    create_styled_label(password_frame, "Password:").pack(side=tk.LEFT, padx=(0, 10))
    global password_entry
    password_entry = create_styled_entry(password_frame, show="*")
    password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Login button
    create_styled_button(login_card, "Login", login, COLORS["success"]).pack(pady=20)

    # Add a footer with instructions
    footer_frame = tk.Frame(root, bg=COLORS["light"], height=50)
    footer_frame.pack(fill=tk.X)
    footer_frame.pack_propagate(False)
    
    create_styled_label(footer_frame, "Demo credentials: admin/password or student1/studentpass", FONTS["small"]).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()