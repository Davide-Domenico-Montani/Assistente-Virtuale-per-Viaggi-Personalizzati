import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import chromadb
from chromadb.utils import embedding_functions
from src.model import Base, User, Flight, Hotel, Activity, Booking
from src.model.UserItinerary import UserItinerary

engine = create_engine('sqlite:///travel_agency.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

chroma_client = chromadb.PersistentClient(path="./chroma_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="activities_rag", embedding_function=sentence_transformer_ef)


def seed_data():
    user = User(name="Mario Rossi", email="mario@example.com")
    session.add(user)
    flights = [
        Flight(destination_country="Spagna", departure_airport="MXP (Milano)", arrival_airport="BCN (Barcellona)",
               date=datetime.date(2026, 7, 10), cost=150.0),
        Flight(destination_country="Spagna", departure_airport="BCN (Barcellona)", arrival_airport="MXP (Milano)",
               date=datetime.date(2026, 7, 17), cost=180.0),
        Flight(destination_country="Spagna", departure_airport="MXP (Milano)", arrival_airport="BCN (Barcellona)",
               date=datetime.date(2026, 10, 10), cost=150.0),
        Flight(destination_country="Spagna", departure_airport="BCN (Barcellona)", arrival_airport="MXP (Milano)",
               date=datetime.date(2026, 10, 17), cost=180.0)
    ]
    session.add_all(flights)

    # Alberghi
    hotels = [
        Hotel(name="Hotel Mare Blu", country="Spagna", city="Barcellona", cost_per_night=120.0, available_dates="Giugno, Luglio, Agosto 2026"),
        Hotel(name="Hostel Fiesta", country="Spagna", city="Barcellona", cost_per_night=45.0, available_dates="Tutto l'anno")
    ]
    session.add_all(hotels)

    # Attività SQL
    activities_sql = [
        Activity(id=1, name="Tour Tapas", country="Spagna", city="Barcellona", cost=50.0, available_dates="Tutto l'anno"),
        Activity(id=2, name="Surf Class", country="Spagna", city="Barcellona", cost=35.0, available_dates="Maggio - Settembre 2026"),
        Activity(id=3, name="Museo Picasso", country="Spagna", city="Barcellona", cost=25.0, available_dates="Tutto l'anno")
    ]
    session.add_all(activities_sql)

    session.commit()
    print("Dati SQL inseriti con successo!")

    # --- DATI VETTORIALI  ---

    documents = [
        "Tour gastronomico delle migliori Tapas di Barcellona. Ideale per coppie e amanti del cibo.",
        "Lezione di surf per principianti sulla spiaggia della Barceloneta. Ideale per giovani, sportivi e amanti dell'adrenalina.",
        "Visita guidata al Museo d'Arte di Picasso. Esperienza tranquilla, culturale, ideale per famiglie e appassionati di storia."
    ]

    metadatas = [
        {"target": "foodie, coppie", "type": "nightlife", "activity_id": 1},
        {"target": "giovani, sportivi", "type": "sport", "activity_id": 2},
        {"target": "famiglie, relax", "type": "cultura", "activity_id": 3}
    ]

    ids = ["act_1", "act_2", "act_3"]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print("Dati Vettoriali inseriti con successo!")


if __name__ == "__main__":
    seed_data()