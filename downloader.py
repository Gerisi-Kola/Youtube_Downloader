import yt_dlp
import os

def fini():
    print("fini !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

def launch_download(download_ops,url):
    with yt_dlp.YoutubeDL(download_ops) as ydl:
        #ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        info = ydl.extract_info(url=url)
        
        title = info.get("title")
        
        print(info.get("thumbnail"))
        video_info = {
            "title" : info.get("title"),
            "thumbnail" : info.get("thumbnail")
        }
        fini()
        return video_info




def move_video_to_folder(settings,video_info):
    folder = settings["working_folder"] # --------------
    
    title = video_info["title"]
    
    cwd = os.getcwd()
    
    if settings["audio_only"]:
        extention = ".mp3"
    else:
        extention = ".mp4"
    
    file = cwd+folder[1:]+"/"+title+extention
    
    file = file.replace("\\", "/")
    
    print(file)
    
    if os.path.isfile(file):
        print(" is file --------")
        try:
            os.rename(file, folder+"/"+title+extention)
            print("renamed")
        except:
            print("cannot rename")
    else:
        print("no file ---------")
    
    """if "D:/Programation/Python/Youtube_Dawnload/working_progress/Rick Astley - Never Gonna Give You Up (Official Music Video).mp3" == file:
        print("True +++++++")
    else:
        print("false +++++++++++++")"""



if __name__ == "__main__":
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
            
    ydl_opts = {
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            #'preferredquality': '192'
            }],
        'progress_hooks': [my_hook],
        'merge_output_format': 'mp4',
        'outtmpl': f'{"./videos"}/%(title)s.%(ext)s',
        'format': 'bestvideo[height<=144]+bestaudio/best[height<=144]',
    }
    url = "https://youtu.be/M2sUoA7FaEs?si=iJUFq5ztrVSZ7Mx"#"https://youtu.be/M2sUoA7FaEs?si=iJUFq5ztrVSZ7MxW"
    
    launch_download(ydl_opts,url)