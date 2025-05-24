import yt_dlp

def convert_settings_for_yt_dlp(settings):
    print(settings)
    ydl_opts = {}
    print(ydl_opts)
    quality = settings["video_quality"]
    temp_dir = settings["working_folder_absolut"]
    
    # -------    mp3 or mp4     -------
    ydl_opts['paths'] = {'home' : settings["save_folder"], 'temp': temp_dir}  # Tous les fichiers temporaires seront ici
    if settings["audio_only"]:
        ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        #'preferredquality': '192'
                        }]
        
        #ydl_opts['merge_output_format'] = 'mp4' 
    else:
        ydl_opts['merge_output_format'] = 'mp4'
    
    # -------    Folder     -------
    ydl_opts['outtmpl']= f"%(title)s.%(ext)s"
    
    # -------    Video quality     -------
    if quality == "best":
        ydl_opts['format'] = "best"
    else :
        ydl_opts['format'] =  f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
    
    
    
    #print(ydl_opts)
    return ydl_opts



if __name__ == "__main__":
    from json_controler import get_settings
    
    def fini():
        print("fini !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    settings = get_settings("settings.json")
    settings = settings["current_settings"]
    
    ydl_opts = convert_settings_for_yt_dlp(settings)
    
    """ydl_opts = {
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        #'preferredquality': '192'
        }],
    'progress_hooks': [my_hook],
    'merge_output_format': 'mp4',
    'outtmpl': f'{"./videos"}/%(title)s.%(ext)s',
    'format': 'bestvideo[height<=144]+bestaudio/best[height<=144]',
    }"""
    
    
    def launch_download(ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])#'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            #info = ydl.extract_info(url=url)
            
            #print(info.get("thumbnail"))
            fini()
    
    launch_download(ydl_opts)