import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox, ttk
from auth import get_user_details, get_student_grades, get_student_eca, update_student_profile
from ui_components import (
    create_styled_button, create_styled_label, create_styled_entry,
    create_styled_frame, create_styled_combobox, COLORS, FONTS
)

def view_average_grades():
    """
    View average grades per subject across all students.
    """
    try:
        # Read grades data
        df = pd.read_csv("data/grades.csv")
        
        # Calculate average for each grade column
        grade_columns = [col for col in df.columns if col.startswith('grade')]
        averages = df[grade_columns].mean()
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(1, len(grade_columns) + 1), averages)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom')
        
        ax.set_xlabel('Subject')
        ax.set_ylabel('Average Grade')
        ax.set_title('Average Grades per Subject')
        ax.set_xticks(range(1, len(grade_columns) + 1))
        
        # Create new window for the plot
        plot_window = tk.Toplevel()
        plot_window.title("Average Grades per Subject")
        plot_window.geometry("800x600")
        
        # Embed the plot in the window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add save button
        save_button = create_styled_button(plot_window, "Save and Return", lambda: plot_window.destroy(), COLORS["success"])
        save_button.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate average grades: {str(e)}")

def view_eca_activity():
    """
    View most active students in ECA.
    """
    try:
        # Read ECA data
        df = pd.read_csv("data/eca.csv")
        
        # Count non-empty activities for each student
        activity_counts = []
        for _, row in df.iterrows():
            count = sum(1 for col in ['activity1', 'activity2', 'activity3'] 
                      if pd.notna(row[col]) and row[col].strip())
            activity_counts.append((row['username'], count))
        
        # Sort by activity count
        activity_counts.sort(key=lambda x: x[1], reverse=True)
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        students = [x[0] for x in activity_counts]
        counts = [x[1] for x in activity_counts]
        
        bars = ax.bar(students, counts)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom')
        
        ax.set_xlabel('Student')
        ax.set_ylabel('Number of Activities')
        ax.set_title('ECA Participation by Student')
        plt.xticks(rotation=45)
        
        # Create new window for the plot
        plot_window = tk.Toplevel()
        plot_window.title("ECA Activity Analysis")
        plot_window.geometry("800x600")
        
        # Embed the plot in the window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add save button
        save_button = create_styled_button(plot_window, "Save and Return", lambda: plot_window.destroy(), COLORS["success"])
        save_button.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate ECA activity analysis: {str(e)}")

