import os
import pandas as pd
from auth import User, get_user_details, add_user, delete_user, update_student_profile
import tkinter as tk
from tkinter import messagebox, ttk
from ui_components import (
    COLORS, FONTS, create_styled_button, create_styled_label,
    create_styled_entry, create_styled_frame, create_styled_combobox
)

def add_user_ui(user, on_success=None):
    """
    UI for adding a new user.
    """
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
            if on_success:
                on_success()
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

def delete_user_ui(user, on_success=None):
    """
    UI for deleting a user.
    """
    def submit():
        username_to_delete = username_entry.get()
        if not username_to_delete:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        if delete_user(username_to_delete):
            messagebox.showinfo("Success", "User deleted successfully!")
            delete_user_window.destroy()
            if on_success:
                on_success()
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

def add_user(username, full_name, password, role):
    """
    Add a new user to users.csv and passwords.csv.
    Returns True if successful, False otherwise.
    """
    if not username or not full_name or not password or not role:
        return False
        
    try:
        # Check if the data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Check if the users file exists, create it if not
        if not os.path.exists("data/users.csv"):
            pd.DataFrame(columns=['username', 'full_name', 'role']).to_csv("data/users.csv", index=False)
                
        # Check if the passwords file exists, create it if not
        if not os.path.exists("data/passwords.csv"):
            pd.DataFrame(columns=['username', 'password', 'role']).to_csv("data/passwords.csv", index=False)
                
        # Check if the username already exists
        users_df = pd.read_csv("data/users.csv")
        if not users_df.empty and username in users_df['username'].values:
            return False  # Username already exists

        # Add the user to users.csv
        new_user = pd.DataFrame({
            'username': [username],
            'full_name': [full_name],
            'role': [role]
        })
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv("data/users.csv", index=False)

        # Add the user to passwords.csv
        passwords_df = pd.read_csv("data/passwords.csv")
        new_password = pd.DataFrame({
            'username': [username],
            'password': [password],
            'role': [role]
        })
        passwords_df = pd.concat([passwords_df, new_password], ignore_index=True)
        passwords_df.to_csv("data/passwords.csv", index=False)

        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

def delete_user(username):
    """
    Delete a user from users.csv and passwords.csv.
    Returns True if successful, False otherwise.
    """
    if not username:
        return False
        
    try:
        # Check if the data directory exists
        if not os.path.exists("data"):
            return False
            
        # Check if the users file exists
        if not os.path.exists("data/users.csv"):
            return False
            
        # Check if the passwords file exists
        if not os.path.exists("data/passwords.csv"):
            return False
            
        # Remove the user from users.csv
        users_df = pd.read_csv("data/users.csv")
        if not users_df.empty:
            users_df = users_df[users_df['username'] != username]
            users_df.to_csv("data/users.csv", index=False)

        # Remove the user from passwords.csv
        passwords_df = pd.read_csv("data/passwords.csv")
        if not passwords_df.empty:
            passwords_df = passwords_df[passwords_df['username'] != username]
            passwords_df.to_csv("data/passwords.csv", index=False)

        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False 