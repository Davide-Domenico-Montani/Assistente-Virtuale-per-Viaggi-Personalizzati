# Frontend — Assistente Virtuale per Viaggi

Questo repository contiene il codice sorgente del client frontend per l'interazione con l'Agente AI di viaggio. Offre un'interfaccia di chat reattiva e una dashboard per gestire le prenotazioni.

---

## Stack Tecnologico

| Componente | Tecnologia |
|---|---|
| Framework | React |
| Styling | CSS Modules / Custom CSS |
| Routing | React Router DOM |
| Formattazione Markdown | React-Markdown + Remark-GFM |

---

## Architettura — Pattern MVVM

Il progetto adotta il pattern **Model-View-ViewModel (MVVM)** per separare nettamente l'interfaccia grafica dalla logica di business e dai dati.

- **Model** (`src/model/`) — Contiene le funzioni che comunicano con il backend (chiamate `fetch` alle API REST) e con servizi esterni come Firebase Authentication. Non contiene alcuna logica di stato React.
- **ViewModel** (`src/viewModel/`) — Implementato tramite Custom Hooks React. Fanno da ponte tra Model e View: gestiscono lo stato locale, le chiamate asincrone e la gestione degli errori (es. `useChatViewModel`, `useLogoutViewModel`).
- **View** (`src/pages/`) — Componenti React che si limitano a renderizzare la UI e delegare la gestione degli eventi ai metodi esposti dai ViewModel.

---

## Prerequisiti

- **Node.js** — versione 18.x o superiore
- **npm** — incluso con Node.js
- **Backend API** — istanza del server Python (FastAPI) attiva

---

## Installazione e Avvio

### 1. Installazione dipendenze

```bash
npm install
```

### 2. Avvio server di sviluppo

```bash
npm run dev
```

L'applicazione sarà disponibile su: [http://localhost:5173](http://localhost:5173)