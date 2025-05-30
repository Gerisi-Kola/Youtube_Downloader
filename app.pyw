import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
#    ----    ----
from settings_manager import convert_settings_for_yt_dlp_sub
import path
import download_manager

class TkApp:
    def __init__(self, settings):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Youtube mp4/mp3")
        self.root.config(bg = "ivory")
        
        self.url = None #'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        
        self.dl = download_manager.DowloadManager()
        
        self.settings = settings["current_settings"]
        self.original_settings = settings["original_settings"]
        self.settings["tmp_folder_absolut"] = \
                    path.get_absolut_path(self.settings["tmp_folder"])
        
        
        
        self.style = ttk.Style()
        self.style.configure("TButton", padding=11, background="ivory")
        self.style.configure("TEntry", padding=8, background="ivory")
        
        #   ----    ----    Frame    ----    ----
        self.top_frame = tk.Frame(self.root, bg="ivory")
        self.top_frame.pack(expand="yes")
        self.search_frame = tk.Frame(self.top_frame, bg="ivory")
        self.search_frame.pack(expand="yes")
        self.progress_frame = tk.Frame(self.top_frame, bg="ivory")
        self.progress_frame.pack(expand="yes")
        
        self.settings_frame = tk.Frame(self.root, bg="ivory")
        self.settings_frame.pack(expand="yes")
        self.mp4_mp3_frame = tk.Frame(self.settings_frame, bg="ivory")
        self.mp4_mp3_frame.pack(side = "left", padx = 50, pady=30)
        
        #   ----    ----    Search    ----    ----
        self.search_entry = ttk.Entry(self.search_frame,
                                        font="bold 15",
                                        width=50
                                        )
        self.search_entry.pack(side = "left",padx=30)
        
        self.search_button = ttk.Button(self.search_frame,
                                        text="Search",
                                        command=self.get_search,
                                        takefocus=False
                                        )
        self.search_button.pack(side="left")
        
        self.progressbar = ttk.Progressbar( self.progress_frame,
                                            mode='indeterminate',
                                            length=420
                                            )
        self.progressbar.pack(side="top", pady=20)
        
        #   ----    ----    mp3 or mp4    ----    ----
        self.mp3_or_mp4_label = tk.Label(self.mp4_mp3_frame,
                                        font="bold 18",
                                        bg="ivory"
                                        )
        self.mp3_or_mp4_label.pack(side="top")
        self.mp3_button = tk.Button(self.mp4_mp3_frame,
                                    text = "mp3",
                                    font="bold 15",
                                    command=self.mp3_command
                                    )
        self.mp3_button.pack(side="left")
        self.mp4_button = tk.Button(self.mp4_mp3_frame,
                                    text = "mp4",
                                    font="bold 15",
                                    command=self.mp4_command
                                    )
        self.mp4_button.pack()
        self.mp3_or_mp4_check()
        
        #   ----    ----    Folder    ----    ----
        self.folder_button = ttk.Button(self.settings_frame,
                                        text = "Folder",
                                        command=self.choice_of_folder,
                                        takefocus=False
                                        )
        self.folder_button.pack(expand="yes",side="left")
        
        self.open_folder_button = ttk.Button(
                                    self.settings_frame,
                                    text = "Open Folder",
                                    command=lambda : path.open_file_explorer\
                                            (self.settings["save_folder"]),
                                    takefocus=False
                                    )
        self.open_folder_button.pack(expand="yes",side="left")
        
        #   ----    ----    Quality    ----    ----
        # set up variable
        self.option_var = tk.StringVar(self.root)
        
        self.style.configure("TMenubutton",background = "white", padding=13, width = 6,font="bold 15")
        
        self.quality_option_menu = ttk.OptionMenu(
                                        self.settings_frame,
                                        self.option_var,
                                        #self.settings["video_quality"],
                                        *self.settings["all_video_quality"],
                                        #command=self.option_changed
                                        )
        self.quality_option_menu.pack(side="right")
        
        
        self.url = self.search_entry.get()
        self.download_ops = convert_settings_for_yt_dlp_sub(self.settings,self.url)
        
        self.root.mainloop()
    
    def get_search(self):
        self.url = self.search_entry.get()
        self.dl.download_and_save(self.settings,
                                    self.url,
                                    self.start_progressbar,
                                    self.stop_progressbar
                                    )
    
    
    def start_progressbar(self):
        self.progressbar.start()
    
    def stop_progressbar(self):
        self.progressbar.stop()
    
    def mp3_command(self):
        if not self.settings["audio_only"]:
            self.settings["audio_only"] = True
            self.mp3_button.config(bg = "#27a300")
            self.mp4_button.config(bg = "red")
            self.mp3_or_mp4_label.config(text=".mp3")
            
            self.save_new_settings()
    
    def mp4_command(self):
        if self.settings["audio_only"]:
            self.settings["audio_only"] = False
            self.mp4_button.config(bg = "#27a300")
            self.mp3_button.config(bg = "red")
            self.mp3_or_mp4_label.config(text=".mp4")
            
            self.save_new_settings()
    
    def mp3_or_mp4_check(self):
        if self.settings["audio_only"]:
            self.mp3_button.config(bg = "#27a300")
            self.mp4_button.config(bg = "red")
            self.mp3_or_mp4_label.config(text=".mp3")
        
        elif not self.settings["audio_only"]:
            self.mp4_button.config(bg = "#27a300")
            self.mp3_button.config(bg = "red")
            self.mp3_or_mp4_label.config(text=".mp4")
    
    def choice_of_folder(self):
        folder = filedialog.askdirectory()
        self.settings["save_folder"] = folder
        """print(folder)
        print(self.settings)"""
        
        self.save_new_settings()
    
    def open_folder(self):
        filedialog.Directory()
    
    def change_quality(self,quality):
        
        self.save_new_settings()
    
    def save_new_settings(self):
        #print("settings has been saved !")
        self.download_ops = convert_settings_for_yt_dlp_sub(self.settings,self.url)


if __name__ == "__main__":
    from json_controler import get_json
    settings = get_json("settings.json")
    win = TkApp(settings=settings)