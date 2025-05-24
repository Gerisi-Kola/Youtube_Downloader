import yt_dlp

def download_video(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Usage
download_video('https://www.youtube.com/watch?v=dQw4w9WgXcQ')