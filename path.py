import tkinter as tk
import os
import subprocess
import platform

def open_file_explorer(folder):
    folder = get_absolut_path(folder)
    
    if platform.system() == "Windows":
        os.startfile(folder)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", folder])
    else:  # Linux
        subprocess.Popen(["xdg-open", folder])

def get_absolut_path(path):
    abs_path = os.path.abspath(path)
    return abs_path
