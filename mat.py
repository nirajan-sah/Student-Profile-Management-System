import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def create_grades_chart(grades):
    """Create a bar chart for student grades"""
    try:
        if not grades:
            return None
            
        # Extract subjects and grades
        subjects = [grade['subject'] for grade in grades]
        grade_values = [float(grade['grade']) for grade in grades]
        
        # Create the bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(subjects, grade_values, color='skyblue')
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')
            
        # Customize the chart
        plt.title('Student Grades by Subject', fontsize=14, pad=20)
        plt.xlabel('Subjects', fontsize=12)
        plt.ylabel('Grade', fontsize=12)
        plt.ylim(0, 100)  # Set y-axis from 0 to 100
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the chart
        if not os.path.exists("data/charts"):
            os.makedirs("data/charts")
        plt.savefig("data/charts/grades_chart.png")
        plt.close()
        
        return "data/charts/grades_chart.png"
    except Exception as e:
        print(f"Error creating grades chart: {e}")
        return None

def create_eca_chart(eca):
    """Create a pie chart for student ECA activities"""
    try:
        if not eca:
            return None
            
        # Extract activities and hours
        activities = [activity['activity'] for activity in eca]
        hours = [float(activity['hours_per_week']) for activity in eca]
        
        # Create the pie chart
        plt.figure(figsize=(10, 8))
        plt.pie(hours, labels=activities, autopct='%1.1f%%',
                startangle=90, colors=plt.cm.Pastel1(np.linspace(0, 1, len(activities))))
        
        # Add a title
        plt.title('Distribution of ECA Hours', fontsize=14, pad=20)
        
        # Add a legend
        plt.legend(activities, title="Activities", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Make the pie chart circular
        plt.axis('equal')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the chart
        if not os.path.exists("data/charts"):
            os.makedirs("data/charts")
        plt.savefig("data/charts/eca_chart.png", bbox_inches='tight')
        plt.close()
        
        return "data/charts/eca_chart.png"
    except Exception as e:
        print(f"Error creating ECA chart: {e}")
        return None

def create_performance_summary(grades, eca):
    """Create a summary of student performance"""
    try:
        if not grades or not eca:
            return None
            
        # Create a figure with subplots
        fig = plt.figure(figsize=(15, 8))
        
        # Add a title
        fig.suptitle('Student Performance Summary', fontsize=16, y=0.95)
        
        # Create subplots
        gs = fig.add_gridspec(1, 2)
        
        # Grades subplot
        ax1 = fig.add_subplot(gs[0, 0])
        subjects = [grade['subject'] for grade in grades]
        grade_values = [float(grade['grade']) for grade in grades]
        bars = ax1.bar(subjects, grade_values, color='skyblue')
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')
        ax1.set_title('Grades by Subject')
        ax1.set_xlabel('Subjects')
        ax1.set_ylabel('Grade')
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # ECA subplot
        ax2 = fig.add_subplot(gs[0, 1])
        activities = [activity['activity'] for activity in eca]
        hours = [float(activity['hours_per_week']) for activity in eca]
        ax2.pie(hours, labels=activities, autopct='%1.1f%%',
                startangle=90, colors=plt.cm.Pastel1(np.linspace(0, 1, len(activities))))
        ax2.set_title('Distribution of ECA Hours')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the chart
        if not os.path.exists("data/charts"):
            os.makedirs("data/charts")
        plt.savefig("data/charts/performance_summary.png")
        plt.close()
        
        return "data/charts/performance_summary.png"
    except Exception as e:
        print(f"Error creating performance summary: {e}")
        return None

def calculate_gpa(username):
    """Calculate GPA for a student based on their grades."""
    try:
        if not os.path.exists("data/grades.csv"):
            return None
            
        grades_df = pd.read_csv("data/grades.csv")
        student_grades = grades_df[grades_df['username'] == username]
        
        if student_grades.empty:
            return None
            
        # Convert grades to numeric values
        grades = pd.to_numeric(student_grades['grade'], errors='coerce')
        
        # Calculate GPA (assuming 4.0 scale)
        gpa = grades.mean() / 25  # Converting percentage to 4.0 scale
        
        return round(gpa, 2)
        
    except Exception as e:
        print(f"Error calculating GPA: {e}")
        return None

def calculate_semester_gpa(username, semester):
    """Calculate GPA for a specific semester."""
    try:
        if not os.path.exists("data/grades.csv"):
            return None
            
        grades_df = pd.read_csv("data/grades.csv")
        student_grades = grades_df[
            (grades_df['username'] == username) & 
            (grades_df['semester'] == semester)
        ]
        
        if student_grades.empty:
            return None
            
        # Convert grades to numeric values
        grades = pd.to_numeric(student_grades['grade'], errors='coerce')
        
        # Calculate GPA (assuming 4.0 scale)
        gpa = grades.mean() / 25  # Converting percentage to 4.0 scale
        
        return round(gpa, 2)
        
    except Exception as e:
        print(f"Error calculating semester GPA: {e}")
        return None

def calculate_level_gpa(username, level):
    """Calculate GPA for a specific level."""
    try:
        if not os.path.exists("data/grades.csv"):
            return None
            
        grades_df = pd.read_csv("data/grades.csv")
        student_grades = grades_df[
            (grades_df['username'] == username) & 
            (grades_df['level'] == level)
        ]
        
        if student_grades.empty:
            return None
            
        # Convert grades to numeric values
        grades = pd.to_numeric(student_grades['grade'], errors='coerce')
        
        # Calculate GPA (assuming 4.0 scale)
        gpa = grades.mean() / 25  # Converting percentage to 4.0 scale
        
        return round(gpa, 2)
        
    except Exception as e:
        print(f"Error calculating level GPA: {e}")
        return None

def get_grade_statistics(username):
    """Get statistical information about a student's grades."""
    try:
        if not os.path.exists("data/grades.csv"):
            return None
            
        grades_df = pd.read_csv("data/grades.csv")
        student_grades = grades_df[grades_df['username'] == username]
        
        if student_grades.empty:
            return None
            
        # Convert grades to numeric values
        grades = pd.to_numeric(student_grades['grade'], errors='coerce')
        
        stats = {
            'mean': round(grades.mean(), 2),
            'median': round(grades.median(), 2),
            'min': round(grades.min(), 2),
            'max': round(grades.max(), 2),
            'std_dev': round(grades.std(), 2)
        }
        
        return stats
        
    except Exception as e:
        print(f"Error calculating grade statistics: {e}")
        return None

def get_subject_performance(username, subject):
    """Get performance information for a specific subject."""
    try:
        if not os.path.exists("data/grades.csv"):
            return None
            
        grades_df = pd.read_csv("data/grades.csv")
        subject_grades = grades_df[
            (grades_df['username'] == username) & 
            (grades_df['subject'] == subject)
        ]
        
        if subject_grades.empty:
            return None
            
        grade = float(subject_grades.iloc[0]['grade'])
        
        performance = {
            'subject': subject,
            'grade': grade,
            'status': 'Pass' if grade >= 40 else 'Fail'
        }
        
        return performance
        
    except Exception as e:
        print(f"Error getting subject performance: {e}")
        return None

def get_semester_performance(username, semester):
    """Get performance statistics for a specific semester."""
    try:
        if not os.path.exists("data/grades.csv"):
            return None
            
        grades_df = pd.read_csv("data/grades.csv")
        semester_grades = grades_df[
            (grades_df['username'] == username) & 
            (grades_df['semester'] == semester)
        ]
        
        if semester_grades.empty:
            return None
            
        # Convert grades to numeric values
        grades = pd.to_numeric(semester_grades['grade'], errors='coerce')
        
        performance = {
            'semester': semester,
            'subjects': semester_grades['subject'].tolist(),
            'grades': grades.tolist(),
            'levels': semester_grades['level'].tolist(),
            'average': round(grades.mean(), 2),
            'highest': round(grades.max(), 2),
            'lowest': round(grades.min(), 2)
        }
        
        return performance
        
    except Exception as e:
        print(f"Error calculating semester performance: {e}")
        return None

def get_level_performance(username, level):
    """Get performance statistics for a specific level."""
    try:
        if not os.path.exists("data/grades.csv"):
            return None
            
        grades_df = pd.read_csv("data/grades.csv")
        level_grades = grades_df[
            (grades_df['username'] == username) & 
            (grades_df['level'] == level)
        ]
        
        if level_grades.empty:
            return None
            
        # Convert grades to numeric values
        grades = pd.to_numeric(level_grades['grade'], errors='coerce')
        
        performance = {
            'level': level,
            'subjects': level_grades['subject'].tolist(),
            'grades': grades.tolist(),
            'semesters': level_grades['semester'].tolist(),
            'average': round(grades.mean(), 2),
            'highest': round(grades.max(), 2),
            'lowest': round(grades.min(), 2)
        }
        
        return performance
        
    except Exception as e:
        print(f"Error calculating level performance: {e}")
        return None

def get_eca_summary(username):
    """Get summary of student's extracurricular activities."""
    try:
        if not os.path.exists("data/eca.csv"):
            return None
            
        eca_df = pd.read_csv("data/eca.csv")
        student_eca = eca_df[eca_df['username'] == username]
        
        if student_eca.empty:
            return None
            
        # Calculate total hours
        total_hours = student_eca['hours_per_week'].sum()
        
        summary = {
            'total_activities': len(student_eca),
            'total_hours': total_hours,
            'activities': student_eca.to_dict('records')
        }
        
        return summary
        
    except Exception as e:
        print(f"Error getting ECA summary: {e}")
        return None

def get_progress_towards_graduation(username):
    """Calculate student's progress towards graduation."""
    try:
        if not os.path.exists("data/grades.csv"):
            return None
            
        grades_df = pd.read_csv("data/grades.csv")
        student_grades = grades_df[grades_df['username'] == username]
        
        if student_grades.empty:
            return None
            
        # Assuming 120 credits needed for graduation
        # Each course is worth 3 credits
        total_credits_needed = 120
        completed_credits = len(student_grades) * 3
        
        progress = {
            'completed_credits': completed_credits,
            'total_credits_needed': total_credits_needed,
            'completion_percentage': round((completed_credits / total_credits_needed) * 100, 2),
            'remaining_credits': total_credits_needed - completed_credits
        }
        
        return progress
        
    except Exception as e:
        print(f"Error calculating graduation progress: {e}")
        return None

def create_overall_grades_distribution():
    """Create a bar chart showing the distribution of grades across all students"""
    try:
        # Read grades data
        grades_df = pd.read_csv('data/grades.csv')
        
        # Create figure and axis
        plt.figure(figsize=(10, 6))
        
        # Create histogram of grades
        plt.hist(grades_df['grade'], bins=10, edgecolor='black')
        
        # Add labels and title
        plt.xlabel('Grade')
        plt.ylabel('Number of Students')
        plt.title('Overall Grade Distribution')
        
        # Add grid
        plt.grid(True, alpha=0.3)
        
        # Save the chart
        plt.savefig('data/overall_grades_distribution.png')
        plt.close()
        
        return 'data/overall_grades_distribution.png'
    except Exception as e:
        print(f"Error creating overall grades distribution chart: {str(e)}")
        return None

def create_subject_performance_comparison():
    """Create a box plot comparing performance across different subjects"""
    try:
        # Read grades data
        grades_df = pd.read_csv('data/grades.csv')
        
        # Create figure and axis
        plt.figure(figsize=(12, 6))
        
        # Create box plot
        grades_df.boxplot(column='grade', by='subject')
        
        # Add labels and title
        plt.xlabel('Subject')
        plt.ylabel('Grade')
        plt.title('Subject Performance Comparison')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Add grid
        plt.grid(True, alpha=0.3)
        
        # Save the chart
        plt.savefig('data/subject_performance_comparison.png')
        plt.close()
        
        return 'data/subject_performance_comparison.png'
    except Exception as e:
        print(f"Error creating subject performance comparison chart: {str(e)}")
        return None

def create_eca_distribution():
    """Create a pie chart showing the distribution of ECA types"""
    try:
        # Read ECA data
        eca_df = pd.read_csv('data/eca.csv')
        
        # Count occurrences of each activity
        activity_counts = eca_df['activity'].value_counts()
        
        # Create figure and axis
        plt.figure(figsize=(10, 8))
        
        # Create pie chart
        plt.pie(activity_counts, labels=activity_counts.index, autopct='%1.1f%%')
        
        # Add title
        plt.title('Distribution of Extracurricular Activities')
        
        # Save the chart
        plt.savefig('data/eca_distribution.png')
        plt.close()
        
        return 'data/eca_distribution.png'
    except Exception as e:
        print(f"Error creating ECA distribution chart: {str(e)}")
        return None

def create_hours_distribution():
    """Create a histogram showing the distribution of hours per week in ECAs"""
    try:
        # Read ECA data
        eca_df = pd.read_csv('data/eca.csv')
        
        # Create figure and axis
        plt.figure(figsize=(10, 6))
        
        # Create histogram
        plt.hist(eca_df['hours_per_week'], bins=10, edgecolor='black')
        
        # Add labels and title
        plt.xlabel('Hours per Week')
        plt.ylabel('Number of Students')
        plt.title('Distribution of ECA Hours per Week')
        
        # Add grid
        plt.grid(True, alpha=0.3)
        
        # Save the chart
        plt.savefig('data/hours_distribution.png')
        plt.close()
        
        return 'data/hours_distribution.png'
    except Exception as e:
        print(f"Error creating hours distribution chart: {str(e)}")
        return None

def get_overall_statistics():
    """Get overall statistics for all students"""
    try:
        # Read data
        grades_df = pd.read_csv('data/grades.csv')
        eca_df = pd.read_csv('data/eca.csv')
        
        stats = {
            'total_students': len(grades_df['username'].unique()),
            'total_grades': len(grades_df),
            'total_ecas': len(eca_df),
            'average_grade': grades_df['grade'].mean(),
            'median_grade': grades_df['grade'].median(),
            'grade_std_dev': grades_df['grade'].std(),
            'average_hours': eca_df['hours_per_week'].mean(),
            'total_hours': eca_df['hours_per_week'].sum(),
            'unique_subjects': len(grades_df['subject'].unique()),
            'unique_activities': len(eca_df['activity'].unique())
        }
        
        return stats
    except Exception as e:
        print(f"Error getting overall statistics: {str(e)}")
        return None 