# Bean & Brew — cafe website (testing1: the clean project)

A small Flask website: home, menu with filters, about, a validated contact form, a JSON API (`/api/menu`) and a
`/health` endpoint.

This repository is deliberately **clean**: pinned and current dependencies, no secrets in the code, a non-root
Docker image with the installers removed, `.env` git-ignored. SecurePipe should score it **ALLOW 0/100** and deploy it.

## Run locally

```
pip install -r requirements.txt
python app.py            # http://localhost:8000
python -m unittest discover -s tests
```

## Run in Docker

```
docker build -t bean-brew .
docker run --rm -p 8000:8000 bean-brew
```
