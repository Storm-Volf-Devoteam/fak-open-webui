# FAK Open WebUI — Opsætningsguide

## Forudsætninger

- [Docker](https://docs.docker.com/get-docker/) installeret
- Adgang til dette repo (SSH-nøgle konfigureret på GitHub)
- API-nøgle til LLM-provider (f.eks. OpenAI, Azure, eller lokal Ollama)

## 1. Klon repo'et

```bash
git clone git@github.com:Storm-Volf-Devoteam/fak-open-webui.git
cd fak-open-webui
```

## 2. Opret .env med API-nøgler

```bash
cp .env.example .env
```

Åbn `.env` og indsæt din Mistral API-nøgle:

```
MISTRAL_API_KEY=din-rigtige-nøgle-her
```

## 3. Byg og start med Docker Compose

```bash
docker compose up -d --build
```

`--build` er vigtigt — det sikrer at image'et bygges fra den lokale kode med alle FAK-ændringer. Første build tager 5-10 minutter.

## 4. Åbn i browser og opret admin

```
http://localhost:3000
```

Opret en admin-bruger ved første login. Sprog er sat til dansk som default.

## 5. Kør seed-script

Seed-scriptet omdøber de 3 Mistral-modeller (Hurtig, Balanceret, Kompleks) og disabler alle øvrige modeller. Det kræver at admin-brugeren er oprettet først.

```bash
docker exec open-webui python3 /app/scripts/fak-seed.py
```

Scriptet er idempotent — safe at køre flere gange. Brug `--force` for at overskrive eksisterende ændringer.

## Hvad er automatisk konfigureret?

Følgende indstillinger sættes automatisk via environment variables i `docker-compose.yaml` (ved første opstart):

| Indstilling | Værdi |
|---|---|
| Sprog | Dansk (da-DK) |
| Signup | Slået fra |
| Community sharing | Slået fra |
| Web search | Aktiveret (DuckDuckGo) |
| Bypass embedding for web search | Til |
| Advarselsbanner | FAK sikkerhedsbesked (permanent, kan ikke fjernes) |
| System prompt | Dansk FAK-prompt med `{{USER_NAME}}` og `{{CURRENT_DATE}}` |
| Temperatur | 0.4 |
| Titel-generering | Dansk, uden emojis (code default) |
| Mistral LLM-forbindelse | Automatisk via env var (API-nøgle fra `.env`) |
| Billedgenerering | FLUX.2 adapter (valgfrit, kræver separat service) |

### Modeller (via seed-script)

Seed-scriptet omdøber 3 Mistral-modeller og disabler alle øvrige:

| Vist navn | Mistral model-ID | Beskrivelse |
|---|---|---|
| Hurtig | mistral-small-latest | Til simple opgaver |
| Balanceret | mistral-medium-latest | Anbefalet til de fleste opgaver |
| Kompleks | mistral-large-latest | Grundigt svar, tager længere tid |

## Billedgenerering med FLUX.2 (valgfrit)

Kræver en separat terminal og en API-nøgle til DataCrunch/Verda.

**Start FLUX.2-adapteren:**
```bash
cd flux-adapter
pip install -r requirements.txt
uvicorn app:app --port 5100
```

**Konfigurér i admin-panelet** (Admin → Indstillinger → Billeder):

| Indstilling | Værdi |
|---|---|
| Enable Image Generation | Til |
| Image Generation Engine | Default (OpenAI) |
| API Base URL | `http://localhost:5100/v1` |
| API Key | DataCrunch/Verda API-nøgle |

## Dokumentation

- `CHANGES.md` — komplet oversigt over alle FAK-tilpasninger
- `LICENSE` — Open WebUI-licens (branding må ikke ændres uden enterprise-licens)
