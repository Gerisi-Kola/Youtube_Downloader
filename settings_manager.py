import yt_dlp
import path as p

def convert_settings_for_yt_dlp(settings):
    print(settings)
    ydl_opts = {}
    print(ydl_opts)
    quality = settings["video_quality"]
    temp_dir = settings["tmp_folder_absolut"]
    
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


def convert_settings_for_yt_dlp_sub(settings,url):
    ydl_opts = ["yt-dlp"]
    audio_only = settings["audio_only"]
    tmp = settings["tmp_folder_absolut"]
    path = p.get_absolut_path(settings["save_folder"])
    quality = settings["video_quality"]
    
    # mp3 or mp4
    if audio_only:
        print("mp3")
        ydl_opts.append(f"-f bv*[height<={quality}]+ba")
        ydl_opts.append("-x")
        ydl_opts.append("--audio-format")
        ydl_opts.append("mp3")
    
    # Quality Video
    else:
        print("mp4")
        if quality == "144":
            q = "160"
        elif quality == "360":
            q = "134"
        elif quality == "480":
            q = "135"
        elif quality == "720":
            q = "136"
        elif quality == "1080":
            q = "137"
        else:
            q = "22" #best ?
        
        ydl_opts.append(f"-f {q}")
    
    # URL
    ydl_opts.append(f"{url}")
    
    # temporary 
    ydl_opts.append(f"-P")
    ydl_opts.append(f"{tmp}")
    
    if settings["audio_only"] == True:
        title = f"-o%(title)s.mp3"
        ydl_opts.append(f"-o%(title)s.%(ext)s")
    else:
        ydl_opts.append(f"-o%(title)s.%(ext)s")
        title = f"-o%(title)s.mp4"
    
    ydl_opts.append("--output")
    ydl_opts.append(f"{path}/%(title)s.mp4")
    
    return ydl_opts

if __name__ == "__main__":
    from json_controler import get_json
    import downloader as d
    
    def fini():
        print("fini !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    settings = get_json("settings.json")
    settings = settings["current_settings"]
    
    ydl_opts,title,path = convert_settings_for_yt_dlp_sub(settings, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    #print(ydl_opts)
    d.launch_download_sub(ydl_opts)
    
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
    
    
    """def launch_download(ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])#'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            #info = ydl.extract_info(url=url)
            
            #print(info.get("thumbnail"))
            fini()
    
    launch_download(ydl_opts)"""