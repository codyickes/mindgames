from datetime import date

import pytest
from fastapi.testclient import TestClient

from wordle.api import app, get_today
from wordle.words import WORDS, answer_for

TODAY = date(2026, 10, 27)
ANSWER = answer_for(TODAY)
WRONG = next(w for w in WORDS if w != ANSWER)


@pytest.fixture
def client():
    app.dependency_overrides[get_today] = lambda: TODAY
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_daily(client):
    assert client.get("/daily").json() == {
        "date": "2026-10-27",
        "puzzle_number": 300,
        "word_length": 5,
        "max_guesses": 6,
    }


def test_correct_guess_solves_and_reveals(client):
    body = client.post("/guess", json={"guess": ANSWER.upper(), "attempt": 1}).json()
    assert body["solved"] is True
    assert body["answer"] == ANSWER
    assert [l["state"] for l in body["letters"]] == ["correct"] * 5
    assert "".join(l["letter"] for l in body["letters"]) == ANSWER


def test_wrong_guess_hides_answer_until_last_attempt(client):
    body = client.post("/guess", json={"guess": WRONG, "attempt": 5}).json()
    assert body["solved"] is False
    assert body["answer"] is None

    body = client.post("/guess", json={"guess": WRONG, "attempt": 6}).json()
    assert body["answer"] == ANSWER


def test_past_date_uses_that_days_answer(client):
    past = date(2026, 10, 1)
    body = client.post(
        "/guess", json={"guess": answer_for(past), "attempt": 1, "date": past.isoformat()}
    ).json()
    assert body["solved"] is True


def test_future_date_rejected(client):
    resp = client.post("/guess", json={"guess": WRONG, "attempt": 1, "date": "2026-10-28"})
    assert resp.status_code == 400


def test_unknown_word_rejected(client):
    resp = client.post("/guess", json={"guess": "zzzzz", "attempt": 1})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Not in word list"


@pytest.mark.parametrize(
    "payload",
    [
        {"guess": "four", "attempt": 1},
        {"guess": "sixsix", "attempt": 1},
        {"guess": "cr4ne", "attempt": 1},
        {"guess": "crane", "attempt": 0},
        {"guess": "crane", "attempt": 7},
    ],
)
def test_invalid_payload(client, payload):
    assert client.post("/guess", json=payload).status_code == 422
