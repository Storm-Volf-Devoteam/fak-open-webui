# FAK Open WebUI — Ændringsoversigt

Alle ændringer lavet til Open WebUI for Forsvarsakademiets on-premise deployment.
Baseret på Open WebUI commit `02dc3e689` (main branch).

**Licensnote:** Open WebUI-branding (navn, logo, visuelle identifikatorer) er IKKE ændret — dette kræver enterprise-licens jf. licensens punkt 4.

---

## Kodeændringer

### 1. Dansk som default sprog
**Fil:** `src/lib/i18n/index.ts`
- Ændret fallback locale fra `['en-US']` til `['da-DK']`

### 2. Login-side disclaimer
**Fil:** `src/routes/auth/+page.svelte`
- Tilføjet tekst under login: "Kun til autoriseret personel. Al aktivitet logges."

### 3. FAK-farvetema (custom CSS)
**Fil:** `static/static/custom.css`
- FAK-farveprofil med navy-toner i dark mode (OKLCH farverum)
- Guld-accent på scrollbars
- CSS-variabler: `--fak-navy`, `--fak-gold` osv.

### 3. Fjernede eksterne community-links og -funktioner

| Fil | Hvad blev fjernet |
|-----|-------------------|
| `src/lib/components/chat/Settings/About.svelte` | Discord, Twitter, GitHub badges |
| `src/lib/components/layout/Sidebar/UserMenu.svelte` | "Documentation" og "Releases" links |
| `src/routes/(app)/+layout.svelte` | UpdateInfoToast og SyncStatsModal |
| `src/routes/+layout.svelte` | Changelog-modal |
| `src/lib/components/chat/ShareChatModal.svelte` | "Share to Open WebUI Community" knap + shareChat() funktion |
| `src/lib/components/chat/Messages/RateComment.svelte` | "Leave a public review" sektion |
| `src/lib/components/workspace/Models.svelte` | Community-sektion + shareModelHandler |
| `src/lib/components/workspace/Prompts.svelte` | Community-sektion + shareHandler |
| `src/lib/components/workspace/Tools.svelte` | Community-sektion + shareHandler |

### 5. Fjernede visse input-menu funktioner
**Fil:** `src/lib/components/chat/MessageInput/InputMenu.svelte`
- Fjernet Capture (kamera/screenshot) knap
- Fjernet Attach Webpage knap og modal
- Fjernet Attach Notes knap og tab view
- **Beholdt:** Google Drive og OneDrive integrationer (restored)

### 6. Fjernede Read Aloud (TTS) fra chat
**Fil:** `src/lib/components/chat/Messages/ResponseMessage.svelte`
- Fjernet Read Aloud-knap og speak/stopAudio-funktioner
- Fjernet Continue Response-knap
- Fjernet Info/token-usage knap (prompt_tokens, total_tokens visning)

### 7. Fjernede sidebar-navigation
**Fil:** `src/lib/components/layout/Sidebar.svelte`
- Fjernet Notes fra sidebar og pinned items
- Fjernet Calendar fra sidebar
- Fjernet Automations fra sidebar
- Fjernet Playground fra sidebar
- Kun Workspace forbliver som sidebar-menu-item

### 8. Fjernede Notes, Calendar, Automations og Playground fra brugermenu
**Fil:** `src/lib/components/layout/Sidebar/UserMenu.svelte`
- Fjernet Notes-link og pin-mulighed
- Fjernet Calendar-link og pin-mulighed
- Fjernet Automations-link og pin-mulighed
- Fjernet Playground-link og pin-mulighed
- Ændret DEFAULT_PINNED_ITEMS til kun `['workspace']`

### 9. FAK-logo som default profilbillede
**Fil:** `static/static/fak-logo.png` (ny fil)
- FAK våbenskjold (ugle med krone, "Sapientia et Providentia") tilføjet som fallback profilbillede

