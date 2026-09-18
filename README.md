# Assistente Virtuale per Viaggi - Architettura di Sistema

Applicazione full-stack per la pianificazione e prenotazione di viaggi personalizzati tramite Intelligenza Artificiale conversazionale.

## Flusso e Componenti

Il sistema si basa su un'architettura disaccoppiata (Client-Server) ed è composto dai seguenti moduli principali:

### 1. Client (Frontend)
* **Tecnologia:** React
* **Ruolo:** Gestisce l'Interfaccia Utente (UI) e l'interazione diretta con l'utente finale. Si occupa di inviare le richieste API al backend e di avviare il flusso di autenticazione. Implementa route guards per proteggere le rotte sensibili (es. prenotazioni) e formatta dinamicamente le risposte testuali e le tabelle tramite `react-markdown`.

### 2. Server (Backend)
* **Tecnologia:** Python 3 (FastAPI)
* **Ruolo:** Riceve le chiamate REST dal frontend, gestisce la logica di business e fa da ponte per i dati. Ospita l'Agente AI basato su LangChain e Groq (Llama 3.3 70B), orchestrando il Tool Calling (ricerca e prenotazione) con rigorosi controlli sui vincoli dell'utente (budget, date, nazione).

### 3. Database (Ibrido)
L'applicazione sfrutta due tecnologie distinte per garantire l'integrità strutturale e flessibilità semantica:
* **Database Relazionale (SQLite):** Memorizza le entità strutturate come Utenti, Voli, Alberghi e logica delle Prenotazioni tramite SQLAlchemy.
* **Database Vettoriale (ChromaDB):** Utilizzato per supportare un approccio RAG (Retrieval-Augmented Generation). Permette di recuperare le attività turistiche interrogando le descrizioni testuali e i target di riferimento tramite ricerca semantica.