# yt-subtitles

**yt-subtitles** - консольная программа для поиска по субтитрам YouTube видео.

![Example](./example.png)

## Подготовка

### Клонирование/создание репозитория проекта

```sh
git clone https://github.com/TVP-Support/yt-subtitles.git
```

```sh
cd yt-subtitles
```

### Установка зависимостей

```sh
pip install -r requirements.txt
```

## Использование

```sh
/bin/python /path/to/yt-subtitles <URL> <QUERY|QUERIES>
```

Пример:

```sh
/bin/python /path/to/yt-subtitles https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg Жак
```

Пример с несколькими запросами:

```sh
/bin/python /path/to/yt-subtitles https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg Жак Вода
```

### Параметр `-h` или `--help`  выводит описание доступных команд и параметров

```sh
/bin/python /path/to/yt-subtitles -h
```

### Параметр `-o` или `--open`  открывает файл с сохраненными результатами после окончания работы скрипта

```sh
/bin/python /path/to/yt-subtitles <URL> <QUERY|QUERIES> -o
```
