# Backend — Assistente Virtuale per Viaggi

Questo repository contiene il codice sorgente del backend API per l'applicazione di pianificazione viaggi.
Il backend funge da intermediario tra il client frontend e il database, orchestrando le chiamate LLM per la generazione degli itinerari.

---

## Stack tecnologico

| Componente | Tecnologia |
|---|---|
| Linguaggio | Python 3 |
| Framework web | FastAPI |
| AI / LLM Orchestration | LangChain, Groq (Llama 3.3 70B) |
| Database Relazionale | SQLite (con SQLAlchemy) |
| Database Vettoriale | ChromaDB (RAG) |

---

## Struttura del progetto

```text
backend/
├── main.py                 # Entrypoint — istanza FastAPI e middleware
├── .env                     # Variabili d'ambiente locali (non versionato)
└── src/
    ├── model/               # Modelli dati SQLAlchemy
    ├── tools.py             # Strumenti eseguibili dall'Agente (Ricerca SQL, RAG, Prenotazione)
    ├── agent.py             # Configurazione LangChain, prompt e setup LLM
    └── seed.py              # Script di popolamento iniziale dei database
```

---

## Configurazione iniziale

### 1. Installazione delle dipendenze

```bash
pip install -r requirements.txt
```

### 2. Configurazione delle variabili d'ambiente

Creare un file `.env` nella directory principale del progetto e inserire le chiavi richieste seguendo il file `.env.example`


### 3. Popolamento del Database

Prima di avviare il server, inizializzare e popolare SQLite e ChromaDB con le destinazioni di default:

```bash
python seed.py
```

---

## Avvio del server

Per avviare il server in locale, eseguire:

```bash
uvicorn main:app --reload
```

Il middleware CORS è già configurato per accettare richieste dal client frontend.

La documentazione interattiva Swagger UI è disponibile su: [http://localhost:8000/docs](http://localhost:8000/docs)