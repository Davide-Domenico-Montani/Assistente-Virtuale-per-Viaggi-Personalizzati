from sqlalchemy import Column, Integer, String, Float

from .base import Base

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    available_dates = Column(String, default="Tutto l'anno")