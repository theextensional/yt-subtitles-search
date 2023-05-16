import json
import os


def search_in_json(files_list: list[str], search_list: list[str]) -> tuple[int, dict[str, list[int]]]:
    matches = {}
    count = 0

    if not search_list or not files_list:
        raise ValueError("Некорректные входные данные")

    for filepath in files_list:
        video_id = os.path.splitext(os.path.basename(filepath))[0].split(".")[0]
        with open(filepath, "r") as file:
            data = json.load(file)["events"]

        count_search_list = len(search_list) - 1
        index, start, found = 0, 0, False

        for event in data:
            segs = event.get("segs", [])
            for seg in segs:
                text = seg.get("utf8", "").strip().lower()
                if text in ["\n", "[музыка]"]:
                    continue

                if text == search_list[index]:
                    if index == 0 and not found:
                        start = event["tStartMs"]
                        count += 1
                    if index == count_search_list:
                        matches.setdefault(video_id, []).append(start)
                        index = 0
                        found = True
                    if index < count_search_list:
                        index += 1
                else:
                    index = 0
                    found = False

    return count, matches
