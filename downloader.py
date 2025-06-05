import yt_dlp
import subprocess

def get_url_info(url: str) -> dict:
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url=url,download=False)
        
        print(info.get("thumbnail"))
        video_info = {
            "title" : info.get("title"),
            "thumbnail" : info.get("thumbnail")
        }
        return video_info

def launch_download_python(download_ops: dict, url: str, stop_progressbar) -> None:
    with yt_dlp.YoutubeDL(download_ops) as ydl:
        ydl.download([url])
    stop_progressbar()

def launch_download_sub(yt: dict, stop_progressbar) -> None:
    print(yt)
    a = subprocess.run(yt, capture_output=True, text=True, shell=True)
    stop_progressbar()
    return a


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