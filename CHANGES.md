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

### 4. Danske prompt-forslag
**Fil:** `backend/open_webui/config.py`
- Erstattet engelske standard-forslag med 6 danske FAK-relevante forslag
- **NB:** Database-værdien skal også opdateres (se "Database-ændringer" nedenfor)

### 5. FAK undertekst på forsiden
**Fil:** `src/lib/components/chat/Placeholder.svelte`
- Tilføjet "Forsvarsakademiets AI-assistent — stil et spørgsmål eller vælg et forslag herunder." under velkomsttitlen

### 6. Fjernede eksterne community-links og -funktioner

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

### 7. Fjernede visse input-menu funktioner
**Fil:** `src/lib/components/chat/MessageInput/InputMenu.svelte`
- Fjernet Capture (kamera/screenshot) knap
- Fjernet Attach Webpage knap og modal
- Fjernet Attach Notes knap og tab view
- **Beholdt:** Google Drive og OneDrive integrationer (restored)

### 8. Fjernede Read Aloud (TTS) fra chat
**Fil:** `src/lib/components/chat/Messages/ResponseMessage.svelte`
- Fjernet Read Aloud-knap og speak/stopAudio-funktioner
- Fjernet Continue Response-knap
- Fjernet Info/token-usage knap (prompt_tokens, total_tokens visning)

### 9. Fjernede sidebar-navigation
**Fil:** `src/lib/components/layout/Sidebar.svelte`
- Fjernet Notes fra sidebar og pinned items
- Fjernet Calendar fra sidebar
- Fjernet Automations fra sidebar
- Fjernet Playground fra sidebar
- Kun Workspace forbliver som sidebar-menu-item

### 10. Fjernede Notes, Calendar, Automations og Playground fra brugermenu
**Fil:** `src/lib/components/layout/Sidebar/UserMenu.svelte`
- Fjernet Notes-link og pin-mulighed
- Fjernet Calendar-link og pin-mulighed
- Fjernet Automations-link og pin-mulighed
- Fjernet Playground-link og pin-mulighed
- Ændret DEFAULT_PINNED_ITEMS til kun `['workspace']`

### 11. FAK-logo som default profilbillede
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

### 12. Fjernede brugerstatus fra brugermenu
**Fil:** `src/lib/components/layout/Sidebar/UserMenu.svelte`
- Fjernet "Aktiv"/"Fraværende" status-indikator
- Fjernet "Opdater din status" knap og emoji-status visning
- Fjernet UserStatusModal trigger (modal-komponent stadig tilgængelig hvis behov)

### 13. Fjernede "Foreslået" prompt-forslag under chat-input
**Filer:**
- `src/lib/components/chat/Placeholder.svelte` — Fjernet `<Suggestions>` komponent fra velkomstsiden
- `src/lib/components/chat/ChatPlaceholder.svelte` — Fjernet `<Suggestions>` komponent fra model-placeholder

---

## Database-ændringer (via Docker exec)

Danske prompt-forslag blev skrevet direkte til SQLite-databasen i containeren:
```bash
docker exec open-webui-backend python3 -c "
import sqlite3, json
db = sqlite3.connect('/app/backend/data/webui.db')
row = db.execute(\"SELECT data FROM config WHERE id=1\").fetchone()
config = json.loads(row[0])
config['ui']['prompt_suggestions'] = [
    {'title': ['Opsummer', 'et dokument eller en rapport'], 'content': '...'},
    {'title': ['Forklar', 'et fagligt koncept i simple termer'], 'content': '...'},
    {'title': ['Skriv udkast', 'til en mail eller et notat'], 'content': '...'},
    {'title': ['Analysér', 'fordele og ulemper ved en beslutning'], 'content': '...'},
    {'title': ['Gennemgå', 'og forbedre en tekst'], 'content': '...'},
    {'title': ['Giv overblik', 'over et emne'], 'content': '...'}
]
db.execute(\"UPDATE config SET data=? WHERE id=1\", [json.dumps(config, ensure_ascii=False)])
db.commit()
db.close()
"
```

---

## Admin-konfiguration (via admin-panelet)

Disse ændringer blev lavet via `http://localhost:8080` admin UI og gemmes i databasen:

| Indstilling | Placering | Værdi |
|---|---|---|
| Info-banner | Indstillinger → Generelt → Bannere | FAK intern platform-besked |
| Response watermark | Indstillinger → Generelt → Vandmærke | Institutionel attribution |
| System prompt | Indstillinger → Generelt → Systemprompt | Dansk FAK-prompt med `{{USER_NAME}}`, `{{CURRENT_DATE}}` |
| Titel-generation prompt | Indstillinger → Grænseflade | Dansk prompt |
| Tag-generation prompt | Indstillinger → Grænseflade | Dansk prompt |
| Opfølgnings-generation prompt | Indstillinger → Grænseflade | Dansk prompt |
| Temperatur | Indstillinger → Generelt → Avanceret | 0.4 |
| Community sharing | Indstillinger → Generelt | Slået fra |
| Signup | Indstillinger → Generelt | Slået fra |
| Default locale | Indstillinger → Generelt | da-DK |

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

1. **Kodeændringer:** Checkout denne branch og byg frontend med `npm run build`
2. **Database:** Kør prompt-suggestions scriptet ovenfor mod den nye container
3. **Admin-konfiguration:** Gentag admin-indstillingerne fra tabellen ovenfor
4. **Langfuse:** Tilføj OTEL env vars til Docker container når Langfuse-adgang er klar

## Verifikation
- `npm run build` kompilerer fejlfrit
- Login-side viser dansk disclaimer
- Forsiden viser FAK-undertekst, ingen "Foreslået"-sektion
- Ingen eksterne links eller community-funktioner synlige
- Sidebar viser kun Workspace (ingen Notes, Calendar, Automations, Playground)
- Brugermenu viser kun Indstillinger, Admin, Arkiverede chats, Workspace, Log ud
- Chat: ingen Read Aloud, Continue Response, Capture, Attach Webpage knapper
- Profilbilleder viser FAK-logo som default (ugle-våbenskjold)
- Rating/feedback, kode-fortolker, RAG, mapper fungerer stadig
