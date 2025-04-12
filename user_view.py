import tkinter as tk
from tkinter import ttk, messagebox
from auth import authenticate
from admin_view import AdminView
from student_view import StudentView

class UserView:
    def __init__(self, parent=None):
        # Create main window
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title("Student Profile Management System")
        self.root.geometry("1000x800")
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1000x800+{x}+{y}")
        
        self.create_widgets()
        
        if not parent:
            self.root.mainloop()
            
    def create_widgets(self):
        self.root.configure(bg="#b5b4a7")
        self.root.geometry("1000x800")
        # Create login frame
        login_frame = ttk.LabelFrame(self.root, text="Login", padding="20", borderwidth=5)
        login_frame.pack(fill="both", padx=50, pady=50)
        
        # Username field
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.username_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Password field
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=5, pady=5)
        
        # Login button
        ttk.Button(login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Configure grid weights
        login_frame.columnconfigure(1, weight=1)
        
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password")
            return
            
        # Authenticate user
        user = authenticate(username, password)
        
        if user:
            # Clear login form
            self.username_var.set("")
            self.password_var.set("")
            
            # Open appropriate view based on role
            if user['role'] == 'admin':
                AdminView(self.root)
            elif user['role'] == 'student':
                StudentView(username, self.root)
            else:
                messagebox.showerror("Error", "Invalid user role")
        else:
            messagebox.showerror("Error", "Invalid username or password")
            
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if isinstance(self.root, tk.Toplevel):
                self.root.master.destroy()  # Close the entire application
            else:
                self.root.destroy()  # Close just this window
                

if __name__ == "__main__":
    UserView()
    
