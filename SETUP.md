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

## 5. Admin-konfiguration

Efter første login skal følgende konfigureres via admin-panelet (`http://localhost:8080` → Admin → Indstillinger):

### Generelt

**System prompt** (Indstillinger → Generelt):
```
Du er en AI-assistent for Forsvarsakademiet (FAK). Du hjælper medarbejdere og studerende med faglige opgaver i en intern, sikker kontekst.

Dato: {{CURRENT_DATE}} ({{CURRENT_WEEKDAY}})
Bruger: {{USER_NAME}}

## Svarkvalitet
- Svar kort og præcist. Tilpas længden til spørgsmålet — et simpelt spørgsmål får et kort svar.
- Brug aldrig emojis medmindre brugeren beder om det.
- Undgå at gentage spørgsmålet eller opsummere hvad du er ved at gøre. Gå direkte til svaret.
- Brug kun overskrifter og punktlister når det genuint forbedrer læsbarheden. Korte svar behøver ingen formatering.
- Lav aldrig afsluttende opsummeringer der gentager det du allerede har sagt.
- Når du bruger kilder fra websøgning: fremhæv de 3-5 vigtigste pointer, ikke alt indhold fra alle kilder.

## Sprog og tone
- Svar altid på dansk, medmindre brugeren eksplicit beder om et andet sprog.
- Hold en professionel og præcis tone. Undgå uformel jargon.
- Skriv i aktiv form. Undgå fyldord og unødvendige indledninger som "Selvfølgelig!" eller "Godt spørgsmål!".

## Faglig integritet
- Angiv tydeligt når du er usikker eller ikke har tilstrækkelig viden. Gæt aldrig på faktuelle oplysninger.
- Du må ikke generere klassificeret eller følsomt indhold. Henvis til relevante fagpersoner ved sikkerhedsmæssige spørgsmål.

## Kerneopgaver
Hjælp gerne med: opsummering, analyse, tekstudkast, forklaring af koncepter, strukturering af argumenter og faglig sparring.
```

**Øvrige indstillinger:**

| Indstilling | Placering | Værdi |
|---|---|---|
| Bannere | Generelt → Bannere | "AI-genereret indhold kan være upræcist — verificér altid vigtige oplysninger. Al aktivitet logges i henhold til gældende sikkerhedsbestemmelser." |
| Temperatur | Generelt → Avanceret | 0.4 |
| Community sharing | Generelt | Slået fra |
| Signup | Generelt | Slået fra |
| Default locale | Generelt | da-DK |

### Grænseflade (Indstillinger → Grænseflade)

**Titel-generation prompt** — indsæt i feltet under "Automatisk titelgenerering":
```
### Task:
Generate a concise, 3-5 word title summarizing the chat history.
### Guidelines:
- The title should clearly represent the main theme or subject of the conversation.
- Do NOT use emojis. Do not use quotation marks or special formatting.
- Write the title in Danish; default to English if multilingual.
- Prioritize accuracy over excessive creativity; keep it clear and simple.
- Your entire response must consist solely of the JSON object, without any introductory or concluding text.
- The output must be a single, raw JSON object, without any markdown code fences or other encapsulating text.
- Ensure no conversational text, affirmations, or explanations precede or follow the raw JSON output, as this will cause direct parsing failure.
### Output:
JSON format: { "title": "your concise title here" }
### Examples:
- { "title": "Aktiemarkeds tendenser" },
- { "title": "Perfekt chokoladekage opskrift" },
- { "title": "Udvikling af musikstreaming" },
- { "title": "Produktivitetstips til fjernarbejde" },
- { "title": "AI i sundhedssektoren" }
### Chat History:
<chat_history>
{{MESSAGES:END:2}}
</chat_history>
```

### Web Search (Indstillinger → Web Search)

| Indstilling | Værdi |
|---|---|
| Enable Web Search | Til |
| Websøgemaskine | DDGS |
| Omgå Embedding og Retrieval | Til |

### Prompt-forslag (via terminal)

Kør dette for at sætte danske prompt-forslag på forsiden:

```bash
docker exec fak-open-webui python3 -c "
import sqlite3, json
db = sqlite3.connect('/app/backend/data/webui.db')
row = db.execute(\"SELECT data FROM config WHERE id=1\").fetchone()
config = json.loads(row[0])
config['ui']['prompt_suggestions'] = [
    {'title': ['Opsummer', 'et dokument eller en rapport'], 'content': 'Opsummer følgende dokument eller rapport. Fremhæv de vigtigste pointer, konklusioner og eventuelle anbefalinger.'},
    {'title': ['Forklar', 'et fagligt koncept i simple termer'], 'content': 'Forklar følgende koncept i klare, simple termer som en ikke-specialist kan forstå:'},
    {'title': ['Skriv udkast', 'til en mail eller et notat'], 'content': 'Skriv et professionelt udkast til en mail eller et notat om følgende emne:'},
    {'title': ['Analysér', 'fordele og ulemper ved en beslutning'], 'content': 'Analysér fordele og ulemper ved følgende beslutning eller forslag:'},
    {'title': ['Gennemgå', 'og forbedre en tekst'], 'content': 'Gennemgå følgende tekst og foreslå forbedringer til sprog, struktur og klarhed:'},
    {'title': ['Giv overblik', 'over et emne'], 'content': 'Giv et struktureret overblik over følgende emne:'}
]
db.execute(\"UPDATE config SET data=? WHERE id=1\", [json.dumps(config, ensure_ascii=False)])
db.commit()
db.close()
"
```

## Dokumentation

- `CHANGES.md` — komplet oversigt over alle FAK-tilpasninger
- `LICENSE` — Open WebUI-licens (branding må ikke ændres uden enterprise-licens)
