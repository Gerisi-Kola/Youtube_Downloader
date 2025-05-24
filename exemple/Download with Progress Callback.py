import yt_dlp

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
    elif d['status'] == 'downloading':
        print(f"Downloading: {d['filename']} - {d['_percent_str']} complete")

ydl_opts = {
    'progress_hooks': [my_hook],
    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])