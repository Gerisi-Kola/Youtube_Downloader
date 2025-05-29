import yt_dlp
import subprocess

def fini():
    print("fini !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

def launch_download(download_ops,url):
    with yt_dlp.YoutubeDL(download_ops) as ydl:
        ydl.download([url])
        
        fini()


def get_url_info(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url=url,download=False)
        
        print(info.get("thumbnail"))
        video_info = {
            "title" : info.get("title"),
            "thumbnail" : info.get("thumbnail")
        }
        fini()
        return video_info

#"https://www.youtube.com/watch?v=2zjwbTaiwNQ"

def launch_download_sub(yt):
    #return subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True, shell=True)
    #mv = ["&&", "mv", f"./tmp{title}", f"{path}/{title}"]
    #yt += mv
    try:
        print(yt)
        a = subprocess.run(yt, capture_output=True, text=True, shell=True)
        #print(f"./tmp{title} \n {path}/{title}")
        #subprocess.run(["mv", f"./tmp{title}", f"{path}/{title}"], capture_output=True, text=True, shell=True)
        return a
    except Exception as e:
        print(e)

if __name__ == "__main__":
    """def my_hook(d):
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
    
    launch_download(ydl_opts,url)"""
    #print(get_url_info())
    #yt = ["yt-dlp", "-f bv*[height>=360]+ba", "-x", "https://www.youtube.com/watch?v=dQw4w9WgXcQ","-P ", "-ovideos/%(title)s.%(ext)s"]
    yt = ["yt-dlp", "-f bv*[height>=quality]+ba", "-x","--audio-format mp3", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "-P ./tmp", "-o./videos/%(title)s.%(ext)s"]
    print(launch_download_sub(yt))