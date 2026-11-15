# Network Routes API

A small Django REST API for a network of nodes connected by directed edges, each with a latency. Give it two nodes and it finds the lowest-latency route between them, and remembers every lookup.

Built with Python 3.12, Django 5.2, DRF, networkx and PostgreSQL 17.

## Running it

Copy the env file first:

    cp .env.example .env

To develop locally, keep Postgres in Docker and run Django on your machine:

    python3.12 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    docker compose up -d --wait db
    python manage.py migrate
    python manage.py runserver

Or run everything in Docker (it migrates on start):

    docker compose up --build

The API lives at http://localhost:8000/api/, and `/api/health_check/` tells you if it's up.

## Endpoints

| Method | Path | What it does |
|---|---|---|
| POST | /api/nodes | Create a node |
| GET | /api/nodes | List nodes |
| DELETE | /api/nodes/{id} | Delete a node (not while it has edges) |
| POST | /api/edges | Create an edge |
| GET | /api/edges | List edges |
| DELETE | /api/edges/{id} | Delete an edge |
| POST | /api/routes/shortest | Find the shortest route |
| GET | /api/routes/history | Past lookups, newest first |

A few things worth knowing:

- Edges are directed, and refer to nodes by name.
- Lists are paginated with `page` and `page_size` (max 100).
- History can be filtered by `source`, `destination`, `date_from` and `date_to`. Dates can be a plain date or a full datetime, and a plain `date_to` includes that whole day.
- Each successful lookup is saved, repeats included. If there's no route, you get a 404 and nothing is saved.

For example:

    curl -X POST http://localhost:8000/api/routes/shortest \
      -H 'Content-Type: application/json' \
      -d '{"source": "ServerA", "destination": "ServerD"}'

    {"total_latency": 23.4, "path": ["ServerA", "ServerB", "ServerD"]}

## Tests

With the database running (`docker compose up -d --wait db`):

    python manage.py test

CI runs the same thing on every push to `main`.

## Postman

`postman/network-routes.postman_collection.json` documents every request, each with a saved success or failure example.
