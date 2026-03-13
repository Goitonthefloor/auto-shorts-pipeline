# Autonomous Shorts Pipeline (Docker, hosted AI, YouTube Upload)

Erstellt aus Eingaben wie `"4 shorts"` autonom:
1. Ideen + Hooks + Titel
2. Video-Rendering über gehostete KI (fal.ai)
3. Musik-Mix + Encoding lokal (FFmpeg, max. 12 Threads)
4. Upload + Beschriftung auf YouTube

## Hardware-Ziel
- CPU: Ryzen 7 5800X3D
- RAM: 32 GB
- GPU: RTX 4070 12 GB

> GPU wird für lokale Schritte nicht zwingend benötigt (KI-Render hosted), aber Container ist GPU-ready.

## Architektur
- FastAPI Service (`POST /run`)
- OpenAI für autonome Ideenentwicklung
- fal.ai für Bild/Video-Generation
- YouTube Data API für Upload
- FFmpeg für finalen Export + Musik

## 1) Setup
```bash
cp .env.example .env
mkdir -p data music secrets
```

`secrets/` benötigt:
- `client_secret.json` (Google OAuth Client für YouTube API)
- `token.json` (wird beim ersten OAuth-Run erzeugt)

## 2) Docker starten
```bash
docker compose up -d --build
```

## 3) Pipeline triggern
```bash
curl -X POST http://localhost:8099/run \
  -H 'Content-Type: application/json' \
  -d '{"instruction":"4 shorts"}'
```

## 4) Geschlossener Container-Hinweis
Empfohlen für produktiv:
- dedizierte Docker Network Policy
- nur Egress auf benötigte APIs erlauben:
  - api.openai.com
  - fal.ai
  - youtube.googleapis.com
  - oauth2.googleapis.com

## GitHub (neues Repo)
Da ich nicht direkt in dein GitHub-Konto pushen kann, lokal so veröffentlichen:
```bash
git init
git add .
git commit -m "Initial autonomous shorts pipeline"
git branch -M main
git remote add origin git@github.com:<DEIN_USER>/<DEIN_REPO>.git
git push -u origin main
```
