import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json_controler as json
#    ----    ----
import path
import download_manager

class TkApp:
    def __init__(self, settings: dict):
        
        #   ----    ----    Settings   ----    ----
        self.settings = settings["current_settings"]
        self.original_settings = settings["original_settings"]
        self.colors = settings["colors"]["default"]
        self.bnt_color = self.colors["button_colors"]
        self.progressbar_color = self.colors["progressbar"]
        self.settings["tmp_folder_absolut"] = \
                    path.get_absolut_path(self.settings["tmp_folder"])
        
        #   ----    ----    Window creation   ----    ----
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Youtube mp4/mp3")
        self.root.configure(background = self.colors["bg"])
        title_label = tk.Label(self.root,text="YouTube Downloader", bg=self.colors["bg"], font="bold 20")
        title_label.pack(pady=30)
        path.taskbar_icon()
        self.root.iconbitmap(r"./image/ico/YouTubeDownloader.ico")
        
        self.url = "" #'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        self.error_progressbar = False
        self.dl = download_manager.DowloadManager()
        
        #   ----    ----  Style   ----    ----
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton",
                            padding=11,
                            background=self.bnt_color["background"],
                            troughcolor=self.bnt_color["troughcolor"],
                            bordercolor=self.bnt_color["bordercolor"],
                            lightcolor=self.bnt_color["lightcolor"],
                            darkcolor=self.bnt_color["darkcolor"]
                            )
        self.style.configure("TEntry",
                            padding=8,
                            background="ivory"
                            )
        self.style.configure("TMenubutton",
                            background = "white",
                            padding=13,
                            width = 6,
                            font="bold 15",
                            )
        self.style.configure("Horizontal.TProgressbar",
                            background = self.progressbar_color["background"],   # Vert doux (barre)
                            troughcolor = self.progressbar_color["troughcolor"],  # Beige clair (fond)
                            bordercolor = self.progressbar_color["bordercolor"],  # Bordure légère
                            lightcolor = self.progressbar_color["lightcolor"],   # Lumière
                            darkcolor = self.progressbar_color["darkcolor"],    # Ombre verte
                            )
        self.style.configure("TFrame",
                            background=self.colors["bg"],
                            )
        self.style.configure("TLabel",
                            background=self.colors["bg"]
                            )
        self.style.configure("MP3.TButton",
                            )
        self.style.configure("MP4.TButton",
                            )
        
        #   ----    ----    Frame    ----    ----
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack()
        self.search_frame = ttk.Frame(self.top_frame)
        self.search_frame.pack(expand="yes")
        self.progress_frame = ttk.Frame(self.top_frame)
        self.progress_frame.pack(expand="yes")
        
        self.settings_frame = ttk.Frame(self.root)
        self.settings_frame.pack(side="bottom", pady=20)
        self.mp4_mp3_frame = ttk.Frame(self.settings_frame)
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
                                            length=420,
                                            orient="horizontal",
                                            style="Horizontal.TProgressbar"
                                            )
        self.progressbar.pack(side="top", pady=20)
        
        #   ----    ----    mp3 or mp4    ----    ----
        self.mp3_or_mp4_label = ttk.Label(self.mp4_mp3_frame,
                                        font="bold 18",
                                        )
        self.mp3_or_mp4_label.pack(side="top")
        self.mp3_button = ttk.Button(self.mp4_mp3_frame,
                                    text = "mp3",
                                    #font="bold 15",
                                    command=self.mp3_command,
                                    style="MP3.TButton",
                                    takefocus=False
                                    )
        self.mp3_button.pack(side="left")
        self.mp4_button = ttk.Button(self.mp4_mp3_frame,
                                    text = "mp4",
                                    #font="bold 15",
                                    command=self.mp4_command,
                                    style="MP4.TButton",
                                    takefocus=False
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
        
        self.quality_option_menu = ttk.OptionMenu(
                                        self.settings_frame,
                                        self.option_var,
                                        #self.settings["video_quality"],
                                        *self.settings["all_video_quality"],
                                        #command=self.option_changed
                                        )
        self.quality_option_menu.pack(side="right")
        
        
        
        self.root.mainloop()
    
    
    
    def get_search(self) -> None:
        self.url = self.search_entry.get()
        self.dl.download_and_save_threads_manager(self.settings,
                                    self.url,
                                    self.start_progressbar,
                                    self.stop_progressbar
                                    )
    
    
    def start_progressbar(self) -> None:
        self.progressbar.start(10)
        if self.error_progressbar:
            self.error_progressbar = False
            self.style.configure(
                        "Horizontal.TProgressbar",
                        background = self.progressbar_color["background"],   # Vert doux (barre)
                        troughcolor = self.progressbar_color["troughcolor"],  # Beige clair (fond)
                        bordercolor = self.progressbar_color["bordercolor"],  # Bordure légère
                        lightcolor = self.progressbar_color["lightcolor"],   # Lumière
                        darkcolor = self.progressbar_color["darkcolor"],    # Ombre verte
                        )
    
    def stop_progressbar(self, error=False) -> None:
        self.progressbar.stop()
        if error:
            self.error_progressbar = True
            self.style.configure(
                        "Horizontal.TProgressbar",
                        background = self.progressbar_color["background_error"],   # Vert doux (barre)
                        troughcolor = self.progressbar_color["troughcolor"],  # Beige clair (fond)
                        bordercolor = self.progressbar_color["bordercolor"],  # Bordure légère
                        lightcolor = self.progressbar_color["lightcolor"],   # Lumière
                        darkcolor = self.progressbar_color["darkcolor"],    # Ombre verte
                        )
    
    def mp3_command(self) -> None:
        if not self.settings["audio_only"]:
            self.settings["audio_only"] = True
            self.style.configure("MP3.TButton",
                            background = self.colors["button_green"]
                            )
            self.style.configure("MP4.TButton",
                            background = self.colors["button_red"]
                            )
            self.mp3_or_mp4_label.config(text=".mp3")
            
            self.save_new_settings()
    
    def mp4_command(self) -> None:
        if self.settings["audio_only"]:
            self.settings["audio_only"] = False
            self.style.configure("MP4.TButton",
                            background = self.colors["button_green"]
                            )
            self.style.configure("MP3.TButton",
                            background = self.colors["button_red"]
                            )
            self.mp3_or_mp4_label.config(text=".mp4")
            
            self.save_new_settings()
    
    def mp3_or_mp4_check(self) -> None:
        if self.settings["audio_only"]:
            self.style.configure("MP3.TButton",
                            background = self.colors["button_green"]
                            )
            self.style.configure
            self.style.configure("MP4.TButton",
                            background = self.colors["button_red"]
                            )
            self.mp3_or_mp4_label.config(text=".mp3")
        
        elif not self.settings["audio_only"]:
            self.style.configure("MP4.TButton",
                            background = self.colors["button_green"]
                            )
            self.style.configure("MP3.TButton",
                            background = self.colors["button_red"]
                            )
            self.mp3_or_mp4_label.config(text=".mp4")
    
    def choice_of_folder(self) -> None:
        folder = filedialog.askdirectory()
        self.settings["save_folder"] = folder
        
        self.save_new_settings()
    
    def open_folder(self) -> None:
        filedialog.Directory()
    
    def change_quality(self,quality: str) -> None:
        
        self.save_new_settings()
    
    def save_new_settings(self) -> None:
        full_settings = {
            "current_settings" : self.settings,
            "original_settings": self.original_settings,
            "colors"           : {
                "default" : self.colors
            }
        }
        
        json.save_json("settings.json", full_settings)


if __name__ == "__main__":
    settings = json.get_json("settings.json")
    win = TkApp(settings=settings)