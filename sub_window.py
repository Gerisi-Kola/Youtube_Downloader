import tkinter as tk
from tkinter import ttk
#    ----    ----
import pymod._yt_dlp as yt_dlp
import pymod.ico_and_folder as IcoFolder
import pymod.files_controller as File

class SubWindow:
    def __init__(self,root: tk.Tk, colors: dict, path:dict, title :str):
        self.COLORS = colors
        self.BNT_COLORS = dict(self.COLORS["button_colors"])
        self.PATH = path
        
        self.win = tk.Toplevel(root)
        self.win.geometry("600x500")
        self.win.title(title)
        self.win.configure(background = self.COLORS["bg"])
        try:
            IcoFolder.taskbar_icon(self.PATH['ico'])
            self.win.iconbitmap(self.PATH['ico'])
        except Exception as e:
            print(f"Can not load ico : {e}")
        
    
    def create_settings_window(self):
        update_button = ttk.Button(self.win,text="Update yt-dlp",command=self.update_yt_dlp)
        update_button.pack()
        
        history_button = ttk.Button(self.win,text="View history",command=self.create_history_window)
        history_button.pack()
    
    def create_history_window(self):
        his_win = SubWindow(self.win,self.COLORS,self.PATH, "History of Download")
        his_win.show_history()
    
    def show_history(self, im):
        im = File.get_file_content_json("./history/2026_02_01.log")
        dic_label = {}
        for i in im.keys:
            dic_label[f"image_{i}"] = "a"
    
    def update_yt_dlp(self):
        yt_dlp.update_nightly()
        #quit()

"""if __name__ == "__main__":
    self.SETTINGS          = dict(settings["current_settings"])
        self.ORIGINAL_SETTINGS = dict(settings["original_settings"])
        self.COLORS            = dict(settings["colors"]["default"
    sub = SubWindow()"""