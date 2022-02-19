import json
import sys
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import os
from os import sep
import logging

# logging_level = logging.DEBUG
logging_level = logging.INFO
logging.basicConfig(format=f'%(levelname)s: %(message)s', level=logging_level)


# url может принимать ссылку на канал, плейлист или поисковой запрос в форме:
# 'ytsearch24:поисковой запрос'
# где 24 - это кол-во результатов по запросу
url = 'https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg'

# если запрос в списке один -
# в консоль выведутся таймкоды, где произносится текст этого запроса
# если запросов в списке несколько -
# в консоль выведутся видео, субтитры которых содержат все из перечисленных запросов
queries = ['фреско']

path_subs = 'subs'

with YoutubeDL({"extract_flat": True, "skip_download": True}) as ydl:
    videos_info = ydl.extract_info(url=url, download=False)
    # logging.debug(videos_info)


def search_query(queries, file):
    video_id = file.split('/')[-1].split('.')[0]
    yt_link = f'https://www.youtube.com/watch?v={video_id}'

    with open(file, encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')

    if len(queries) == 1:

        query = queries[0]
        paragraphes = soup.find_all('p')
        for paragraph in paragraphes:
            if paragraph.get_text().find(query) != -1:
                logging.info(f'{yt_link}&t={paragraph.get("t")}ms')

    else:

        def is_full_match(queries, subs_text):
            for query in queries:
                if subs_text.find(query) == -1:
                    return False
            return True

        subs_text = soup.get_text()
        if is_full_match(queries, subs_text):
            logging.info(yt_link)


ydl_opts = {
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ['ru'],
    "subtitlesformat": 'srv3',
    "outtmpl": f'{path_subs}/%(id)s',
    "skip_download": True,
    "quiet": True
}

for video_info in videos_info['entries']:
    file = f'{path_subs}/{video_info["id"]}.ru.srv3'
    if not os.path.isfile(file):
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_info['url'])
    if os.path.isfile(file):
        search_query(queries, file)
