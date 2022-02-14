import os
from bs4 import BeautifulSoup

# Тут внимательно! Следить руками:
# что бы video_id в yt_link совпадало с video_id первого файла в директории path
yt_link = "https://www.youtube.com/watch?v=0TJLkZZd_ds&t="
search_words = "вами"

# Get the list of all files and directories
path = "./subs/"
dir_list = os.listdir(path)

all_words = []
all_times = []

# код ниже ищет заданные search_words
# ТОЛЬКО в автоматически сгенерированных субтитрах
# и ТОЛЬКО в первом файле директории subs
for file in dir_list[:1]:
    with open(path+file, encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')

        paragraphes = soup.find_all('p')
        for paragraph in paragraphes:
            p_time = paragraph.get('t')

            words = paragraph.find_all('s')
            if not words:
                continue

            for word in words:
                w_time = paragraph.get('t')
                w_time = w_time if not None else p_time

                all_words.append(word.text.strip())
                all_times.append(w_time)

timeByWordIndex = {}
string_of_all_words = ''
for idx, word in enumerate(all_words):
    string_of_all_words += word + ' '
    timeByWordIndex[len(string_of_all_words)] = all_times[idx]

res = -1
answers = []
while True:
    res = string_of_all_words.find(search_words, res + 1)
    if res == -1:
        break
    index = string_of_all_words[:res].rfind(' ') + 1
    answers.append(timeByWordIndex[index])

for timems in answers:
    print(yt_link + timems + 'ms')
