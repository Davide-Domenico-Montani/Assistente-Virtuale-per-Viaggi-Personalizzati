from sqlalchemy import Column, Integer, String, Float, Text
from .base import Base

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    destination = Column(String)
    details = Column(Text)
    total_cost = Column(Float, nullable=True)
    status = Column(String, default="confirmed")