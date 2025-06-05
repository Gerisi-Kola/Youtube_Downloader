import os
import subprocess
import platform
import ctypes


def open_file_explorer(folder: str) -> None:
    folder = get_absolut_path(folder)
    
    if platform.system() == "Windows":
        os.startfile(folder)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", folder])
    else:  # Linux
        subprocess.Popen(["xdg-open", folder])

def get_absolut_path(path: str) -> str:
    abs_path = os.path.abspath(path)
    abs_path = abs_path.replace("\\", "/")
    return abs_path

def taskbar_icon():
    # this is the part that sets the icon
    if platform.system() == "Windows":
        myappid = 'tkinter.python.test'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)