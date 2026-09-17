import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from .tools import search_activities_in_db, search_flights_and_hotels, book_itinerary
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0.1
)

tools = [search_activities_in_db, search_flights_and_hotels, book_itinerary]

system_prompt = """
Sei un assistente virtuale per un'agenzia di viaggi. 
Il tuo obiettivo è creare itinerari personalizzati e far prenotare l'utente.
Rispondi sempre in lingua italiana in modo conciso, empatico e professionale.

L'ID univoco dell'utente con cui stai parlando è: {user_id}

Devi raccogliere in modo naturale questi 4 dati fondamentali:
1. Nazione o Città di interesse
2. Periodo di viaggio (chiedi il mese e convertilo in numero, es. 7 per Luglio)
3. Budget totale
4. Preferenze sulle attività (es. cultura, sport, relax)

REGOLE IMPORTANTI:
- Se manca qualche informazione, fai domande gentili per scoprirla. Non fare più di due domande alla volta.
- QUANDO HAI RACCOLTO TUTTI E 4 I DATI, DEVI usare gli strumenti (search_activities_in_db e search_flights_and_hotels) per cercare voli, hotel e attività reali.
- NON inventare i dati, usa ESCLUSIVAMENTE quelli restituiti dagli strumenti.
- CONTROLLO DISPONIBILITÀ: Gli strumenti ti restituiranno il campo "available_dates" per gli hotel e le attività. DEVI LEGGERE ATTENTAMENTE queste date. NON DEVI MAI consigliare un hotel o un'attività se il mese richiesto dall'utente non è compreso nelle date di apertura. Le opzioni con "Tutto l'anno" vanno sempre bene.
- PRENOTAZIONE: Se l'utente ti chiede esplicitamente di prenotare, confermare o salvare l'itinerario che gli hai appena proposto, DEVI usare lo strumento di prenotazione (book_itinerary) passando l'ID utente indicato qui sopra. Dopo aver usato lo strumento, conferma all'utente che il viaggio è stato prenotato con successo.
- ESECUZIONE INVISIBILE: Non mostrare MAI all'utente il codice JSON o la dicitura "type: function" per chiamare gli strumenti. Gli strumenti vanno eseguiti silenziosamente in background. Attendi sempre di ricevere i risultati degli strumenti prima di dare la tua risposta finale.
- VOLI COMPLETI: Quando proponi l'itinerario, devi SEMPRE mostrare sia il volo di andata che il volo di ritorno. Calcola la data del ritorno in base alla durata del viaggio richiesta dall'utente.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def get_chat_response(user_message: str, history: list, user_id: str) -> str:
    formatted_history = []
    for msg in history:
        if isinstance(msg, dict):
            role = msg.get("role", "")
            content = msg.get("content", "")
        else:
            role = getattr(msg, "role", "")
            content = getattr(msg, "content", "")
        if role == "user":
            formatted_history.append(HumanMessage(content=content))
        else:
            formatted_history.append(AIMessage(content=content))

    try:
        response = agent_executor.invoke({
            "input": user_message,
            "chat_history": formatted_history,
            "user_id": user_id
        })
        return response["output"]
    except Exception as e:
        return f"Errore durante la generazione: {str(e)}"