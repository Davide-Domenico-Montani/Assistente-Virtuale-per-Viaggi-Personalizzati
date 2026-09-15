from sqlalchemy import Column, Integer, String, Text
from .base import Base



class UserItinerary(Base):
    __tablename__ = "user_itineraries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    user_message = Column(Text)
    ai_response = Column(Text)