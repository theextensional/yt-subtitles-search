import string


def clean_text(text: str) -> list[str]:
    """
    Принимает строку и возвращает список слов без знаков пунктуации и в нижнем регистре.
    """
    return text.translate(str.maketrans("", "", string.punctuation)).lower().split()
