# Поиск текста по субтитрам YouTube

**yt-subtitles-search** - консольная программа для поиска по субтитрам YouTube видео.

![Example](./example.png)

## Подготовка

### Клонирование/создание репозитория проекта

```sh
git clone https://github.com/TVP-Support/yt-subtitles-search.git
```

```sh
cd yt-subtitles-search
```

### Установка зависимостей

```sh
pip install -r requirements.txt
```

## Использование

```sh
python main.py <URL> <QUERY|QUERIES>
```

Пример:

```sh
python main.py 'https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg' 'вода'
```

Пример с несколькими словами:

```sh
python main.py 'https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg' 'вентилятор с'
```

### Параметр `-h` или `--help`  выводит описание доступных команд и параметров

```sh
python main.py -h
```

### Параметр `-o` или `--open`  открывает файл с сохраненными результатами после окончания работы скрипта

```sh
/bin/python /path/to/yt-subtitles <URL> <QUERY|QUERIES> -o
```