**Ændrede filer (favicon.png → fak-logo.png som profil-fallback):**
| Fil | Ændring |
|-----|---------|
| `src/lib/components/chat/Messages/ProfileImage.svelte` | Default model-profilbillede |
| `src/lib/components/chat/Messages/UserMessage.svelte` | Bruger-avatar fallback |
| `src/lib/components/workspace/Models/ModelEditor.svelte` | Model editor default + reset |
| `src/lib/components/admin/Settings/Evaluations/ArenaModelModal.svelte` | Arena model default |
| `src/lib/components/chat/Placeholder.svelte` | Model-billede on:error |
| `src/lib/components/chat/ChatPlaceholder.svelte` | Model-billede on:error |
| `src/lib/components/chat/MessageInput/Commands/Models.svelte` | Model-liste on:error |
| `src/lib/components/chat/ModelSelector/ModelItem.svelte` | Model-vælger on:error |
| `src/lib/components/layout/Sidebar/PinnedModelItem.svelte` | Pinned model on:error |
| `src/lib/components/workspace/Models.svelte` | Model-liste on:error |
| `src/lib/components/admin/Settings/Models.svelte` | Admin model-liste on:error |
| `src/lib/components/admin/Evaluations/Leaderboard.svelte` | Leaderboard on:error |
| `src/lib/components/admin/Analytics/ModelUsage.svelte` | Analytics on:error |
| `src/lib/components/admin/Analytics/Dashboard.svelte` | Dashboard on:error |
| `src/lib/components/admin/Users/UserList.svelte` | Brugerliste on:error |
| `src/lib/components/channel/Messages/Message.svelte` | Kanal-beskeder on:error |
| `src/lib/components/channel/MessageInput/MentionList.svelte` | Mention-liste on:error |
| `src/lib/components/chat/Messages/Citations.svelte` | Kilde-billede on:error |
| `backend/open_webui/routers/models.py` | Backend model-profilbillede redirect |

**NB:** App-logoet i sidebar-headeren (`Sidebar.svelte`) og notifikationer forbliver som `favicon.png` — dette er Open WebUI branding (licensbeskyttet).

### 10. Fjernede brugerstatus fra brugermenu
**Fil:** `src/lib/components/layout/Sidebar/UserMenu.svelte`
- Fjernet "Aktiv"/"Fraværende" status-indikator
- Fjernet "Opdater din status" knap og emoji-status visning
- Fjernet UserStatusModal trigger (modal-komponent stadig tilgængelig hvis behov)

### 11. Fjernede "Foreslået" prompt-forslag under chat-input
**Filer:**
- `src/lib/components/chat/Placeholder.svelte` — Fjernet `<Suggestions>` komponent fra velkomstsiden
- `src/lib/components/chat/ChatPlaceholder.svelte` — Fjernet `<Suggestions>` komponent fra model-placeholder

### 12. Fjernede FAK-logo fra login-siden
**Fil:** `src/routes/auth/+page.svelte`
- Fjernet FAK-logo (`fak-logo.png`) fra login-siden for at undgå visuel overskyggelse af Open WebUI-branding (licensens §4 "obscuring"-klausul)
- Login-disclaimer ("Kun til autoriseret personel. Al aktivitet logges.") er bevaret

### 13. Dansk titelgenerering uden emojis
**Fil:** `backend/open_webui/config.py`
- Ændret `DEFAULT_TITLE_GENERATION_PROMPT_TEMPLATE` til dansk
- Fjernet emoji-instruktioner fra titel-prompten
- Titler genereres nu på dansk uden emojis
- **NB:** Database-værdien kan overskrive kode-default — opdatér evt. via Docker exec

### 14. Forbedrede danske oversættelser
**Fil:** `src/lib/i18n/locales/da-DK/translation.json`

| Nøgle | Før | Efter |
|-------|-----|-------|
| `How can I help you today?` | "Hvordan kan jeg hjælpe dig i dag med FAK?" | "Hvordan kan jeg hjælpe dig i dag?" |
| `Reference Chats` | "Reference chats" | "Tidligere chats" |
| `Image` | "Billede" | "Billedgenerering" |
| `Regenerate` | "Regenerer" | "Prøv igen" |
| `Clone` | "Klon" | "Kopier" |
| `Clone Chat` | "Klon chat" | "Kopier chat" |
| `Clone of {{TITLE}}` | "Klon af {{TITLE}}" | "Kopi af {{TITLE}}" |
| `Attach Files` | "" (tom) | "Vedhæft filer" |
| `Was this response helpful?` | (ny) | "Var dette svar nyttigt?" |

