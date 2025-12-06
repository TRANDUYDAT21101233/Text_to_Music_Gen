import yt_dlp
def extract_audio(youtube_url, output_filename="output_audio"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

extract_audio("https://youtu.be/cBKAmZjRRDI?si=GmmvcB1KOAmZ4gvd")
