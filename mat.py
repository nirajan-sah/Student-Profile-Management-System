import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

class StudentAnalytics:
    """Class for handling student analytics and visualizations"""
    
    def __init__(self):
        """Initialize the analytics class"""
        self.data_dir = "data"
        self.charts_dir = os.path.join(self.data_dir, "charts")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.charts_dir):
            os.makedirs(self.charts_dir)
    
    def _cleanup_old_charts(self):
        """Clean up old chart files"""
        try:
            if os.path.exists(self.charts_dir):
                for file in os.listdir(self.charts_dir):
                    if file.endswith('.png'):
                        file_path = os.path.join(self.charts_dir, file)
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"Error removing chart {file}: {e}")
        except Exception as e:
            print(f"Error cleaning up charts: {e}")
    
    def create_grades_chart(self, grades, username):
        """Create a bar chart for student grades"""
        try:
            if not grades:
                return None
            
            # Clean up old charts
            self._cleanup_old_charts()
                
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
            plt.title(f'Grades for {username}', fontsize=14, pad=20)
            plt.xlabel('Subjects', fontsize=12)
            plt.ylabel('Grade', fontsize=12)
            plt.ylim(0, 100)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Rotate x-axis labels
            plt.xticks(rotation=45, ha='right')
            
            # Adjust layout
            plt.tight_layout()
            
            # Save the chart
            filename = f"grades_{username}.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error creating grades chart: {e}")
            return None

    def create_eca_chart(self, eca, username):
        """Create a pie chart for student ECA activities"""
        try:
            if not eca:
                return None
            
            # Clean up old charts
            self._cleanup_old_charts()
                
            # Extract activities and hours
            activities = [activity['activity'] for activity in eca]
            hours = [float(activity['hours_per_week']) for activity in eca]
            
            # Create the pie chart
            plt.figure(figsize=(10, 8))
            plt.pie(hours, labels=activities, autopct='%1.1f%%',
                    startangle=90, colors=plt.cm.Pastel1(np.linspace(0, 1, len(activities))))
            
            # Add title
            plt.title(f'ECA Distribution for {username}', fontsize=14, pad=20)
            
            # Add legend
            plt.legend(activities, title="Activities", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            # Make the pie chart circular
            plt.axis('equal')
            
            # Adjust layout
            plt.tight_layout()
            
            # Save the chart
            filename = f"eca_{username}.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error creating ECA chart: {e}")
            return None

    def create_performance_summary(self, grades, eca, username):
        """Create a summary of student performance"""
        try:
            if not grades or not eca:
                return None
            
            # Clean up old charts
            self._cleanup_old_charts()
                
            # Create figure with subplots
            fig = plt.figure(figsize=(15, 8))
            
            # Add title
            fig.suptitle(f'Performance Summary for {username}', fontsize=16, y=0.95)
            
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
            filename = f"summary_{username}.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error creating performance summary: {e}")
            return None

    def calculate_gpa(self, username):
        """Calculate GPA for a student"""
        try:
            if not os.path.exists(os.path.join(self.data_dir, "grades.csv")):
                return None
                
            grades_df = pd.read_csv(os.path.join(self.data_dir, "grades.csv"))
            
            if username not in grades_df['username'].values:
                return None
                
            student_row = grades_df[grades_df['username'] == username].iloc[0]
            grade_columns = [col for col in grades_df.columns if col != 'username']
            grades = []
            
            for column in grade_columns:
                grade_value = student_row[column]
                if pd.notna(grade_value):
                    grades.append(float(grade_value))
            
            if not grades:
                return None
                
            gpa = np.mean(grades) / 25  # Converting percentage to 4.0 scale
            return round(gpa, 2)
            
        except Exception as e:
            print(f"Error calculating GPA: {e}")
            return None

    def get_grade_statistics(self, username):
        """Get statistical information about a student's grades"""
        try:
            if not os.path.exists(os.path.join(self.data_dir, "grades.csv")):
                return None
                
            grades_df = pd.read_csv(os.path.join(self.data_dir, "grades.csv"))
            
            if username not in grades_df['username'].values:
                return None
                
            student_row = grades_df[grades_df['username'] == username].iloc[0]
            grade_columns = [col for col in grades_df.columns if col != 'username']
            grades = []
            
            for column in grade_columns:
                grade_value = student_row[column]
                if pd.notna(grade_value):
                    grades.append(float(grade_value))
            
            if not grades:
                return None
                
            stats = {
                'mean': round(np.mean(grades), 2),
                'median': round(np.median(grades), 2),
                'min': round(np.min(grades), 2),
                'max': round(np.max(grades), 2),
                'std_dev': round(np.std(grades), 2)
            }
            
            return stats
            
        except Exception as e:
            print(f"Error calculating grade statistics: {e}")
            return None

    def get_eca_summary(self, username):
        """Get summary of student's extracurricular activities"""
        try:
            if not os.path.exists(os.path.join(self.data_dir, "eca.csv")):
                return None
                
            eca_df = pd.read_csv(os.path.join(self.data_dir, "eca.csv"))
            student_eca = eca_df[eca_df['username'] == username]
            
            if student_eca.empty:
                return None
                
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

    def create_overall_grades_distribution(self):
        """Create a bar chart showing the distribution of grades across all students"""
        try:
            # Clean up old charts
            self._cleanup_old_charts()
                
            grades_df = pd.read_csv(os.path.join(self.data_dir, 'grades.csv'))
            
            all_grades = []
            for column in grades_df.columns:
                if column != 'username':
                    subject_grades = grades_df[column].dropna().tolist()
                    all_grades.extend(subject_grades)
            
            if not all_grades:
                return None
            
            plt.figure(figsize=(10, 6))
            plt.hist(all_grades, bins=10, edgecolor='black')
            
            plt.xlabel('Grade')
            plt.ylabel('Number of Students')
            plt.title('Overall Grade Distribution')
            plt.grid(True, alpha=0.3)
            
            filename = f"overall_grades.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error creating overall grades distribution chart: {e}")
            return None

    def create_subject_performance_comparison(self):
        """Create a box plot comparing performance across different subjects"""
        try:
            # Clean up old charts
            self._cleanup_old_charts()
                
            grades_df = pd.read_csv(os.path.join(self.data_dir, 'grades.csv'))
            subject_columns = [col for col in grades_df.columns if col != 'username']
            
            if not subject_columns:
                return None
            
            plt.figure(figsize=(12, 6))
            data = [grades_df[subject].dropna().tolist() for subject in subject_columns]
            plt.boxplot(data, labels=subject_columns)
            
            plt.xlabel('Subject')
            plt.ylabel('Grade')
            plt.title('Subject Performance Comparison')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            filename = f"subject_comparison.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error creating subject performance comparison chart: {e}")
            return None

    def create_eca_distribution(self):
        """Create a pie chart showing the distribution of ECA types"""
        try:
            # Clean up old charts
            self._cleanup_old_charts()
                
            eca_df = pd.read_csv(os.path.join(self.data_dir, 'eca.csv'))
            activity_counts = eca_df['activity'].value_counts()
            
            plt.figure(figsize=(10, 8))
            plt.pie(activity_counts, labels=activity_counts.index, autopct='%1.1f%%')
            plt.title('Distribution of Extracurricular Activities')
            
            filename = f"eca_distribution.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error creating ECA distribution chart: {e}")
            return None

    def create_hours_distribution(self):
        """Create a histogram showing the distribution of hours per week in ECAs"""
        try:
            # Clean up old charts
            self._cleanup_old_charts()
                
            eca_df = pd.read_csv(os.path.join(self.data_dir, 'eca.csv'))
            
            plt.figure(figsize=(10, 6))
            plt.hist(eca_df['hours_per_week'], bins=10, edgecolor='black')
            
            plt.xlabel('Hours per Week')
            plt.ylabel('Number of Students')
            plt.title('Distribution of ECA Hours per Week')
            plt.grid(True, alpha=0.3)
            
            filename = f"hours_distribution.png"
            filepath = os.path.join(self.charts_dir, filename)
            plt.savefig(filepath)
            plt.close()
            
            return filepath
        except Exception as e:
            print(f"Error creating hours distribution chart: {e}")
            return None

    def get_overall_statistics(self):
        """Get overall statistics for all students"""
        try:
            grades_df = pd.read_csv(os.path.join(self.data_dir, 'grades.csv'))
            eca_df = pd.read_csv(os.path.join(self.data_dir, 'eca.csv'))
            
            subject_columns = [col for col in grades_df.columns if col != 'username']
            all_grades = []
            
            for column in subject_columns:
                subject_grades = grades_df[column].dropna().tolist()
                all_grades.extend(subject_grades)
            
            stats = {
                'total_students': len(grades_df),
                'total_grades': len(all_grades),
                'total_ecas': len(eca_df),
                'average_grade': np.mean(all_grades) if all_grades else 0,
                'median_grade': np.median(all_grades) if all_grades else 0,
                'grade_std_dev': np.std(all_grades) if all_grades else 0,
                'average_hours': eca_df['hours_per_week'].mean() if not eca_df.empty else 0,
                'total_hours': eca_df['hours_per_week'].sum() if not eca_df.empty else 0,
                'unique_subjects': len(subject_columns),
                'unique_activities': len(eca_df['activity'].unique()) if not eca_df.empty else 0
            }
            
            return stats
        except Exception as e:
            print(f"Error getting overall statistics: {e}")
            return None 