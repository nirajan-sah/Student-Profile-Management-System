"""
Importing all the libraries
"""
import pandas as pd
import numpy as np
import os

"""Get student profile information"""
def get_student_profile(username):
    """Get student profile information"""
    try:
        if not os.path.exists('data/users.csv'):
            print("Error: File not found")
            return None
            
        users_df = pd.read_csv('data/users.csv')
        if users_df.empty:
            print("Error: File is empty")
            return None
            
        student = users_df[users_df['username'] == username]
        if student.empty:
            print(f"Student with username '{username}' not found")
            return None
            
        # Convert numeric fields to appropriate types
        profile = student.iloc[0].to_dict()
        try:
            profile['level'] = float(profile['level'])
        except (ValueError, TypeError):
            profile['level'] = 0.0
            
        return profile
        
    except Exception as e:
        print(f"Error fetching student profile: {str(e)}")
        return None

def get_student_grades(username):
    """Fetch grades for a student from grades.csv."""
    if not username:
        return None
        
    try:            
        if not os.path.exists("data/grades.csv"):
            print("Error: File not found.")
            return None
            
        df = pd.read_csv("data/grades.csv")
        
        # Check if the student exists in the grades file
        if username not in df['username'].values:
            print(f"Student with username '{username}' not found in file")
            return []
            
        # Get the student's row
        student_row = df[df['username'] == username].iloc[0]
        
        # Convert to the expected format (list of dictionaries with subject and grade)
        grades = []
        for column in df.columns:
            if column != 'username':  # Skip the username column
                grade_value = student_row[column]
                if pd.notna(grade_value):  # Check if the grade is not NaN
                    grades.append({
                        'subject': column,
                        'grade': float(grade_value)
                    })
        
        return grades
            
    except Exception as e:
        print(f"Error getting student grades: {e}")
        return None

def get_student_eca(username):
    """Fetch extracurricular activities for a student from eca.csv."""
    if not username:
        return None
        
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists("data/eca.csv"):
            print("Error: eca.csv file not found.")
            return None
            
        df = pd.read_csv("data/eca.csv")
        user_eca = df[df['username'] == username]
        
        if not user_eca.empty:
            return user_eca.to_dict('records')
        return []
            
    except Exception as e:
        print(f"Error getting student ECA: {e}")
        return None

def update_student_profile(username, data):
    """Update the student's profile information in users.csv."""
    if not username or not data:
        print("Username and data are required")
        return False
        
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists("data/users.csv"):
            print("Error: users.csv file not found")
            return False
            
        df = pd.read_csv("data/users.csv")
        if df.empty:
            print("Error: users.csv is empty")
            return False
            
        if username not in df['username'].values:
            print(f"Student with username '{username}' not found")
            return False
            
        # Validate and convert data types
        if 'level' in data:
            try:
                data['level'] = float(data['level'])
                if not (0 <= data['level'] <= 4):
                    print("Level must be between 0 and 4")
                    return False
            except (ValueError, TypeError):
                print("Level must be a number")
                return False
                
        # Update the user's information
        for key, value in data.items():
            if key in df.columns:
                df.loc[df['username'] == username, key] = value
                
        # Save changes
        df.to_csv("data/users.csv", index=False)
        print("Profile updated successfully")
        return True
        
    except Exception as e:
        print(f"Error updating student profile: {e}")
        return False

def add_student_grade(username, subject, grade):
    """Add a new grade for a student."""
    try:
        # Validate inputs
        if not username or not subject:
            print("Username and subject are required")
            return False
            
        # Check if student exists
        if not os.path.exists("data/users.csv"):
            print("Users file not found")
            return False
            
        users_df = pd.read_csv("data/users.csv")
        if username not in users_df['username'].values:
            print(f"Student with username '{username}' not found")
            return False
            
        # Validate grade is numeric and between 0 and 100
        try:
            grade = float(grade)
            if not (0 <= grade <= 100):
                print("Grade must be between 0 and 100")
                return False
        except ValueError:
            print("Grade must be a number")
            return False
            
        # Create data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Create grades.csv if it doesn't exist
        if not os.path.exists("data/grades.csv"):
            # Create with username column and subject columns
            columns = ['username', 'Physics', 'Math', 'Chemistry', 'Biology', 'English']
            pd.DataFrame(columns=columns).to_csv("data/grades.csv", index=False)
            
        # Read existing grades
        df = pd.read_csv("data/grades.csv")
        
        # Check if the subject column exists, if not add it
        if subject not in df.columns:
            df[subject] = None
            
        # Check if student already exists in the grades file
        if username in df['username'].values:
            # Update the grade for the existing student
            df.loc[df['username'] == username, subject] = grade
        else:
            # Add a new row for the student
            new_row = pd.DataFrame({'username': [username]})
            # Set all subject columns to None initially
            for col in df.columns:
                if col != 'username':
                    new_row[col] = None
            # Set the grade for the specified subject
            new_row[subject] = grade
            # Append the new row to the dataframe
            df = pd.concat([df, new_row], ignore_index=True)
        
        # Save to CSV
        df.to_csv("data/grades.csv", index=False)
        print(f"Grade added successfully for {username} in {subject}")
        return True
        
    except Exception as e:
        print(f"Error adding student grade: {e}")
        return False

def add_student_eca(username, activity, role, hours_per_week, description=""):
    """Add a new extracurricular activity for a student."""
    try:
        # Validate required inputs
        if not username or not activity or not role:
            print("Username, activity, and role are required")
            return False
            
        # Check if student exists
        if not os.path.exists("data/users.csv"):
            print("Users file not found")
            return False
            
        users_df = pd.read_csv("data/users.csv")
        if username not in users_df['username'].values:
            print(f"Student with username '{username}' not found")
            return False
            
        # Validate hours_per_week is numeric and positive
        try:
            hours_per_week = float(hours_per_week)
            if hours_per_week < 0:
                print("Hours per week must be positive")
                return False
        except ValueError:
            print("Hours per week must be a number")
            return False
            
        # Create data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Create eca.csv if it doesn't exist
        if not os.path.exists("data/eca.csv"):
            pd.DataFrame(columns=['username', 'activity', 'role', 'hours_per_week', 'description']).to_csv("data/eca.csv", index=False)
            
        # Read existing ECA records
        df = pd.read_csv("data/eca.csv")
        
        # Check if activity already exists for this student
        existing_eca = df[
            (df['username'] == username) & 
            (df['activity'] == activity)
        ]
        
        if not existing_eca.empty:
            # Update existing ECA instead of creating a new one
            df.loc[(df['username'] == username) & (df['activity'] == activity), ['role', 'hours_per_week', 'description']] = [role, hours_per_week, description]
        else:
            # Create new ECA entry
            new_eca = pd.DataFrame({
                'username': [username],
                'activity': [activity],
                'role': [role],
                'hours_per_week': [hours_per_week],
                'description': [description]
            })
            # Add new ECA to dataframe
            df = pd.concat([df, new_eca], ignore_index=True)
        
        # Save to CSV
        df.to_csv("data/eca.csv", index=False)
        print(f"ECA added successfully for {username}: {activity}")
        return True
        
    except Exception as e:
        print(f"Error adding student ECA: {e}")
        return False 