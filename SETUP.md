# FAK Open WebUI — Hurtig opsætning

## Forudsætninger

- [Docker](https://docs.docker.com/get-docker/) installeret
- Adgang til dette repo (SSH-nøgle konfigureret på GitHub)
- API-nøgle til LLM-provider (f.eks. OpenAI, Azure, eller lokal Ollama)

## 1. Klon repo'et

```bash
git clone git@github.com:Storm-Volf-Devoteam/fak-open-webui.git
cd fak-open-webui
```

## 2. Byg Docker image

```bash
docker build -t fak-open-webui .
```

Bemærk: Første build tager 5-10 minutter.

## 3. Start containeren

```bash
docker run -d \
  --name fak-open-webui \
  -p 8080:8080 \
  -v open-webui-data:/app/backend/data \
  -e OPENAI_API_KEY=din-api-nøgle \
  fak-open-webui
```

## 4. Åbn i browser

```
http://localhost:8080
```

Opret en admin-bruger ved første login. Sprog er sat til dansk som default.

## Dokumentation

- `CHANGES.md` — komplet oversigt over alle FAK-tilpasninger
- `LICENSE` — Open WebUI-licens (branding må ikke ændres uden enterprise-licens)
