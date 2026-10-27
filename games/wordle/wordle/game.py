from collections import Counter
from enum import StrEnum

WORD_LENGTH = 5
MAX_GUESSES = 6


class LetterState(StrEnum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"


def score(guess: str, answer: str) -> list[LetterState]:
    # Only answer letters not matched exactly can turn a misplaced guess letter yellow,
    # so repeated letters are never marked present more often than the answer contains them.
    remaining = Counter(a for g, a in zip(guess, answer) if g != a)
    result = []
    for g, a in zip(guess, answer):
        if g == a:
            result.append(LetterState.CORRECT)
        elif remaining[g]:
            remaining[g] -= 1
            result.append(LetterState.PRESENT)
        else:
            result.append(LetterState.ABSENT)
    return result
