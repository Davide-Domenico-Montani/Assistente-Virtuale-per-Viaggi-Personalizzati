from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.model import Activity, Booking, User
from src.auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional
from src.agent import get_chat_response
from fastapi.middleware.cors import CORSMiddleware
from src.model.UserItinerary import UserItinerary

app = FastAPI(title="Travel Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Benvenuto nel backend dell'Assistente Viaggi!"}

@app.get("/api/activities")
def get_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()


@app.get("/api/me")
def get_user_profile(db: Session = Depends(get_db)):
    """
    MOCK: Ritorna il primo utente nel database simulando un login.
    """
    mock_user = db.query(User).first()
    return mock_user


@app.get("/api/bookings")
def get_user_bookings(db: Session = Depends(get_db)):
    """
    MOCK: Ritorna le prenotazioni del primo utente.
    """
    mock_user = db.query(User).first()

    # Se per qualche motivo il DB è vuoto, evitiamo errori
    if not mock_user:
        return []

    bookings = db.query(Booking).filter(Booking.user_id == mock_user.id).all()
    return bookings


class MessageInput(BaseModel):
    role: str  # "user" o "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[MessageInput] = []
    user_id: str

class ChatResponse(BaseModel):
    reply: str
    # In futuro qui aggiungeremo l'oggetto "itinerary" quando l'AI lo genera
    itinerary: Optional[dict] = None


@app.post("/api/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        ai_reply = get_chat_response(user_message=request.message, history=request.history, user_id=request.user_id)
        new_itinerary = UserItinerary(
            user_id=request.user_id,
            user_message=request.message,
            ai_response=ai_reply
        )
        db.add(new_itinerary)
        db.commit()

        return ChatResponse(reply=ai_reply, itinerary=None)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return ChatResponse(reply=f"Errore del server: {str(e)}")

@app.get("/api/bookings/{user_id}")
def get_user_bookings(user_id: str, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    return {"bookings": bookings}


@app.delete("/api/bookings/{booking_id}")
def delete_booking(booking_id: int, user_id: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata o non autorizzata")

    db.delete(booking)
    db.commit()

    return {"message": "Prenotazione eliminata con successo"}