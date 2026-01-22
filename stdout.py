""" Create with chatgpt 22/01/2026
Need to be set as a value of 'sys.stdout'
"""
import tkinter as tk

class RedirectText:
    def __init__(self, widget):
        self.widget = widget
    
    def write(self, string):
        self.widget.config(state="normal")     # autoriser l'écriture
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.config(state="disabled")   # re-bloquer
    
    def flush(self):
        pass     # nécessaire pour sys.stdout


if __name__ == "__main__":
    import subprocess
    import sys
    from tkinter.scrolledtext import ScrolledText
    
    def subprocess_captured_output():
        """ exemple of how to get the output from subprocess"""
        result = subprocess.run(["ffmpeg","-version"], capture_output=True, text=True, shell=True)
        # print est récupérer et envoyer dans la text box
        print(result.stdout) 
        print(result.stderr)
    
    root = tk.Tk()
    root.title("Console Tkinter")
    
    # Creation of the text box
    text = ScrolledText(root, width=100, height=25, state="disabled")
    text.pack(padx=10, pady=10)
    
    # Define the text box as the standard output
    sys.stdout = RedirectText(text)
    
    print("Console en lecture seule")
    print("Impossible d'écrire ici au clavier\n")
    
    
    
    # -----------------------------
    def pr():
        print("Clic")
    tk.Button(root,text="Press",command=pr).pack(side="left",expand="yes")
    tk.Button(root,text="subprocess",command=subprocess_captured_output).pack(side="left",expand="yes")
    
    root.mainloop()