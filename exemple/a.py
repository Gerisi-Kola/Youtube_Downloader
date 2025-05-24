import yt_dlp

# URL de la vidéo YouTube
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Options (ici : meilleure qualité)
ydl_opts = {
    'format': 'best',
    'outtmpl': 'videos/%(title)s.%(ext)s'  # nom et dossier de sortie
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