### 15. Simplificeret feedback-modal
**Fil:** `src/lib/components/chat/Messages/RateComment.svelte`
- Fjernet karaktergivning (1-10 skala)
- Fjernet tags-input
- Beholdt: reason-valg og kommentar-felt

### 16. Banner vises under aktiv chat
**Fil:** `src/lib/components/chat/Navbar.svelte`
- Fjernet `!$chatId` betingelse, så advarselsbannerere også vises under aktiv chat

### 17. Feedback-opfordring ved svar
**Fil:** `src/lib/components/chat/Messages/ResponseMessage.svelte`
- Tilføjet "Var dette svar nyttigt?" tekst ved thumbs up/down-knapper på sidste besked

### 18. Fjernet FAK-logo fra chat-fallback
**Filer:** Alle filer der brugte `fak-logo.png` som fallback er ændret tilbage til `favicon.png`
- FAK ønskede logoet fjernet helt fra chat — Open WebUI's favicon bruges nu som default

### 19. Permanent advarselsbanner (ingen dismiss-knap)
**Filer:**
- `src/lib/components/common/Banner.svelte` — Fjernet dismiss-knap (×)
- `src/lib/components/chat/Navbar.svelte` — Fjernet dismiss-filtrering, banner vises altid

### 20. Omdøbning af UI-termer (dansk + engelsk)
**Filer:**
- `src/lib/i18n/locales/da-DK/translation.json`
- `src/lib/i18n/locales/en-US/translation.json`

| Original term | Dansk | Engelsk |
|---|---|---|
| Workspace | Opsætnings panel | Setup Panel |
| Folder/Folders | Projekt/Projekter | Project/Projects |

Workspace-sektionen (Opsætningspanelet) bruger "Agenter" for sine tilpassede modeller, mens Admin-indstillinger bruger "Modeller" for de rå provider-modeller. Ændret via separate i18n-nøgler:
- Workspace-komponenter bruger nye nøgler: `Agents`, `New Agent`, `Search Agents`
- Admin Settings-komponenter bruger standard `Models`-nøgler

### 21. Bruger-profilbilleder låst til FAK-logo
**Ændrede filer:**
| Fil | Ændring |
|-----|---------|
| `src/lib/components/layout/Sidebar.svelte` | Sidebar avatar (collapsed + expanded) |
| `src/lib/components/chat/Navbar.svelte` | Top-right avatar |
| `src/lib/components/channel/Navbar.svelte` | Kanal-navbar avatar |
| `src/lib/components/layout/Sidebar/UserMenu.svelte` | Dropdown-menu avatar |
| `src/routes/+layout.svelte` | Browser-notification ikon |
| `src/lib/components/chat/Settings/Account.svelte` | Profilbillede-redigering deaktiveret |

- Alle bruger-profilbilleder viser nu altid `fak-logo.png`
- Brugere kan ikke længere ændre deres profilbillede i indstillinger
- Påvirker IKKE model-billeder, app-logo eller andre brugeres avatarer i kanaler/admin

### 22. Kanaler genaktiveret
**Fil:** `backend/open_webui/config.py`
- Ændret `ENABLE_CHANNELS` default fra `'False'` til `'True'`

### 23. Model-konfiguration via seed-script
**Fil:** `scripts/fak-seed.py`
- Omdøber 3 Mistral-modeller: mistral-small→Hurtig, mistral-medium→Balanceret, mistral-large→Kompleks
- Disabler alle øvrige provider-modeller (henter listen fra Mistral API)
- Idempotent med `--force` flag

---

## Docker deployment-konfiguration

### Dockerfile-ændringer
**Fil:** `Dockerfile`
- Fjernet `--platform=$BUILDPLATFORM` fra `FROM node:22-alpine3.20 AS build`
- Tilføjet `ENV NODE_OPTIONS="--max-old-space-size=4096"` før `RUN npm run build`
- Tilføjet `COPY ./scripts/fak-seed.py /app/scripts/fak-seed.py`

### Environment variables (docker-compose.yaml)

Alle FAK-indstillinger sættes automatisk via env vars ved første opstart (tom database):

