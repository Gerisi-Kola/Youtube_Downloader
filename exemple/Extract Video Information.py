import yt_dlp

def get_video_info(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

# Usage
info = get_video_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
print(f"Title: {info['title']}")
print(f"Duration: {info['duration']} seconds")