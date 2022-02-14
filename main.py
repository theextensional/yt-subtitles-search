from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import os
from os import sep

# url может принимать ссылку на канал, плейлист или поисковой запрос в форме:
# 'ytsearch24:поисковой запрос'
# где 24 - это кол-во результатов по запросу
url = 'https://www.youtube.com/channel/UCY6zVRa3Km52bsBmpyQnk6A'

# если запрос в списке один -
# в консоль выведутся таймкоды, где произносится текст этого запроса
# если запросов в списке несколько -
# в консоль выведутся видео, субтитры которых содержат все из перечисленных запросов
queries = ['температур']

path_subs = os.path.abspath('./subs')

with YoutubeDL({"extract_flat": True, "skip_download": True}) as ydl:
    res = ydl.extract_info(url)


def search_query(queries, file):
    video_id = file.split(sep)[-1].split('.')[0]
    yt_link = f'https://www.youtube.com/watch?v={video_id}'

    with open(file, encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')

    if len(queries) == 1:

        query = queries[0]
        paragraphes = soup.find_all('p')
        for paragraph in paragraphes:
            if paragraph.get_text().find(query) != -1:
                print(f'{yt_link}&t={paragraph.get("t")}ms')

    else:

        def is_full_match(queries, subs_text):
            for query in queries:
                if subs_text.find(query) == -1:
                    return False
            return True

        subs_text = soup.get_text()
        if is_full_match(queries, subs_text):
            print(yt_link)


ydl_opts = {
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ['ru'],
    "subtitlesformat": 'srv3',
    "outtmpl": path_subs + os.sep + '%(id)s',
    "skip_download": True,
    "quiet": True
}

for i in res["entries"]:
    file = path_subs + os.sep + i['id'] + '.ru.srv3'
    if not os.path.isfile(file):
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(i['url'])
    if os.path.isfile(file):
        search_query(queries, file)
