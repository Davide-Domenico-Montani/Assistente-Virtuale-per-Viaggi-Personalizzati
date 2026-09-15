from sqlalchemy import Column, Integer, String, Float, Date
from .base import Base


class Flight(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    destination_country = Column(String, nullable=False)
    departure_airport = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    cost = Column(Float, nullable=False)