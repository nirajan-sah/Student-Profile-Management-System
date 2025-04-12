import os
import pandas as pd
from student import get_student_grades, get_student_eca, update_student_profile


def authenticate(username, password):
    """Authenticate user credentials"""
    try:
            
        if not os.path.exists("data/passwords.csv"):
            print("Error: passwords.csv file not found")
            return None
            
        if not os.path.exists("data/users.csv"):
            print("Error: users.csv file not found")
            return None
            
        # Read passwords file
        passwords_df = pd.read_csv("data/passwords.csv")
        if passwords_df.empty:
            print("Error: passwords.csv is empty")
            return None
            
        # Read users file
        users_df = pd.read_csv("data/users.csv")
        if users_df.empty:
            print("Error: users.csv is empty")
            return None
            
        # Find user in passwords file
        user = passwords_df[
            (passwords_df['username'] == username) & 
            (passwords_df['password'] == password)
        ]
        
        if user.empty:
            print("Invalid username or password")
            return None
            
        # Get user role
        role = user.iloc[0]['role']
        if not role or role not in ['admin', 'student']:
            print("Invalid user role")
            return None
            
        # Verify user exists in users.csv
        if username not in users_df['username'].values:
            print("User not found in users.csv")
            return None
            
        return {
            'username': username,
            'role': role
        }
        
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return None


def get_user_details(username):
    """Fetch user details from users.csv based on the username."""
    if not username:
        return None
        
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists("data/users.csv"):
            print("Error: users.csv file not found.")
            return None
            
        df = pd.read_csv("data/users.csv")
        user_row = df[df['username'] == username]
        
        if not user_row.empty:
            return {
                'username': user_row.iloc[0]['username'],
                'full_name': user_row.iloc[0]['full_name'],
                'role': user_row.iloc[0]['role'],
                'email': user_row.iloc[0].get('email', ''),
                'phone': user_row.iloc[0].get('phone', ''),
                'address': user_row.iloc[0].get('address', ''),
                'department': user_row.iloc[0].get('department', ''),
                'year_of_study': user_row.iloc[0].get('year_of_study', '')
            }
            
    except Exception as e:
        print(f"Error getting user details: {e}")
    return None


def initialize_data_files():
    """Initialize data directory and required CSV files"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Initialize users.csv
        if not os.path.exists("data/users.csv"):
            pd.DataFrame(columns=['username', 'full_name', 'role', 'email', 'phone', 'address', 
                                'department', 'year_of_study', 'enrollment_date']).to_csv("data/users.csv", index=False)
            
        # Initialize passwords.csv
        if not os.path.exists("data/passwords.csv"):
            pd.DataFrame(columns=['username', 'password', 'role']).to_csv("data/passwords.csv", index=False)
            
        # Initialize grades.csv
        if not os.path.exists("data/grades.csv"):
            pd.DataFrame(columns=['username', 'subject', 'grade']).to_csv("data/grades.csv", index=False)
            
        # Initialize eca.csv
        if not os.path.exists("data/eca.csv"):
            pd.DataFrame(columns=['username', 'activity', 'role', 'hours']).to_csv("data/eca.csv", index=False)
            
        # Add default admin user if not exists
        passwords_df = pd.read_csv("data/passwords.csv")
        users_df = pd.read_csv("data/users.csv")
        
        if 'admin' not in passwords_df['username'].values:
            # Add admin to passwords.csv
            new_password = pd.DataFrame({
                'username': ['admin'],
                'password': ['password'],
                'role': ['admin']
            })
            passwords_df = pd.concat([passwords_df, new_password], ignore_index=True)
            passwords_df.to_csv("data/passwords.csv", index=False)
            
            # Add admin to users.csv
            new_user = pd.DataFrame({
                'username': ['admin'],
                'full_name': ['Administrator'],
                'role': ['admin'],
                'email': ['admin@example.com'],
                'phone': [''],
                'address': [''],
                'department': [''],
                'year_of_study': [''],
                'enrollment_date': [pd.Timestamp.now().strftime('%Y-%m-%d')]
            })
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_csv("data/users.csv", index=False)
            
    except Exception as e:
        print(f"Error initializing data files: {str(e)}")


if __name__ == "__main__":
    initialize_data_files()
    print("Data files initialized successfully!")
