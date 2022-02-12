# import OS module
import os
from bs4 import BeautifulSoup

# Get the list of all files and directories
path = "./subs/"

dir_list = os.listdir(path)

all_words = []
all_times = []
words_list = []

for file in dir_list[:1]:
    with open(path+file) as f:
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

                words_list.append(w_time + ':' + word.text.strip())
                all_words.append(word.text.strip())
                all_times.append(w_time)

all_text = ' '.join(all_words)
# print(all_text)
# print(all_times)
# print(words_list)

tt = {}
s = ''
for idx, word in enumerate(all_words):
    s += word + ' '
    tt[len(s)] = all_times[idx]

# print(s)
# print(tt)

# s1 = "вот такую штуку"
s1 = "вот так"

res = -1
answers = []
while True:
    res = s.find(s1, res+1)
    if res == -1:
        break
    answers.append(tt[res])

# print(res)
# print(tt[res])
print(answers)
yt_link = "https://www.youtube.com/watch?v=prPeDmN4JnU&t="
for timems in answers:
    print(yt_link + timems + 'ms')
