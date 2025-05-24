import yt_dlp

ydl_opts = {
    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])