from yt_dlp import YoutubeDL

# # Речь в Стокгольме
# url = "https://www.youtube.com/watch?v=SMecXHg2y-A"
# # Э, что такое ОС
# url2 = "https://www.youtube.com/watch?v=FyQzGimAH-s"
# # Последнияя книга Жака Фреско
# url3 = "https://www.youtube.com/watch?v=8uKVrtUstSA"

# Канал Экстенсиональный
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
