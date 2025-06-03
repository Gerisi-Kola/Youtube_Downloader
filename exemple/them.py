import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()

def change_theme(theme_name):
    if theme_name in style.theme_names():
        style.theme_use(theme_name)
        print(f"Theme changed to: {theme_name}")
    else:
        print(f"Theme '{theme_name}' not found.")

# Create buttons to change themes
clam_button = ttk.Button(root, text="Clam Theme", command=lambda: change_theme('clam'))
clam_button.pack()

alt_button = ttk.Button(root, text="Alt Theme", command=lambda: change_theme('alt'))
alt_button.pack()

default_button = ttk.Button(root, text="Default Theme", command=lambda: change_theme('default'))
default_button.pack()

# Initial widgets (will use the default theme initially)
label = ttk.Label(root, text="Themed Label")
label.pack()

root.mainloop()
