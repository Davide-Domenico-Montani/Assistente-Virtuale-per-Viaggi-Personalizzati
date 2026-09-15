import chromadb
from chromadb.utils import embedding_functions
from sqlalchemy.orm import Session
from sqlalchemy import extract, or_
from langchain_core.tools import tool
from .model import Booking
import datetime
from typing import Optional

from .db.database import SessionLocal, get_db
from .model import Flight, Hotel, Activity

chroma_client = chromadb.PersistentClient(path="./chroma_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_collection(name="activities_rag", embedding_function=sentence_transformer_ef)


def get_db_session():
    """Funzione di supporto per ottenere la sessione SQLite nei Tool"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e


@tool
def search_activities_in_db(city: str, preferences: str) -> str:
    """
    Usa questo strumento per cercare attività ed esperienze turistiche nel database.

    DEVI passare esattamente questi due parametri:
    - city: La nazione o la città di interesse (es. 'Barcellona', 'Spagna'). Non usare la chiave 'city'.
    - preferences: Le preferenze o gli interessi dell'utente (es. 'relax', 'sport', 'cultura').
    """
    if not city:
        return "Errore: devi specificare una città."
    query_text = f"Attività a {city} per {preferences}"

    results = collection.query(
        query_texts=[query_text],
        n_results=2
    )

    if not results['documents'] or not results['documents'][0]:
        return "Nessuna attività trovata per queste preferenze."

    db = get_db_session()

    try:
        activities_str = ""
        for idx, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][idx]
            activity_id = metadata.get('activity_id')

            available_dates = "Date non specificate"
            if activity_id:
                db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
                if db_activity:
                    available_dates = db_activity.available_dates

            activities_str += f"- Attività: {doc} (Target: {metadata.get('target')}) | Date disponibili: {available_dates}\n"

        return activities_str
    finally:
        db.close()


@tool
def search_flights_and_hotels(destination: str, month: int) -> str:
    """
    Cerca voli e hotel disponibili nel database relazionale SQLite, controllando le date dispobili.
    """
    db = get_db_session()

    try:
        search_term = destination.split(',')[0].strip()
        hotels = db.query(Hotel).filter(
            or_(
                Hotel.country.ilike(f"%{search_term}%"),
                Hotel.city.ilike(f"%{search_term}%")
            )
        ).all()

        hotel_str = "\n".join([f"- {h.name} ({h.city}): {h.cost_per_night}€ a notte | Date disponibili: {h.available_dates}" for h in hotels])
        if not hotel_str:
            hotel_str = "Nessun hotel trovato."

        flights = db.query(Flight).filter(
            or_(
                Flight.destination_country.ilike(f"%{search_term}%"),
                Flight.arrival_airport.ilike(f"%{search_term}%")
            ),
            extract('month', Flight.date) == month
        ).all()

        flight_str = "\n".join(
            [f"- Da {f.departure_airport} a {f.arrival_airport} il {f.date}: {f.cost}€" for f in flights])
        if not flight_str:
            flight_str = "Nessun volo trovato."

        return f"HOTEL DISPONIBILI:\n{hotel_str}\n\nVOLI DISPONIBILI:\n{flight_str}"

    finally:
        db.close()


@tool
def book_itinerary(user_id: str, destination: str, details: str) -> str:
    """
    Usa questo strumento SOLO per CONFERMARE E PRENOTARE il viaggio.

    DEVI fornire ESATTAMENTE questi tre parametri:
    - user_id: L'ID utente che ti ho fornito nel prompt (es. 'D5abMq...').
    - destination: La città o nazione principale (es. 'Barcellona').
    - details: Un testo discorsivo che riassume i voli, l'hotel e le attività incluse.
    """
    db = next(get_db())

    try:
        nuova_prenotazione = Booking(
            user_id=user_id,
            destination=destination,
            details=details,
            total_cost=0.0
        )
        db.add(nuova_prenotazione)
        db.commit()

        return "SUCCESSO: Prenotazione salvata nel database. Informa l'utente che il viaggio è stato prenotato con successo!"
    except Exception as e:
        return f"ERRORE durante il salvataggio della prenotazione: {str(e)}"
    finally:
        db.close()