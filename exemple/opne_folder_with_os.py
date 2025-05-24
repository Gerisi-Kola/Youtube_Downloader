import tkinter as tk
import os
import subprocess
import platform

def ouvrir_explorateur():
    dossier = "C:/Users/Fatmira/Documents/MEGA"
    
    if platform.system() == "Windows":
        os.startfile(dossier)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", dossier])
    else:  # Linux
        subprocess.Popen(["xdg-open", dossier])

# Interface tkinter
fenetre = tk.Tk()
fenetre.title("Ouvrir l'explorateur")

bouton = tk.Button(fenetre, text="Ouvrir dossier", command=ouvrir_explorateur)
bouton.pack(pady=20)

fenetre.mainloop()
