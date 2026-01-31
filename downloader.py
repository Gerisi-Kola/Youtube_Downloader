import yt_dlp
import subprocess
import sys

def get_url_info(url: str) -> dict:
    """ Use yt-dlp embed to get the thumbnail and the title and return a dict of them
        {
        'title'     = str(...)
        'thumbnail' = ???
        }"""
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url=url,download=False) # why it start download ?
        
        print(info.get("thumbnail"))
        video_info = {
            "title" : info.get("title"),
            "thumbnail" : info.get("thumbnail")
        }
        return video_info

def launch_download_python(download_ops: dict, url: str, stop_progressbar) -> None:
    """ Download using python embed"""
    with yt_dlp.YoutubeDL(download_ops) as ydl:
        ydl.download([url])
    stop_progressbar()

def launch_download_sub(yt: dict, stop_progressbar) -> None:
    """ Download using subprocess and yt-dlp"""
    print(yt)
    with subprocess.Popen(yt,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1,) as process:
        for line in process.stdout:
            # ici tu passes explicitement par sys.stdout
            sys.stdout.write(line)
    stop_progressbar()
    return

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
    """yt = ["yt-dlp", "-f", "bv*[height>=quality]+ba", "-x","--audio-format", "mp3", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "-P", "./tmp", "-o./videos/%(title)s.%(ext)s"]
    print(launch_download_sub(yt))"""
    get_url_info(r"https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1")