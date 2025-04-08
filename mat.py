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
        hours = [activity['hours'] for activity in eca]
        
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

def create_gpa_chart(gpa):
    """Create a gauge chart for student GPA"""
    try:
        if gpa is None:
            return None
            
        # Create the gauge chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create the gauge
        gauge = ax.barh(0, gpa, color='skyblue', height=0.3)
        
        # Add value label
        plt.text(gpa, 0, f'{gpa:.2f}', ha='center', va='center', fontsize=14)
        
        # Customize the chart
        plt.title('Student GPA', fontsize=14, pad=20)
        plt.xlim(0, 4.0)  # Set x-axis from 0 to 4.0
        plt.ylim(-0.5, 0.5)  # Set y-axis to show only the gauge
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Remove y-axis
        plt.yticks([])
        
        # Add x-axis labels
        plt.xticks([0, 1, 2, 3, 4], ['0.0', '1.0', '2.0', '3.0', '4.0'])
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the chart
        if not os.path.exists("data/charts"):
            os.makedirs("data/charts")
        plt.savefig("data/charts/gpa_chart.png")
        plt.close()
        
        return "data/charts/gpa_chart.png"
    except Exception as e:
        print(f"Error creating GPA chart: {e}")
        return None

def create_performance_summary(grades, eca, gpa):
    """Create a summary of student performance"""
    try:
        if not grades or not eca or gpa is None:
            return None
            
        # Create a figure with subplots
        fig = plt.figure(figsize=(15, 10))
        
        # Add a title
        fig.suptitle('Student Performance Summary', fontsize=16, y=0.95)
        
        # Create subplots
        gs = fig.add_gridspec(2, 2)
        
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
        hours = [activity['hours'] for activity in eca]
        ax2.pie(hours, labels=activities, autopct='%1.1f%%',
                startangle=90, colors=plt.cm.Pastel1(np.linspace(0, 1, len(activities))))
        ax2.set_title('Distribution of ECA Hours')
        
        # GPA subplot
        ax3 = fig.add_subplot(gs[1, :])
        gauge = ax3.barh(0, gpa, color='skyblue', height=0.3)
        ax3.text(gpa, 0, f'{gpa:.2f}', ha='center', va='center', fontsize=14)
        ax3.set_title('GPA')
        ax3.set_xlim(0, 4.0)
        ax3.set_ylim(-0.5, 0.5)
        ax3.grid(axis='x', linestyle='--', alpha=0.7)
        ax3.set_yticks([])
        ax3.set_xticks([0, 1, 2, 3, 4])
        ax3.set_xticklabels(['0.0', '1.0', '2.0', '3.0', '4.0'])
        
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