from yt_dlp import YoutubeDL
from subs_parse import search_query
import os

path_subs = os.path.abspath('./subs')

url = 'https://www.youtube.com/c/DesigningTheFuture'
query = 'общей'

with YoutubeDL({"extract_flat": True, "skip_download": True}) as ydl:
    res = ydl.extract_info(url)

ydl_opts = {
    #  "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ['ru'],
    "subtitlesformat": 'srv3',
    "outtmpl": './subs/%(id)s',
    "skip_download": True,
    "quiet": True
}

for i in res["entries"]:
    if not os.path.isfile('./subs/' + i["id"] + '.ru.srv3'):
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(i["url"])
    if os.path.isfile('./subs/' + i["id"] + '.ru.srv3'):
        search_query(query, path_subs + os.sep + i["id"] + ".ru.srv3")
