import tkinter as tk
from tkinter import ttk

# Color scheme
COLORS = {
    "primary": "#4a90e2",
    "secondary": "#50e3c2",
    "success": "#5cb85c",
    "danger": "#d9534f",
    "warning": "#f0ad4e",
    "light": "#f8f9fa",
    "dark": "#343a40"
}

# Font styles
FONTS = {
    "heading": ("Helvetica", 24, "bold"),
    "subheading": ("Helvetica", 18, "bold"),
    "normal": ("Helvetica", 12),
    "small": ("Helvetica", 10)
}

def create_styled_button(parent, text, command, bg_color=COLORS["primary"]):
    """
    Create a styled button with consistent appearance.
    """
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg="white",
        font=FONTS["normal"],
        relief=tk.FLAT,
        padx=20,
        pady=10
    )
    button.bind("<Enter>", lambda e: button.config(bg=adjust_color(bg_color, -20)))
    button.bind("<Leave>", lambda e: button.config(bg=bg_color))
    return button

def create_styled_label(parent, text, font=FONTS["normal"], fg=COLORS["dark"]):
    """
    Create a styled label with consistent appearance.
    """
    return tk.Label(
        parent,
        text=text,
        font=font,
        fg=fg,
        bg=COLORS["light"]
    )

def create_styled_entry(parent, show=None):
    """
    Create a styled entry field with consistent appearance.
    """
    return tk.Entry(
        parent,
        font=FONTS["normal"],
        relief=tk.SOLID,
        borderwidth=1,
        show=show
    )

def create_styled_frame(parent, bg=COLORS["light"]):
    """
    Create a styled frame with consistent appearance.
    """
    return tk.Frame(
        parent,
        bg=bg,
        padx=20,
        pady=20
    )

def adjust_color(color, amount):
    """
    Adjust the brightness of a color by the given amount.
    """
    # Convert hex to RGB
    color = color.lstrip('#')
    r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    
    # Adjust each component
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    
    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}'

def create_styled_combobox(parent, values):
    """
    Create a styled combobox with consistent appearance.
    """
    style = ttk.Style()
    style.configure(
        "Custom.TCombobox",
        fieldbackground=COLORS["light"],
        background=COLORS["light"],
        arrowcolor=COLORS["dark"]
    )
    
    combo = ttk.Combobox(
        parent,
        values=values,
        style="Custom.TCombobox",
        font=FONTS["normal"]
    )
    return combo 