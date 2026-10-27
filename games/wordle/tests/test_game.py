import pytest

from wordle.game import LetterState, score

C, P, A = LetterState.CORRECT, LetterState.PRESENT, LetterState.ABSENT


@pytest.mark.parametrize(
    ("guess", "answer", "expected"),
    [
        ("crane", "crane", [C, C, C, C, C]),
        ("found", "crane", [A, A, A, C, A]),
        ("nacre", "crane", [P, P, P, P, C]),
        # Repeated guess letters only light up as often as the answer contains them.
        ("speed", "abide", [A, A, P, A, P]),
        ("eerie", "there", [P, A, P, A, C]),
        ("lolly", "hello", [A, P, C, C, A]),
        ("hello", "lolly", [A, A, C, C, P]),
    ],
)
def test_score(guess, answer, expected):
    assert score(guess, answer) == expected