def modify_student_data(user):
    """
    UI for modifying student data (personal info, grades, ECA).
    """
    def load_student_data():
        username = student_var.get()
        if not username:
            return
            
        # Load personal info
        user = get_user_details(username)
        if user:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, user.full_name)
        
        # Load grades
        grades = get_student_grades(username)
        if grades:
            for i, grade in enumerate(grades):
                grade_entries[i].delete(0, tk.END)
                grade_entries[i].insert(0, grade)
        
        # Load ECA
        eca = get_student_eca(username)
        if eca:
            for i, activity in enumerate(eca):
                eca_entries[i].delete(0, tk.END)
                eca_entries[i].insert(0, activity)
    
    def save_changes():
        username = student_var.get()
        if not username:
            messagebox.showerror("Error", "Please select a student")
            return
        
        try:
            # Update personal info
            new_name = name_entry.get()
            update_student_profile(username, new_name)
            
            # Update grades
            new_grades = [entry.get() for entry in grade_entries]
            df = pd.read_csv("data/grades.csv")
            df.loc[df['username'] == username, ['grade1', 'grade2', 'grade3', 'grade4', 'grade5']] = new_grades
            df.to_csv("data/grades.csv", index=False)
            
            # Update ECA
            new_eca = [entry.get() for entry in eca_entries]
            df = pd.read_csv("data/eca.csv")
            df.loc[df['username'] == username, ['activity1', 'activity2', 'activity3']] = new_eca
            df.to_csv("data/eca.csv", index=False)
            
            messagebox.showinfo("Success", "Student data updated successfully!")
            modify_window.destroy()
            admin_dashboard(user)  # Return to admin dashboard
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student data: {str(e)}")
    
    # Create modification window
    modify_window = tk.Toplevel()
    modify_window.title("Modify Student Data")
    modify_window.geometry("600x800")
    modify_window.configure(bg=COLORS["light"])
    
    # Create main frame
    main_frame = tk.Frame(modify_window, bg=COLORS["light"], padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Student selection
    student_frame = tk.Frame(main_frame, bg=COLORS["light"])
    student_frame.pack(fill=tk.X, pady=10)
    
    create_styled_label(student_frame, "Select Student:", FONTS["normal"]).pack(side=tk.LEFT, padx=(0, 10))
    
    # Get list of students
    df = pd.read_csv("data/users.csv")
    students = df[df['role'] == 'student']['username'].tolist()
    
    student_var = tk.StringVar()
    student_menu = ttk.Combobox(student_frame, textvariable=student_var, values=students)
    student_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Personal info section
    personal_frame = tk.LabelFrame(main_frame, text="Personal Information", bg=COLORS["light"], padx=10, pady=10)
    personal_frame.pack(fill=tk.X, pady=10)
    
    create_styled_label(personal_frame, "Full Name:", FONTS["normal"]).pack(anchor=tk.W)
    name_entry = create_styled_entry(personal_frame)
    name_entry.pack(fill=tk.X, pady=5)
    
    # Grades section
    grades_frame = tk.LabelFrame(main_frame, text="Grades", bg=COLORS["light"], padx=10, pady=10)
    grades_frame.pack(fill=tk.X, pady=10)
    
    grade_entries = []
    for i in range(5):
        create_styled_label(grades_frame, f"Subject {i+1}:", FONTS["normal"]).pack(anchor=tk.W)
        entry = create_styled_entry(grades_frame)
        entry.pack(fill=tk.X, pady=5)
        grade_entries.append(entry)
    
    # ECA section
    eca_frame = tk.LabelFrame(main_frame, text="Extracurricular Activities", bg=COLORS["light"], padx=10, pady=10)
    eca_frame.pack(fill=tk.X, pady=10)
    
    eca_entries = []
    for i in range(3):
        create_styled_label(eca_frame, f"Activity {i+1}:", FONTS["normal"]).pack(anchor=tk.W)
        entry = create_styled_entry(eca_frame)
        entry.pack(fill=tk.X, pady=5)
        eca_entries.append(entry)
    
    # Buttons
    button_frame = tk.Frame(main_frame, bg=COLORS["light"])
    button_frame.pack(fill=tk.X, pady=20)
    
    create_styled_button(button_frame, "Load Data", load_student_data, COLORS["primary"]).pack(side=tk.LEFT, padx=5)
    create_styled_button(button_frame, "Save Changes", save_changes, COLORS["success"]).pack(side=tk.RIGHT, padx=5)

def view_student_details():
    """
    View detailed information about a selected student.
    """
    def load_student_data():
        username = student_var.get()
        if not username:
            return
            
        # Load personal info
        user = get_user_details(username)
        if user:
            name_label.config(text=f"Full Name: {user.full_name}")
            role_label.config(text=f"Role: {user.role}")
        
        # Load grades
        grades = get_student_grades(username)
        if grades:
            grades_text = "\n".join([f"Subject {i+1}: {grade}" for i, grade in enumerate(grades)])
            grades_label.config(text=f"Grades:\n{grades_text}")
        else:
            grades_label.config(text="No grades found.")
        
        # Load ECA
        eca = get_student_eca(username)
        if eca:
            eca_text = "\n".join([f"Activity {i+1}: {activity}" for i, activity in enumerate(eca)])
            eca_label.config(text=f"Extracurricular Activities:\n{eca_text}")
        else:
            eca_label.config(text="No extracurricular activities found.")
    
    # Create details window
    details_window = tk.Toplevel()
    details_window.title("Student Details")
    details_window.geometry("600x800")
    details_window.configure(bg=COLORS["light"])
    
    # Create main frame
    main_frame = tk.Frame(details_window, bg=COLORS["light"], padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Student selection
    student_frame = tk.Frame(main_frame, bg=COLORS["light"])
    student_frame.pack(fill=tk.X, pady=10)
    
    create_styled_label(student_frame, "Select Student:", FONTS["normal"]).pack(side=tk.LEFT, padx=(0, 10))
    
    # Get list of students
    df = pd.read_csv("data/users.csv")
    students = df[df['role'] == 'student']['username'].tolist()
    
    student_var = tk.StringVar()
    student_menu = ttk.Combobox(student_frame, textvariable=student_var, values=students)
    student_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Personal info section
    personal_frame = tk.LabelFrame(main_frame, text="Personal Information", bg=COLORS["light"], padx=10, pady=10)
    personal_frame.pack(fill=tk.X, pady=10)
    
    name_label = create_styled_label(personal_frame, "Full Name: ", FONTS["normal"])
    name_label.pack(anchor=tk.W)
    
    role_label = create_styled_label(personal_frame, "Role: ", FONTS["normal"])
    role_label.pack(anchor=tk.W)
    
    # Grades section
    grades_frame = tk.LabelFrame(main_frame, text="Grades", bg=COLORS["light"], padx=10, pady=10)
    grades_frame.pack(fill=tk.X, pady=10)
    
    grades_label = create_styled_label(grades_frame, "No grades found.", FONTS["normal"])
    grades_label.pack(anchor=tk.W)
    
    # ECA section
    eca_frame = tk.LabelFrame(main_frame, text="Extracurricular Activities", bg=COLORS["light"], padx=10, pady=10)
    eca_frame.pack(fill=tk.X, pady=10)
    
    eca_label = create_styled_label(eca_frame, "No extracurricular activities found.", FONTS["normal"])
    eca_label.pack(anchor=tk.W)
    
    # Buttons
    button_frame = tk.Frame(main_frame, bg=COLORS["light"])
    button_frame.pack(fill=tk.X, pady=20)
    
    create_styled_button(button_frame, "Load Data", load_student_data, COLORS["primary"]).pack(side=tk.LEFT, padx=5)
    create_styled_button(button_frame, "Save and Return", lambda: details_window.destroy(), COLORS["success"]).pack(side=tk.RIGHT, padx=5) 