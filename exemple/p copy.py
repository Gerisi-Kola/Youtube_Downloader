import yt_dlp

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
    'format': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
    
}


def fini():
    print("fini !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    info = ydl.extract_info(url="https://youtu.be/M2sUoA7FaEs?si=iJUFq5ztrVSZ7MxW")
    
    print(info.get("thumbnail"))
    fini()