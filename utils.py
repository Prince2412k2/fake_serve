import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import random
from static import places, characters
import json


def load() -> None:
    nltk.download("punkt")


def count_tokens(sentence: str) -> int:
    return len(word_tokenize(sentence))


async def get_chars() -> dict[str, dict]:
    num_of_char = random.randint(1, 9)
    indexs = [random.randint(1, 49) for _ in range(num_of_char)]
    output_chars = {characters[i][0]: characters[i][1] for i in indexs}
    return {"characters": output_chars}


async def get_places() -> dict[str, dict]:
    num_of_place = random.randint(1, 5)
    indexs = [random.randint(1, 49) for _ in range(num_of_place)]
    output_places = {places[i][0]: places[i][1] for i in indexs}
    return {"places": output_places}


async def get_summary(text: str) -> dict[str, str]:
    sentances = text.split(".")

    length = random.randint(len(sentances) // 4, len(sentances) // 2)
    start = random.randint(0, len(sentances) // 4)
    sentances = sentances[start:length]
    return {"summary": ".".join(sentances)}


if __name__ == "__main__":
    load()
    from test import text

    print(get_summary(text))
