from yt_dlp import YoutubeDL
import multiprocessing
from os import path, listdir
from bs4 import BeautifulSoup

url = 'https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg'
query = 'жак'
directory = path.dirname(__file__)
download_dir = f'{directory}/downloads'
ydl_opts = {
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ['ru'],
    "subtitlesformat": 'srv3',
    "outtmpl": f'{download_dir}/%(id)s',
    "skip_download": True
}


def subtitles_download(video_info):
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_info['url'])


def search_query(query: str):
    list_files = listdir(download_dir)

    for file in list_files:
        yt_link = f'https://www.youtube.com/watch?v={file.split(".")[0]}'

        with open(f'{download_dir}/{file}', encoding="utf-8") as f:
            soup = BeautifulSoup(f, 'html.parser')
            paragraphes = soup.find_all('p')
            for paragraph in paragraphes:
                if paragraph.get_text().find(query) != -1:
                    print(f'{yt_link}&t={paragraph.get("t")}ms')


def main():
    with YoutubeDL({"extract_flat": True, "skip_download": True}) as ydl:
        videos_info = ydl.extract_info(url=url, download=False)['entries']

    with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
        process.map(subtitles_download, videos_info)

    search_query(query)


if __name__ == "__main__":
    main()
