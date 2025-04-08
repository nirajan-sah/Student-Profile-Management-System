import pandas as pd
import os

def add_user(username, full_name, password, role):
    """Add a new user to the system"""
    try:
        # Check if data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Check if users file exists
        if not os.path.exists("data/users.csv"):
            # Create new users file with headers
            pd.DataFrame(columns=['username', 'full_name', 'role', 'email', 'phone', 'address', 'department', 'year_of_study', 'enrollment_date']).to_csv('data/users.csv', index=False)
            
        users_df = pd.read_csv('data/users.csv')
        if not users_df.empty and username in users_df['username'].values:
            return False, "Username already exists"

        # Create default values for new user
        email = f"{username}@university.edu"
        phone = "0000000000"
        address = "Student Address"
        department = "General"
        year_of_study = 1
        enrollment_date = "2023-09-01"

        new_user = pd.DataFrame({
            'username': [username],
            'full_name': [full_name],
            'role': [role],
            'email': [email],
            'phone': [phone],
            'address': [address],
            'department': [department],
            'year_of_study': [year_of_study],
            'enrollment_date': [enrollment_date]
        })
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv('data/users.csv', index=False)
        
        # Also add to passwords.csv
        if not os.path.exists("data/passwords.csv"):
            pd.DataFrame(columns=['username', 'password', 'role']).to_csv('data/passwords.csv', index=False)
            
        passwords_df = pd.read_csv('data/passwords.csv')
        new_password = pd.DataFrame({
            'username': [username],
            'password': [password],
            'role': [role]
        })
        passwords_df = pd.concat([passwords_df, new_password], ignore_index=True)
        passwords_df.to_csv('data/passwords.csv', index=False)
        
        return True, "User added successfully"
    except Exception as e:
        return False, f"Error adding user: {str(e)}"

def delete_user(username):
    """Delete a user from the system"""
    try:
        # Delete from users.csv
        users_df = pd.read_csv('data/users.csv')
        if users_df.empty or username not in users_df['username'].values:
            return False, "User not found"
            
        users_df = users_df[users_df['username'] != username]
        users_df.to_csv('data/users.csv', index=False)
        
        # Delete from passwords.csv
        if os.path.exists('data/passwords.csv'):
            passwords_df = pd.read_csv('data/passwords.csv')
            passwords_df = passwords_df[passwords_df['username'] != username]
            passwords_df.to_csv('data/passwords.csv', index=False)
            
        # Delete from grades.csv
        if os.path.exists('data/grades.csv'):
            grades_df = pd.read_csv('data/grades.csv')
            grades_df = grades_df[grades_df['username'] != username]
            grades_df.to_csv('data/grades.csv', index=False)
            
        # Delete from eca.csv
        if os.path.exists('data/eca.csv'):
            eca_df = pd.read_csv('data/eca.csv')
            eca_df = eca_df[eca_df['username'] != username]
            eca_df.to_csv('data/eca.csv', index=False)
            
        return True, "User deleted successfully"
    except Exception as e:
        return False, f"Error deleting user: {str(e)}"

def modify_student_data(username, data):
    """Modify student data"""
    try:
        users_df = pd.read_csv('data/users.csv')
        if username not in users_df['username'].values:
            return False, "User not found"
            
        for key, value in data.items():
            if key in users_df.columns:
                users_df.loc[users_df['username'] == username, key] = value
                
        users_df.to_csv('data/users.csv', index=False)
        
        # Update password if provided
        if 'password' in data and os.path.exists('data/passwords.csv'):
            passwords_df = pd.read_csv('data/passwords.csv')
            passwords_df.loc[passwords_df['username'] == username, 'password'] = data['password']
            passwords_df.to_csv('data/passwords.csv', index=False)
            
        return True, "Student data updated successfully"
    except Exception as e:
        return False, f"Error updating student data: {str(e)}"

def get_all_students():
    """Get list of all students"""
    try:
        users_df = pd.read_csv('data/users.csv')
        # Filter only students
        students_df = users_df[users_df['role'] == 'student']
        return students_df.to_dict('records')
    except Exception as e:
        print(f"Error fetching students: {str(e)}")
        return []

def get_student_details(username):
    """Get detailed information about a specific student"""
    try:
        users_df = pd.read_csv('data/users.csv')
        student = users_df[users_df['username'] == username]
        if not student.empty:
            return student.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"Error fetching student details: {str(e)}")
        return None 