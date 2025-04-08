import pandas as pd
import os

def get_student_grades(username):
    """Get grades for a specific student"""
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
        return None
    except Exception as e:
        print(f"Error getting student grades: {e}")
        return None

def get_student_eca(username):
    """Get ECA activities for a specific student"""
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
        return None
    except Exception as e:
        print(f"Error getting student ECA: {e}")
        return None

def update_student_profile(username, data):
    """Update student profile information"""
    try:
        # Check if the data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Check if the users file exists
        if not os.path.exists("data/users.csv"):
            print("Error: users.csv file not found.")
            return False, "Users file not found"
            
        # Read the CSV file
        df = pd.read_csv("data/users.csv")
        
        # Check if the user exists
        if df.empty or username not in df['username'].values:
            return False, "User not found"
            
        # Update the user's information
        for key, value in data.items():
            if key in df.columns:
                df.loc[df['username'] == username, key] = value
                
        # Save the updated data
        df.to_csv("data/users.csv", index=False)
        return True, "Profile updated successfully"
    except Exception as e:
        return False, f"Error updating profile: {str(e)}"

def get_student_profile(username):
    """Get student profile information"""
    try:
        users_df = pd.read_csv('data/users.csv')
        student = users_df[users_df['username'] == username]
        if not student.empty:
            return student.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"Error fetching student profile: {str(e)}")
        return None

def calculate_gpa(grades):
    """Calculate GPA from grades"""
    if not grades:
        return 0.0
        
    grade_points = {
        'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'F': 0.0
    }
    
    total_points = 0
    total_credits = 0
    
    for grade in grades:
        if grade['grade'] in grade_points:
            total_points += grade_points[grade['grade']] * grade['credits']
            total_credits += grade['credits']
            
    return total_points / total_credits if total_credits > 0 else 0.0

def get_student_grades(username):
    """Get student grades"""
    try:
        if not os.path.exists('data/grades.csv'):
            return []
            
        grades_df = pd.read_csv('data/grades.csv')
        student_grades = grades_df[grades_df['username'] == username]
        return student_grades.to_dict('records')
    except Exception as e:
        print(f"Error fetching grades: {str(e)}")
        return []

def update_student_grades(username, grades_data):
    """Update student grades"""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if not os.path.exists('data/grades.csv'):
            pd.DataFrame(columns=['username', 'subject', 'grade']).to_csv('data/grades.csv', index=False)
            
        grades_df = pd.read_csv('data/grades.csv')
        
        # Remove existing grades for this student
        grades_df = grades_df[grades_df['username'] != username]
        
        # Add new grades
        for subject, grade in grades_data.items():
            new_grade = pd.DataFrame({
                'username': [username],
                'subject': [subject],
                'grade': [grade]
            })
            grades_df = pd.concat([grades_df, new_grade], ignore_index=True)
            
        grades_df.to_csv('data/grades.csv', index=False)
        return True, "Grades updated successfully"
    except Exception as e:
        return False, f"Error updating grades: {str(e)}"

def get_student_eca(username):
    """Get student extracurricular activities"""
    try:
        if not os.path.exists('data/eca.csv'):
            return []
            
        eca_df = pd.read_csv('data/eca.csv')
        student_eca = eca_df[eca_df['username'] == username]
        return student_eca.to_dict('records')
    except Exception as e:
        print(f"Error fetching ECA: {str(e)}")
        return []

def update_student_eca(username, eca_data):
    """Update student extracurricular activities"""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if not os.path.exists('data/eca.csv'):
            pd.DataFrame(columns=['username', 'activity', 'role', 'hours']).to_csv('data/eca.csv', index=False)
            
        eca_df = pd.read_csv('data/eca.csv')
        
        # Remove existing ECA for this student
        eca_df = eca_df[eca_df['username'] != username]
        
        # Add new ECA
        for activity, details in eca_data.items():
            new_eca = pd.DataFrame({
                'username': [username],
                'activity': [activity],
                'role': [details.get('role', '')],
                'hours': [details.get('hours', 0)]
            })
            eca_df = pd.concat([eca_df, new_eca], ignore_index=True)
            
        eca_df.to_csv('data/eca.csv', index=False)
        return True, "ECA updated successfully"
    except Exception as e:
        return False, f"Error updating ECA: {str(e)}" 