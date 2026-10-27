from datetime import date, timedelta

from wordle.words import WORDS, answer_for, is_valid, puzzle_number


def test_wordlist_loads():
    assert len(WORDS) > 1000
    assert all(len(w) == 5 and w.isalpha() and w.islower() for w in WORDS)


def test_is_valid():
    assert is_valid("crane")
    assert not is_valid("zzzzz")


def test_answer_is_stable_for_a_day():
    day = date(2026, 10, 27)
    assert answer_for(day) == answer_for(day)
    assert is_valid(answer_for(day))


def test_answers_do_not_repeat_until_list_exhausted():
    start = date(2026, 1, 1)
    answers = [answer_for(start + timedelta(days=i)) for i in range(len(WORDS) + 1)]
    assert len(set(answers[:-1])) == len(WORDS)
    assert answers[-1] == answers[0]


def test_puzzle_number():
    assert puzzle_number(date(2026, 1, 1)) == 1
    assert puzzle_number(date(2026, 1, 31)) == 31
