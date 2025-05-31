from sqlalchemy import Column, Integer, String, Float, DateTime, func
from .base import Base

class WeatherRecord(Base):
    """Stores historical weather data"""
    _tablename_ = "weather_records"
    
    id = Column(Integer, primary_key=True)
    city = Column(String)
    temperature = Column(Float)
    feels_like = Column(Float)
    conditions = Column(String)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    pressure = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())

    