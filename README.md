# MindGames

Collection of custom word, trivia, and other puzzle games. Showcase of CI/CD principles.

## Layout

```
frontend/              Vue 3 + Vite site shell
  src/games/index.js   game registry (drives routes and the home page)
  src/games/<id>/      each game's Vue UI; talks to its backend only via api.js
games/<id>/            each game's backend: standalone service with its own Dockerfile, tests, and CI
proxy/nginx.conf       production routing: /api/<id>/* -> <id> service
docker-compose.yml     runs everything behind nginx on http://localhost:8080
```

Each game backend serves its routes at `/`. The proxy (`vite.config.js` in dev, `proxy/nginx.conf` in prod)
maps `/api/<id>/*` to the right service and strips the prefix.

## Running

```sh
# dev: one terminal per game backend, plus the frontend
cd games/wordle && pip install -r requirements-dev.txt && uvicorn wordle.api:app --reload --port 8001
cd frontend && npm install && npm run dev

# everything in containers
docker compose up --build
```

## Adding a game

1. `games/<id>/`: backend service (copy `games/wordle` as a template) with a Dockerfile listening on port 8000.
2. `frontend/src/games/<id>/`: entry component plus `api.js` calling `/api/<id>/...`.
3. Register it in `frontend/src/games/index.js`.
4. Add a route to `frontend/vite.config.js` (`gameServices`, unique local port) and a `location` block to `proxy/nginx.conf`.
5. Add the service to `docker-compose.yml` and a `.github/workflows/game-<id>.yml` (copy the wordle one).
