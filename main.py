from yt_dlp import YoutubeDL

url = 'https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg/videos'

ydl_opts = {
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ['ru'],
    "subtitlesformat": 'srv3',
    "outtmpl": './subs/%(title)s.f%(format_id)s.%(ext)s',
    "skip_download": True
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
