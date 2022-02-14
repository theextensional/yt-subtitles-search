import os
from os import sep
from bs4 import BeautifulSoup


def search_query(search_words, file):
    video_id = file.split(sep)[-1].split('.')[0]
    yt_link = f"https://www.youtube.com/watch?v={video_id}&t="

    all_words = []
    all_times = []

    with open(file, encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')

        paragraphes = soup.find_all('p')
        for paragraph in paragraphes:
            p_time = int(paragraph.get('t'))

            words = paragraph.find_all('s')
            if not words:
                continue

            for word in words:
                w_time = word.get('t')
                if w_time is None:
                    w_time = 0
                else:
                    w_time = int(w_time)

                all_words.append(word.text.strip())
                all_times.append(w_time + p_time)

    timeByWordIndex = {}
    string_of_all_words = ''
    for idx, word in enumerate(all_words):
        timeByWordIndex[len(string_of_all_words)] = all_times[idx]
        string_of_all_words += word + ' '

    res = -1
    answers = []
    while True:
        res = string_of_all_words.find(search_words, res + 1)
        if res == -1:
            break
        index = string_of_all_words[:res].rfind(' ') + 1
        answers.append(timeByWordIndex[index])

    for timems in answers:
        print(yt_link + str(timems) + 'ms')


def main(query, file):
    search_query(query, file)


if __name__ == '__main__':
    main()
