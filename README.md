# Feedback App

Small Flask app for collecting feedback submissions. Built for the DevOps assignment.

## What it does

- `/` - home page
- `/form` - submit feedback (name, email, message)
- `/submissions` - list of all submissions, latest first

Data is stored in a SQLite database (`data/feedback.db`).

## Tech used

- Python 3 + Flask
- SQLite
- Docker + docker-compose
- Gunicorn (as the WSGI server in container)

## Running locally (without docker)

```
python -m venv venv
source venv/bin/activate    # on windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:8000

## Running with docker

```
docker compose up -d --build
```

Then go to http://localhost:8000

To stop:
```
docker compose down
```

Data will be saved in `./data/feedback.db` and will persist between restarts because of the volume mount in docker-compose.

## Deployment

Deployed on AWS EC2 (Debian), behind nginx with HTTPS via Let's Encrypt.
The container is set to `restart: unless-stopped` so it comes back up after a reboot.
