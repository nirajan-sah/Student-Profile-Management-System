import tkinter as tk
from tkinter import ttk

# Color scheme
COLORS = {
    'primary': '#007bff',
    'secondary': '#6c757d',
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# Font styles
FONTS = {
    'title': ('Arial', 16, 'bold'),
    'subtitle': ('Arial', 14, 'bold'),
    'normal': ('Arial', 12),
    'small': ('Arial', 10)
}

def create_button(parent, text, command):
    """Create a styled button"""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=COLORS['primary'],
        fg='white',
        font=FONTS['normal'],
        relief=tk.FLAT,
        padx=10,
        pady=5
    )
    
    def on_enter(e):
        btn['bg'] = adjust_color(COLORS['primary'], -20)
        
    def on_leave(e):
        btn['bg'] = COLORS['primary']
        
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    
    return btn

def create_label(parent, text, font=None):
    """Create a styled label"""
    return tk.Label(
        parent,
        text=text,
        font=font or FONTS['normal'],
        bg='white'
    )

def create_entry(parent, show=None):
    """Create a styled entry field"""
    return tk.Entry(
        parent,
        show=show,
        font=FONTS['normal'],
        relief=tk.SOLID,
        borderwidth=1
    )

def create_frame(parent):
    """Create a styled frame"""
    return tk.Frame(
        parent,
        bg='white'
    )

def create_combobox(parent, values):
    """Create a styled combobox"""
    return ttk.Combobox(
        parent,
        values=values,
        font=FONTS['normal']
    )

def adjust_color(color, amount):
    """Adjust color brightness"""
    # Convert hex to RGB
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    
    # Adjust each component
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    
    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}' 