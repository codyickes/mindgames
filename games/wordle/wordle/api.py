from datetime import UTC, date, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field, StringConstraints

from wordle.game import MAX_GUESSES, WORD_LENGTH, LetterState, score
from wordle.words import answer_for, is_valid, puzzle_number

app = FastAPI(title="Wordle")

Word = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=WORD_LENGTH,
        max_length=WORD_LENGTH,
        pattern=r"^[A-Za-z]+$",
    ),
]


def get_today() -> date:
    return datetime.now(UTC).date()


Today = Annotated[date, Depends(get_today)]


class Daily(BaseModel):
    date: date
    puzzle_number: int
    word_length: int
    max_guesses: int


class GuessRequest(BaseModel):
    guess: Word
    attempt: int = Field(ge=1, le=MAX_GUESSES)
    date: date | None = None


class LetterResult(BaseModel):
    letter: str
    state: LetterState


class GuessResponse(BaseModel):
    guess: str
    letters: list[LetterResult]
    solved: bool
    answer: str | None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/daily")
def daily(today: Today) -> Daily:
    return Daily(
        date=today,
        puzzle_number=puzzle_number(today),
        word_length=WORD_LENGTH,
        max_guesses=MAX_GUESSES,
    )


@app.post("/guess")
def guess(body: GuessRequest, today: Today) -> GuessResponse:
    day = body.date or today
    if day > today:
        raise HTTPException(status_code=400, detail="Puzzle not available yet")
    if not is_valid(body.guess):
        raise HTTPException(status_code=400, detail="Not in word list")

    answer = answer_for(day)
    states = score(body.guess, answer)
    solved = body.guess == answer
    return GuessResponse(
        guess=body.guess,
        letters=[LetterResult(letter=l, state=s) for l, s in zip(body.guess, states)],
        solved=solved,
        # The client tracks attempts, so the answer is revealed once it reports its final guess.
        answer=answer if solved or body.attempt == MAX_GUESSES else None,
    )
