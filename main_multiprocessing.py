import multiprocessing
from os import listdir, path

from bs4 import BeautifulSoup
from yt_dlp import DownloadError, YoutubeDL

# playlist "Эффективность"
url = 'https://www.youtube.com/playlist?list=PLa2WHSYysn_EV0SHkXiB2TRLi-31x8Pcy'
query = 'робот'
# Творчество, воображение, оригинальность - Жак Фреско [Цикл лекций]
url = 'https://www.youtube.com/watch?v=l0WtRwYNVb0'
query = 'крыша'

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


def subtitles_download(info):
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(info['url'])
    except DownloadError:
        print(f'❌ DonwloadError')
        return


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
        videos_info = ydl.extract_info(url=url, download=False)
        try:
            videos_info = videos_info['entries']
            # with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
            with multiprocessing.Pool(16) as process:
                process.map(subtitles_download, videos_info)
        except KeyError:
            videos_info = ydl.extract_info(url=url, download=False)
            videos_info['url'] = videos_info['original_url']
            subtitles_download(videos_info)

        search_query(query)


if __name__ == "__main__":
    main()
