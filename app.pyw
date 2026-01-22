import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText # Create the text box
#    ----    ----
import path
import download_manager
import files_controller as File
from stdout import RedirectText # Transfer the print to the text box


class TkApp:
    def __init__(self, settings: dict):
        #   ----    ----    Settings   ----    ----
        self.SETTINGS          = dict(settings["current_settings"])
        self.ORIGINAL_SETTINGS = dict(settings["original_settings"])
        self.COLORS            = dict(settings["colors"]["default"])
        self.BNT_COLORS        = dict(self.COLORS["button_colors"])
        self.PROGRESSBAR_COLOR = dict(self.COLORS["progressbar"])
        self.PATHS             = dict(settings["paths"])
        self.SETTINGS["tmp_folder_absolut"] = path.get_absolut_path(self.SETTINGS["tmp_folder"])
        
        #   ----    ----    Window creation   ----    ----
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Youtube mp4/mp3")
        self.root.configure(background = self.COLORS["bg"])
        title_label = tk.Label(self.root,text="YouTube Downloader", bg=self.COLORS["bg"], font="bold 20")
        title_label.pack(pady=30)
        try:
            path.taskbar_icon()
            self.root.iconbitmap(self.PATHS['ico'])
        except Exception as e:
            print(f"Can not load ico : {e}")
        
        self.url = "" #'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        self.error_progressbar = False
        self.dl = download_manager.DowloadManager()
        
        #   ----    ----  Style   ----    ----
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton",
                            padding=11,
                            background=self.BNT_COLORS["background"],
                            troughcolor=self.BNT_COLORS["troughcolor"],
                            bordercolor=self.BNT_COLORS["bordercolor"],
                            lightcolor=self.BNT_COLORS["lightcolor"],
                            darkcolor=self.BNT_COLORS["darkcolor"]
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
                            background = self.PROGRESSBAR_COLOR["background"],   # Barre
                            troughcolor = self.PROGRESSBAR_COLOR["troughcolor"],  # Fond
                            bordercolor = self.PROGRESSBAR_COLOR["bordercolor"],  # Bordure légère
                            lightcolor = self.PROGRESSBAR_COLOR["lightcolor"],   # Lumière
                            darkcolor = self.PROGRESSBAR_COLOR["darkcolor"],    # Ombre verte
                            )
        self.style.configure("TFrame",
                            background=self.COLORS["bg"],
                            )
        self.style.configure("TLabel",
                            background=self.COLORS["bg"]
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
        
        self.stdout_frame = ttk.Frame(self.root)
        self.stdout_frame.pack(side="bottom",fill="x")
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
                                    command=self.mp3_command,
                                    style="MP3.TButton",
                                    takefocus=False
                                    )
        self.mp3_button.pack(side="left")
        self.mp4_button = ttk.Button(self.mp4_mp3_frame,
                                    text = "mp4",
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
                                            (self.SETTINGS["save_folder"]),
                                    takefocus=False
                                    )
        self.open_folder_button.pack(expand="yes",side="left")
        
        #   ----    ----    Quality    ----    ----
        # set up variable
        self.option_var = tk.StringVar(self.root)
        
        self.quality_option_menu = ttk.OptionMenu(
                                        self.settings_frame,
                                        self.option_var,
                                        self.SETTINGS["video_quality"],
                                        *self.SETTINGS["all_video_quality"],
                                        command=self.change_quality
                                        )
        self.quality_option_menu.pack(side="right")
        
        #   ----    ----    Standard Output    ----    ----
        # Creation of the text box
        text = ScrolledText(self.stdout_frame, height=8, state="disabled")
        text.pack(side="bottom",fill="x")#padx=10, pady=10)
        # Define the text box as the standard output
        stdout = RedirectText(text)
        sys.stdout = stdout
        sys.stderr = stdout
        
        
        self.root.mainloop()
    
    
    
    def get_search(self) -> None:
        """ Get the text wrote by the user in the 'search bar' """
        self.url = self.search_entry.get()
        self.dl.download_and_save_threads_manager(self.SETTINGS,
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
                        background = self.PROGRESSBAR_COLOR["background"],
                        )
    
    def stop_progressbar(self, error=False) -> None:
        self.progressbar.stop()
        if error:
            self.error_progressbar = True
            self.style.configure(
                        "Horizontal.TProgressbar",
                        background = self.PROGRESSBAR_COLOR["background_error"],
                        )
    
    def mp3_command(self) -> None:
        if not self.SETTINGS["audio_only"]:
            self.SETTINGS["audio_only"] = True
            self.style.configure("MP3.TButton",
                            background = self.COLORS["button_green"]
                            )
            self.style.configure("MP4.TButton",
                            background = self.COLORS["button_red"]
                            )
            self.mp3_or_mp4_label.config(text=".mp3")
            
            self.save_new_settings()
    
    def mp4_command(self) -> None:
        if self.SETTINGS["audio_only"]:
            self.SETTINGS["audio_only"] = False
            self.style.configure("MP4.TButton",
                            background = self.COLORS["button_green"]
                            )
            self.style.configure("MP3.TButton",
                            background = self.COLORS["button_red"]
                            )
            self.mp3_or_mp4_label.config(text=".mp4")
            
            self.save_new_settings()
    
    def mp3_or_mp4_check(self) -> None:
        if self.SETTINGS["audio_only"]:
            self.style.configure("MP3.TButton",
                            background = self.COLORS["button_green"]
                            )
            self.style.configure
            self.style.configure("MP4.TButton",
                            background = self.COLORS["button_red"]
                            )
            self.mp3_or_mp4_label.config(text=".mp3")
        
        elif not self.SETTINGS["audio_only"]:
            self.style.configure("MP4.TButton",
                            background = self.COLORS["button_green"]
                            )
            self.style.configure("MP3.TButton",
                            background = self.COLORS["button_red"]
                            )
            self.mp3_or_mp4_label.config(text=".mp4")
    
    def choice_of_folder(self) -> None:
        """ Open the file explorer and ask to choice a folder """
        folder = filedialog.askdirectory()
        self.SETTINGS["save_folder"] = folder
        
        self.save_new_settings()
    
    def open_folder(self) -> None:
        """ Open the file explorer in the current folder """
        filedialog.Directory()
    
    def change_quality(self,quality: str) -> None:
        print(f"quality changed to {quality}")
        self.SETTINGS["video_quality"] = quality
        self.save_new_settings()
    
    def save_new_settings(self) -> None:
        """ Update the settings and save it in settings.json """
        full_settings = {
            "current_settings" : self.SETTINGS,
            "original_settings": self.ORIGINAL_SETTINGS,
            "colors"           : {
                "default" : self.COLORS
            }
        }
        
        File.save_json(self.PATHS["settings_file"], full_settings)


if __name__ == "__main__":
    settings = File.get_json("settings.json")
    win = TkApp(settings=settings)