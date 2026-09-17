import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import chromadb
from chromadb.utils import embedding_functions
from src.model import Base, Flight, Hotel, Activity

engine = create_engine('sqlite:///travel_agency.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

chroma_client = chromadb.PersistentClient(path="./chroma_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="activities_rag", embedding_function=sentence_transformer_ef)


def seed_data():

    destinations = [
        ("Spagna", "Barcellona", "BCN"),
        ("Francia", "Parigi", "CDG"),
        ("Regno Unito", "Londra", "LHR"),
        ("Germania", "Berlino", "BER"),
        ("Italia", "Roma", "FCO"),
        ("Giappone", "Tokyo", "NRT"),
        ("Stati Uniti", "New York", "JFK"),
        ("Australia", "Sydney", "SYD"),
        ("Emirati Arabi", "Dubai", "DXB"),
        ("Indonesia", "Bali", "DPS")
    ]

    #Voli
    flights = []
    for country, city, code in destinations:
        # Voli Luglio
        flights.append(
            Flight(destination_country=country, departure_airport="MXP (Milano)", arrival_airport=f"{code} ({city})",
                   date=datetime.date(2026, 7, 10), cost=150.0))
        flights.append(
            Flight(destination_country=country, departure_airport=f"{code} ({city})", arrival_airport="MXP (Milano)",
                   date=datetime.date(2026, 7, 17), cost=180.0))
        # Voli Ottobre
        flights.append(
            Flight(destination_country=country, departure_airport="MXP (Milano)", arrival_airport=f"{code} ({city})",
                   date=datetime.date(2026, 10, 10), cost=130.0))
        flights.append(
            Flight(destination_country=country, departure_airport=f"{code} ({city})", arrival_airport="MXP (Milano)",
                   date=datetime.date(2026, 10, 17), cost=160.0))

    session.add_all(flights)

    #Alberghi
    hotels = [
        # Barcellona
        Hotel(name="W Barcelona", country="Spagna", city="Barcellona", cost_per_night=250.0,
              available_dates="Tutto l'anno"),
        Hotel(name="Hostel Fiesta", country="Spagna", city="Barcellona", cost_per_night=45.0,
              available_dates="Tutto l'anno"),
        # Parigi
        Hotel(name="Ritz Paris", country="Francia", city="Parigi", cost_per_night=450.0,
              available_dates="Tutto l'anno"),
        Hotel(name="Le Montclair Hostel", country="Francia", city="Parigi", cost_per_night=50.0,
              available_dates="Tutto l'anno"),
        # Londra
        Hotel(name="The Savoy", country="Regno Unito", city="Londra", cost_per_night=400.0,
              available_dates="Tutto l'anno"),
        Hotel(name="Wombat's City Hostel", country="Regno Unito", city="Londra", cost_per_night=40.0,
              available_dates="Tutto l'anno"),
        # Berlino
        Hotel(name="Adlon Kempinski", country="Germania", city="Berlino", cost_per_night=300.0,
              available_dates="Tutto l'anno"),
        Hotel(name="Generator Hostel", country="Germania", city="Berlino", cost_per_night=35.0,
              available_dates="Tutto l'anno"),
        # Roma
        Hotel(name="Hassler Roma", country="Italia", city="Roma", cost_per_night=350.0, available_dates="Tutto l'anno"),
        Hotel(name="YellowSquare", country="Italia", city="Roma", cost_per_night=30.0, available_dates="Tutto l'anno"),
        # Tokyo
        Hotel(name="Park Hyatt", country="Giappone", city="Tokyo", cost_per_night=350.0,
              available_dates="Tutto l'anno"),
        Hotel(name="Nine Hours Capsule", country="Giappone", city="Tokyo", cost_per_night=40.0,
              available_dates="Tutto l'anno"),
        # New York
        Hotel(name="The Plaza", country="Stati Uniti", city="New York", cost_per_night=500.0,
              available_dates="Tutto l'anno"),
        Hotel(name="HI NYC Hostel", country="Stati Uniti", city="New York", cost_per_night=60.0,
              available_dates="Tutto l'anno"),
        # Sydney
        Hotel(name="Four Seasons", country="Australia", city="Sydney", cost_per_night=280.0,
              available_dates="Tutto l'anno"),
        Hotel(name="Wake Up! Sydney", country="Australia", city="Sydney", cost_per_night=35.0,
              available_dates="Tutto l'anno"),
        # Dubai
        Hotel(name="Burj Al Arab", country="Emirati Arabi", city="Dubai", cost_per_night=800.0,
              available_dates="Tutto l'anno"),
        Hotel(name="Rove Downtown", country="Emirati Arabi", city="Dubai", cost_per_night=80.0,
              available_dates="Tutto l'anno"),
        # Bali
        Hotel(name="Ayana Resort", country="Indonesia", city="Bali", cost_per_night=200.0,
              available_dates="Tutto l'anno"),
        Hotel(name="The Farm Hostel", country="Indonesia", city="Bali", cost_per_night=20.0,
              available_dates="Tutto l'anno")
    ]
    session.add_all(hotels)

    #Attività
    activities_sql = [
        # BCN
        Activity(id=1, name="Tour Tapas", country="Spagna", city="Barcellona", cost=50.0,
                 available_dates="Tutto l'anno"),
        Activity(id=2, name="Surf Class", country="Spagna", city="Barcellona", cost=35.0,
                 available_dates="Maggio - Settembre 2026"),
        # CDG
        Activity(id=3, name="Tour del Louvre", country="Francia", city="Parigi", cost=70.0,
                 available_dates="Tutto l'anno"),
        Activity(id=4, name="Crociera sulla Senna", country="Francia", city="Parigi", cost=25.0,
                 available_dates="Maggio - Ottobre 2026"),
        # LHR
        Activity(id=5, name="London Eye", country="Regno Unito", city="Londra", cost=35.0,
                 available_dates="Tutto l'anno"),
        Activity(id=6, name="Pub Crawl Storico", country="Regno Unito", city="Londra", cost=20.0,
                 available_dates="Tutto l'anno"),
        # BER
        Activity(id=7, name="Tour Muro di Berlino", country="Germania", city="Berlino", cost=15.0,
                 available_dates="Tutto l'anno"),
        Activity(id=8, name="Ingresso Club Techno", country="Germania", city="Berlino", cost=25.0,
                 available_dates="Tutto l'anno"),
        # FCO
        Activity(id=9, name="Tour Colosseo", country="Italia", city="Roma", cost=30.0, available_dates="Tutto l'anno"),
        Activity(id=10, name="Corso di Pasta Fresca", country="Italia", city="Roma", cost=60.0,
                 available_dates="Tutto l'anno"),
        # NRT
        Activity(id=11, name="Masterclass di Sushi", country="Giappone", city="Tokyo", cost=80.0,
                 available_dates="Tutto l'anno"),
        Activity(id=12, name="Escursione Monte Fuji", country="Giappone", city="Tokyo", cost=120.0,
                 available_dates="Maggio - Novembre 2026"),
        # JFK
        Activity(id=13, name="Statua della Libertà", country="Stati Uniti", city="New York", cost=40.0,
                 available_dates="Tutto l'anno"),
        Activity(id=14, name="Bici in Central Park", country="Stati Uniti", city="New York", cost=20.0,
                 available_dates="Aprile - Ottobre 2026"),
        # SYD
        Activity(id=15, name="Tour Opera House", country="Australia", city="Sydney", cost=50.0,
                 available_dates="Tutto l'anno"),
        Activity(id=16, name="Lezione Surf Bondi Beach", country="Australia", city="Sydney", cost=45.0,
                 available_dates="Settembre - Aprile 2026"),
        # DXB
        Activity(id=17, name="Safari nel Deserto", country="Emirati Arabi", city="Dubai", cost=90.0,
                 available_dates="Tutto l'anno"),
        Activity(id=18, name="Ticket Burj Khalifa", country="Emirati Arabi", city="Dubai", cost=45.0,
                 available_dates="Tutto l'anno"),
        # DPS
        Activity(id=19, name="Tour dei Templi", country="Indonesia", city="Bali", cost=25.0,
                 available_dates="Tutto l'anno"),
        Activity(id=20, name="Ritiro Yoga", country="Indonesia", city="Bali", cost=15.0, available_dates="Tutto l'anno")
    ]
    session.add_all(activities_sql)

    session.commit()
    print("Dati SQL (Voli, Hotel, Attività per 10 città) inseriti con successo!")

    #Dati vettoriali

    documents = [
        "Tour gastronomico delle migliori Tapas di Barcellona. Ideale per coppie e amanti del cibo.",
        "Lezione di surf per principianti sulla spiaggia della Barceloneta. Ideale per giovani, sportivi e amanti dell'adrenalina.",
        "Esplora i capolavori del Museo del Louvre con una guida esperta. Ideale per appassionati d'arte e cultura.",
        "Romantica crociera al tramonto lungo la Senna. Perfetto per coppie in cerca di relax.",
        "Goditi una vista mozzafiato sulla città dalla ruota panoramica London Eye. Adatto a famiglie e turisti.",
        "Serata all'insegna del divertimento nei pub storici di Londra. Perfetto per i giovani e la nightlife.",
        "Camminata storica lungo i resti del Muro di Berlino. Altamente educativo, per appassionati di storia.",
        "Scopri la celebre vita notturna berlinese in un iconico club techno. Esclusivo per giovani adulti e amanti della musica.",
        "Immergiti nella storia dell'Antica Roma con un tour completo del Colosseo. Culturale e imperdibile per famiglie.",
        "Impara a cucinare la vera pasta italiana con uno chef locale. Rilassante, divertente, ideale per coppie e buongustai.",
        "Scopri i segreti della preparazione del sushi a Tokyo. Perfetto per foodie e amanti della cultura giapponese.",
        "Fuggi dalla città per un'escursione naturalistica al Monte Fuji. Ideale per sportivi e amanti dei paesaggi.",
        "Visita il monumento simbolo degli Stati Uniti d'America. Classica esperienza culturale per tutti i target.",
        "Noleggia una bici ed esplora il polmone verde di New York. Attività fisica leggera, ideale per giovani e relax.",
        "Scopri i segreti architettonici della Sydney Opera House. Molto culturale, adatto a un pubblico adulto.",
        "Cavalca le onde nella spiaggia più famosa d'Australia. Sport estremo ma guidato, per giovani dinamici.",
        "Adrenalina pura sulle dune di sabbia seguita da cena beduina. Sport e cultura araba fusi insieme.",
        "Ammira Dubai dal grattacielo più alto del mondo. Attività tranquilla e panoramica, ideale per il relax.",
        "Escursione spirituale tra i templi sacri di Bali. Profondamente culturale e rilassante, per esploratori.",
        "Sessione di yoga all'aperto immersi nella giungla balinese. Il massimo del relax e della meditazione per viaggiatori solitari o coppie."
    ]

    metadatas = [
        {"target": "foodie, coppie", "type": "nightlife", "activity_id": 1},
        {"target": "giovani, sportivi", "type": "sport", "activity_id": 2},
        {"target": "cultura, adulti", "type": "cultura", "activity_id": 3},
        {"target": "coppie, relax", "type": "relax", "activity_id": 4},
        {"target": "famiglie, relax", "type": "relax", "activity_id": 5},
        {"target": "giovani, nightlife", "type": "nightlife", "activity_id": 6},
        {"target": "cultura, storia", "type": "cultura", "activity_id": 7},
        {"target": "giovani, nightlife", "type": "nightlife", "activity_id": 8},
        {"target": "famiglie, storia", "type": "cultura", "activity_id": 9},
        {"target": "foodie, coppie", "type": "relax", "activity_id": 10},
        {"target": "foodie, cultura", "type": "cultura", "activity_id": 11},
        {"target": "sportivi, natura", "type": "sport", "activity_id": 12},
        {"target": "famiglie, storia", "type": "cultura", "activity_id": 13},
        {"target": "giovani, relax", "type": "sport", "activity_id": 14},
        {"target": "cultura, adulti", "type": "cultura", "activity_id": 15},
        {"target": "giovani, sportivi", "type": "sport", "activity_id": 16},
        {"target": "sportivi, giovani", "type": "sport", "activity_id": 17},
        {"target": "coppie, relax", "type": "relax", "activity_id": 18},
        {"target": "esploratori, cultura", "type": "cultura", "activity_id": 19},
        {"target": "solitari, relax", "type": "relax", "activity_id": 20}
    ]

    ids = [f"act_{i}" for i in range(1, 21)]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print("Dati Vettoriali (RAG) per 10 città inseriti con successo!")


if __name__ == "__main__":
    seed_data()