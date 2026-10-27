import random
from datetime import date
from importlib.resources import files

EPOCH = date(2026, 1, 1)

WORDS: tuple[str, ...] = tuple(
    sorted(files("wordle").joinpath("data", "wordlist").read_text().split())
)
_WORD_SET = frozenset(WORDS)

# A fixed shuffle of the list: puzzle N gets the N-th word, so no answer repeats until every word is used.
# Changing the seed or the word list reshuffles every past and future answer.
_SCHEDULE: tuple[str, ...] = tuple(random.Random(0).sample(WORDS, len(WORDS)))


def is_valid(word: str) -> bool:
    return word in _WORD_SET


def answer_for(day: date) -> str:
    return _SCHEDULE[(puzzle_number(day) - 1) % len(_SCHEDULE)]


def puzzle_number(day: date) -> int:
    return (day - EPOCH).days + 1
