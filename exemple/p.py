import yt_dlp

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'progress_hooks': [my_hook],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])
    info = ydl.extract_info(url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',download=False)
    
    print(info.get("thumbnail"))