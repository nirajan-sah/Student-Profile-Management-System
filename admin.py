import pandas as pd
import os
import csv
from datetime import datetime

def add_user(username, full_name, password, role, email=None, phone=None, address=None, department=None, level=None):
    """Add a new user to the system"""
    try:
        # Input validation
        if not username or not full_name or not password or not role:
            return False, "Username, full name, password, and role are required"
        
        if role not in ['admin', 'student']:
            return False, "Role must be either 'admin' or 'student'"
        
        # Create data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")
        
        # Check if username already exists
        if os.path.exists("data/passwords.csv"):
            passwords_df = pd.read_csv("data/passwords.csv")
            if username in passwords_df['username'].values:
                return False, "Username already exists"
        
        # Add user to passwords.csv
        if not os.path.exists("data/passwords.csv"):
            with open("data/passwords.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'password', 'role'])
        
        with open("data/passwords.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, password, role])
        
        # Add user to users.csv
        if not os.path.exists("data/users.csv"):
            with open("data/users.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'full_name', 'email', 'phone', 'address', 'department', 'level', 'created_at'])
        
        with open("data/users.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, full_name, email, phone, address, department, level, datetime.now()])
        
        return True, "User added successfully"
    except Exception as e:
        return False, f"Error adding user: {str(e)}"

def remove_user(username):
    """Remove a user from the system"""
    try:
        # Input validation
        if not username:
            return False, "Username is required"
        
        # Check if user exists
        if not os.path.exists("data/users.csv"):
            return False, "User database not found"
        
        users_df = pd.read_csv("data/users.csv")
        if username not in users_df['username'].values:
            return False, "User not found"
        
        # Remove from passwords.csv
        if os.path.exists("data/passwords.csv"):
            passwords_df = pd.read_csv("data/passwords.csv")
            passwords_df = passwords_df[passwords_df['username'] != username]
            passwords_df.to_csv("data/passwords.csv", index=False)
        
        # Remove from users.csv
        users_df = users_df[users_df['username'] != username]
        users_df.to_csv("data/users.csv", index=False)
        
        # Remove from grades.csv
        if os.path.exists("data/grades.csv"):
            grades_df = pd.read_csv("data/grades.csv")
            grades_df = grades_df[grades_df['username'] != username]
            grades_df.to_csv("data/grades.csv", index=False)
        
        # Remove from eca.csv
        if os.path.exists("data/eca.csv"):
            eca_df = pd.read_csv("data/eca.csv")
            eca_df = eca_df[eca_df['username'] != username]
            eca_df.to_csv("data/eca.csv", index=False)
        
        return True, "User removed successfully"
    except Exception as e:
        return False, f"Error removing user: {str(e)}"

def list_all_users():
    """List all users in the system"""
    try:
        if not os.path.exists("data/users.csv"):
            return []
        
        users_df = pd.read_csv("data/users.csv")
        if users_df.empty:
            return []
            
        return users_df.to_dict('records')
    except Exception as e:
        print(f"Error listing users: {str(e)}")
        return []

def get_user_details(username):
    """Get detailed information about a user"""
    try:
        # Input validation
        if not username:
            return None
        
        if not os.path.exists("data/users.csv"):
            return None
        
        users_df = pd.read_csv("data/users.csv")
        if users_df.empty:
            return None
            
        user = users_df[users_df['username'] == username]
        
        if user.empty:
            return None
        
        return user.iloc[0].to_dict()
    except Exception as e:
        print(f"Error getting user details: {str(e)}")
        return None

def update_user(username, data):
    """Update user information."""
    try:
        if not os.path.exists("data/users.csv"):
            return False
            
        users_df = pd.read_csv("data/users.csv")
        if username not in users_df['username'].values:
            return False
            
        for key, value in data.items():
            if key in users_df.columns:
                users_df.loc[users_df['username'] == username, key] = value
                
        users_df.to_csv("data/users.csv", index=False)
        return True
        
    except Exception as e:
        print(f"Error updating user: {e}")
        return False

def modify_student_data(username, data):
    """Modify student data"""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if not os.path.exists('data/users.csv'):
            return False, "Users file not found"
            
        users_df = pd.read_csv('data/users.csv')
        if users_df.empty:
            return False, "Users file is empty"
            
        if username not in users_df['username'].values:
            return False, "User not found"
            
        # Validate and convert data types
        if 'level' in data:
            try:
                data['level'] = float(data['level'])
                if not (0 <= data['level'] <= 4):
                    return False, "Level must be between 0 and 4"
            except (ValueError, TypeError):
                return False, "Level must be a number"
                
        # Update user information
        for key, value in data.items():
            if key in users_df.columns:
                users_df.loc[users_df['username'] == username, key] = value
                
        users_df.to_csv('data/users.csv', index=False)
        
        # Update password if provided
        if 'password' in data:
            if not os.path.exists('data/passwords.csv'):
                return False, "Passwords file not found"
                
            passwords_df = pd.read_csv('data/passwords.csv')
            if passwords_df.empty:
                return False, "Passwords file is empty"
                
            if username not in passwords_df['username'].values:
                return False, "User not found in passwords file"
                
            passwords_df.loc[passwords_df['username'] == username, 'password'] = data['password']
            passwords_df.to_csv('data/passwords.csv', index=False)
            
        return True, "Student data updated successfully"
        
    except Exception as e:
        return False, f"Error updating student data: {str(e)}"
    
def update_student_profile(username, data):
    """Update student profile information"""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if not os.path.exists('data/users.csv'):
            return False, "Users file not found"
            
        users_df = pd.read_csv('data/users.csv')
        if username not in users_df['username'].values:
            return False, "User not found"
            
        for key, value in data.items():
            if key in users_df.columns:
                users_df.loc[users_df['username'] == username, key] = value
                
        users_df.to_csv('data/users.csv', index=False)
        return True, "Profile updated successfully"
    except Exception as e:
        return False, f"Error updating profile: {str(e)}"

def update_student_grades(username, grades_data):
    """Update student grades using pandas for efficient data manipulation"""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if not os.path.exists('data/grades.csv'):
            # Create with username column and subject columns
            columns = ['username', 'Physics', 'Math', 'Chemistry', 'Biology', 'English']
            pd.DataFrame(columns=columns).to_csv('data/grades.csv', index=False)
            
        # Validate student exists
        if not os.path.exists('data/users.csv'):
            return False, "Users file not found"
            
        users_df = pd.read_csv('data/users.csv')
        if username not in users_df['username'].values:
            return False, "Student not found"
            
        grades_df = pd.read_csv('data/grades.csv')
        
        # Check if student already exists in the grades file
        if username in grades_df['username'].values:
            # Update grades for the existing student
            for subject, data in grades_data.items():
                try:
                    grade = float(data.get('grade', 0))
                    if not (0 <= grade <= 100):
                        return False, f"Invalid grade for {subject}: must be between 0 and 100"
                    
                    # Check if the subject column exists, if not add it
                    if subject not in grades_df.columns:
                        grades_df[subject] = None
                    
                    # Update the grade
                    grades_df.loc[grades_df['username'] == username, subject] = grade
                    
                except (ValueError, TypeError) as e:
                    return False, f"Invalid data for {subject}: {str(e)}"
        else:
            # Add a new row for the student
            new_row = pd.DataFrame({'username': [username]})
            
            # Set all subject columns to None initially
            for col in grades_df.columns:
                if col != 'username':
                    new_row[col] = None
            
            # Add the new row to the dataframe
            grades_df = pd.concat([grades_df, new_row], ignore_index=True)
            
            # Update grades for the new student
            for subject, data in grades_data.items():
                try:
                    grade = float(data.get('grade', 0))
                    if not (0 <= grade <= 100):
                        return False, f"Invalid grade for {subject}: must be between 0 and 100"
                    
                    # Check if the subject column exists, if not add it
                    if subject not in grades_df.columns:
                        grades_df[subject] = None
                    
                    # Update the grade
                    grades_df.loc[grades_df['username'] == username, subject] = grade
                    
                except (ValueError, TypeError) as e:
                    return False, f"Invalid data for {subject}: {str(e)}"
        
        # Save to CSV
        grades_df.to_csv('data/grades.csv', index=False)
        return True, "Grades updated successfully"
        
    except Exception as e:
        return False, f"Error updating grades: {str(e)}"
    
def update_student_eca(username, eca_data):
    """Update student extracurricular activities using pandas"""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if not os.path.exists('data/eca.csv'):
            pd.DataFrame(columns=['username', 'activity', 'role', 'hours_per_week', 'description']).to_csv('data/eca.csv', index=False)
            
        eca_df = pd.read_csv('data/eca.csv')
        
        # Remove existing ECA for this student
        eca_df = eca_df[eca_df['username'] != username]
        
        # Create new ECA DataFrame using pandas
        new_eca = pd.DataFrame([
            {
                'username': username,
                'activity': activity,
                'role': data.get('role', ''),
                'hours_per_week': data.get('hours_per_week', 0),
                'description': data.get('description', '')
            }
            for activity, data in eca_data.items()
        ])
        
        # Concatenate and save
        eca_df = pd.concat([eca_df, new_eca], ignore_index=True)
        eca_df.to_csv('data/eca.csv', index=False)
        return True, "ECA updated successfully"
    except Exception as e:
        return False, f"Error updating ECA: {str(e)}"

def get_all_students():
    """Get all users"""
    try:
        if not os.path.exists('data/users.csv'):
            return []
            
        users_df = pd.read_csv('data/users.csv')
        return users_df.to_dict('records')
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return []

def get_student_details(username):
    """Get detailed student information"""
    try:
        if not os.path.exists('data/users.csv'):
            return None
            
        users_df = pd.read_csv('data/users.csv')
        student = users_df[users_df['username'] == username]
        
        if student.empty:
            return None
            
        student_data = student.iloc[0].to_dict()
        
        # Get grades if they exist
        if os.path.exists('data/grades.csv'):
            grades_df = pd.read_csv('data/grades.csv')
            
            # Check if the student exists in the grades file
            if username in grades_df['username'].values:
                # Get the student's row
                student_row = grades_df[grades_df['username'] == username].iloc[0]
                
                # Convert to the expected format (list of dictionaries with subject and grade)
                grades = []
                for column in grades_df.columns:
                    if column != 'username':  # Skip the username column
                        grade_value = student_row[column]
                        if pd.notna(grade_value):  # Check if the grade is not NaN
                            grades.append({
                                'subject': column,
                                'grade': float(grade_value)
                            })
                
                student_data['grades'] = grades
            
        # Get ECA if they exist
        if os.path.exists('data/eca.csv'):
            eca_df = pd.read_csv('data/eca.csv')
            student_eca = eca_df[eca_df['username'] == username]
            student_data['eca'] = student_eca.to_dict('records')
            
        return student_data
    except Exception as e:
        print(f"Error fetching student details: {str(e)}")
        return None 