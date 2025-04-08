import os
import csv
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from ui_components import COLORS, FONTS, create_button, create_label, create_entry, create_frame
from admin_view import AdminView
from student_view import StudentView
from user_view import UserView


class User:
    def __init__(self, username, full_name, role):
        self.username = username
        self.full_name = full_name
        self.role = role


def authenticate(username, password):
    """Authenticate user credentials"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists("data/passwords.csv"):
            return None
            
        passwords_df = pd.read_csv("data/passwords.csv")
        user = passwords_df[
            (passwords_df['username'] == username) & 
            (passwords_df['password'] == password)
        ]
        
        if not user.empty:
            return {
                'username': user.iloc[0]['username'],
                'role': user.iloc[0]['role']
            }
        return None
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return None


def get_user_details(username):
    """
    Fetch user details from users.csv based on the username.
    Returns a User object if found, otherwise None.
    """
    if not username:
        return None
        
    try:
        # Check if the data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Check if the users file exists
        if not os.path.exists("data/users.csv"):
            print("Error: users.csv file not found.")
            return None
            
        # Read the CSV file
        df = pd.read_csv("data/users.csv")
        
        # Find the user
        user_row = df[df['username'] == username]
        if not user_row.empty:
            return {
                'username': user_row.iloc[0]['username'],
                'full_name': user_row.iloc[0]['full_name'],
                'role': user_row.iloc[0]['role'],
                'user_id': user_row.iloc[0]['username']  # Using username as user_id for simplicity
            }
            
    except Exception as e:
        print(f"Error getting user details: {e}")
    return None


def login_window():
    """Create and show login window"""
    root = tk.Tk()
    root.title("Student Profile Management System - Login")
    root.geometry("400x300")
    
    main_frame = create_frame(root)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    create_label(main_frame, "Login", font=('Arial', 16, 'bold')).pack(pady=10)
    
    username_frame = create_frame(main_frame)
    username_frame.pack(fill='x', pady=5)
    create_label(username_frame, "Username:").pack(side='left')
    username_entry = create_entry(username_frame)
    username_entry.pack(side='right', expand=True, fill='x', padx=5)
    
    password_frame = create_frame(main_frame)
    password_frame.pack(fill='x', pady=5)
    create_label(password_frame, "Password:").pack(side='left')
    password_entry = create_entry(password_frame, show="*")
    password_entry.pack(side='right', expand=True, fill='x', padx=5)
    
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        user = authenticate(username, password)
        if user:
            root.destroy()
            if user['role'] == 'admin':
                AdminView(user)
            elif user['role'] == 'student':
                StudentView(user)
            else:
                UserView(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    create_button(main_frame, "Login", handle_login).pack(pady=20)
    
    root.mainloop()


def get_student_grades(username):
    """
    Fetch grades for a student from grades.csv.
    Returns a list of grades if found, otherwise None.
    """
    if not username:
        return None
        
    try:
        # Check if the data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Check if the grades file exists
        if not os.path.exists("data/grades.csv"):
            print("Error: grades.csv file not found.")
            return None
            
        # Read the CSV file
        df = pd.read_csv("data/grades.csv")
        
        # Find the user
        user_row = df[df['username'] == username]
        if not user_row.empty:
            # Get all grade columns
            grades = []
            for i in range(1, 6):  # grade1 to grade5
                grade_col = f'grade{i}'
                if grade_col in user_row.columns and pd.notna(user_row[grade_col].iloc[0]):
                    grades.append({
                        'subject': f'Subject {i}',
                        'grade': str(user_row[grade_col].iloc[0]),
                        'credits': 3  # Assuming 3 credits per subject
                    })
            return grades
            
    except Exception as e:
        print(f"Error getting student grades: {e}")
    return None


def get_student_eca(username):
    """
    Fetch extracurricular activities for a student from eca.csv.
    Returns a list of activities if found, otherwise None.
    """
    if not username:
        return None
        
    try:
        # Check if the data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Check if the eca file exists
        if not os.path.exists("data/eca.csv"):
            print("Error: eca.csv file not found.")
            return None
            
        # Read the CSV file
        df = pd.read_csv("data/eca.csv")
        
        # Find the user
        user_row = df[df['username'] == username]
        if not user_row.empty:
            # Get all activity columns
            activities = []
            for i in range(1, 4):  # activity1 to activity3
                activity_col = f'activity{i}'
                if activity_col in user_row.columns and pd.notna(user_row[activity_col].iloc[0]):
                    activities.append({
                        'activity': user_row[activity_col].iloc[0],
                        'hours': 10  # Assuming 10 hours per activity
                    })
            return activities
            
    except Exception as e:
        print(f"Error getting student ECA: {e}")
    return None


def update_student_profile(username, full_name):
    """
    Update the student's profile information in users.csv.
    """
    if not username or not full_name:
        return False
        
    try:
        # Check if the data directory exists
        if not os.path.exists("data"):
            return False
            
        # Check if the users file exists
        if not os.path.exists("data/users.csv"):
            return False
            
        # Read the CSV file
        df = pd.read_csv("data/users.csv")
        
        # Check if the user exists
        if df.empty or username not in df['username'].values:
            return False
            
        # Update the user's full name
        df.loc[df['username'] == username, 'full_name'] = full_name
        df.to_csv("data/users.csv", index=False)
        
        return True
    except Exception as e:
        print(f"Error updating student profile: {e}")
        return False


if __name__ == "__main__":
    login_window()
