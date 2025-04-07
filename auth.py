import os
import csv
import pandas as pd


class User:
    def __init__(self, username, full_name, role):
        self.username = username
        self.full_name = full_name
        self.role = role


def authenticate(username, password):
    """
    Authenticate the user by checking the credentials in passwords.csv.
    Returns a User object if valid, otherwise None.
    """
    if not username or not password:
        return None
        
    try:
        # Check if the data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Check if the passwords file exists
        if not os.path.exists("data/passwords.csv"):
            print("Error: passwords.csv file not found.")
            return None
            
        # Read the CSV file
        df = pd.read_csv("data/passwords.csv")
        
        # Find the user
        user_row = df[df['username'] == username]
        if not user_row.empty and user_row.iloc[0]['password'] == password:
            # Get user details
            user_details = get_user_details(username)
            if user_details:
                return user_details
            
    except Exception as e:
        print(f"Error during authentication: {e}")
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
            return User(
                username=user_row.iloc[0]['username'],
                full_name=user_row.iloc[0]['full_name'],
                role=user_row.iloc[0]['role']
            )
            
    except Exception as e:
        print(f"Error getting user details: {e}")
    return None


def add_user(username, full_name, password, role):
    """
    Add a new user to users.csv and passwords.csv.
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

'''
enter and update grades for student
3 in one class
'''

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
                    grades.append(str(user_row[grade_col].iloc[0]))
            return grades
            
    except Exception as e:
        print(f"Error getting student grades: {e}")
    return None

'''
enter and update eca for student
3 in one
'''

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
                    activities.append(user_row[activity_col].iloc[0])
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