| Indstilling | Env var | Værdi |
|---|---|---|
| Signup | `ENABLE_SIGNUP` | `false` |
| Community sharing | `ENABLE_COMMUNITY_SHARING` | `false` |
| Default locale | `DEFAULT_LOCALE` | `da-DK` |
| Kanaler | `ENABLE_CHANNELS` | `true` |
| Web search | `ENABLE_WEB_SEARCH` | `true` |
| Søgemaskine | `WEB_SEARCH_ENGINE` | `ddgs` |
| Bypass embedding | `BYPASS_WEB_SEARCH_EMBEDDING_AND_RETRIEVAL` | `true` |
| Banner | `WEBUI_BANNERS` | JSON med FAK sikkerhedsbesked |
| System prompt + temperatur | `DEFAULT_MODEL_PARAMS` | Dansk FAK-prompt, temp 0.4 |
| LLM-forbindelse | `OPENAI_API_BASE_URLS` | `https://api.mistral.ai/v1` |
| LLM API-nøgle | `OPENAI_API_KEYS` | Fra `.env` (MISTRAL_API_KEY) |
| Billedgenerering | `ENABLE_IMAGE_GENERATION` | `true` |
| Billed-engine | `IMAGE_GENERATION_ENGINE` | `openai` |
| Billed-API URL | `IMAGES_OPENAI_API_BASE_URL` | `http://host.docker.internal:5100/v1` |
| Billed-API-nøgle | `IMAGES_OPENAI_API_KEY` | Fra `.env` (FLUX_API_KEY) |

**NB:** API-nøgler lever i `.env` (gitignored) og refereres via `${VAR}` i docker-compose.yaml.

---

## Langfuse-integration (forberedt, ikke implementeret)

Kræver kun Docker environment variables — ingen kodeændringer:
```bash
-e ENABLE_OTEL=true
-e ENABLE_OTEL_TRACES=true
-e ENABLE_OTEL_METRICS=true
-e OTEL_EXPORTER_OTLP_ENDPOINT=https://<LANGFUSE_HOST>/api/public/otel
-e OTEL_OTLP_SPAN_EXPORTER=http
-e OTEL_BASIC_AUTH_USERNAME=<LANGFUSE_PUBLIC_KEY>
-e OTEL_BASIC_AUTH_PASSWORD=<LANGFUSE_SECRET_KEY>
-e OTEL_SERVICE_NAME=fak-open-webui
```

---

## Billedgenerering (FLUX.2 adapter)

**Mappe:** `flux-adapter/`

Midlertidig OpenAI → FLUX.2 adapter-proxy så Open WebUI kan bruge DataCrunch/Verda FLUX.2 [klein] til billedgenerering. Erstattes af LiteLLM-proxy i produktion.

**Opstart:**
```bash
cd flux-adapter
pip install -r requirements.txt
uvicorn app:app --port 5100
```

**Open WebUI konfiguration (Admin → Settings → Images):**
| Indstilling | Værdi |
|---|---|
| Enable Image Generation | On |
| Image Generation Engine | Default (OpenAI) |
| API Base URL | `http://localhost:5100/v1` |
| API Key | DataCrunch/Verda API-nøgle |

---

## Deployment-instruktioner for teamet

1. Klon repo og opret `.env` med API-nøgler (se `.env.example`)
2. `docker compose up -d --build`
3. Opret admin-bruger via `http://localhost:3000`
4. `docker exec open-webui python3 /app/scripts/fak-seed.py`

Se `SETUP.md` for detaljeret guide.

## Verifikation
- `npm run build` kompilerer fejlfrit
- Login-side viser dansk disclaimer
- Forsiden viser FAK-undertekst, ingen "Foreslået"-sektion
- Ingen eksterne links eller community-funktioner synlige
- Sidebar viser kun Workspace (ingen Notes, Calendar, Automations, Playground)
- Brugermenu viser kun Indstillinger, Admin, Arkiverede chats, Workspace, Log ud
- Chat: ingen Read Aloud, Continue Response, Capture, Attach Webpage knapper
- Web search virker via DDGS (DuckDuckGo) — kilder vises i chat
- Chat-titler genereres på dansk uden emojis
- Kun 3 agenter synlige: Hurtig, Balanceret, Kompleks (rå modeller skjult)
- Advarselsbanner permanent synligt (ingen dismiss-knap)
- Kanaler tilgængelige i sidebar
- Rating/feedback, kode-fortolker, RAG, mapper fungerer stadig
