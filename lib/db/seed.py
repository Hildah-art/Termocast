from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import WeatherRecord
from datetime import datetime, timedelta


def seed_weather_data():
    engine = create_engine("sqlite:///weather_data.db")
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        # Clear existing data
        session.query(WeatherRecord).delete()
        
        # Add test records
        test_data = [
            WeatherRecord(
                city="London",
                temperature=18.5,
                feels_like=17.2,
                conditions="cloudy",
                humidity=75,
                wind_speed=12.3,
                pressure=1012,
                timestamp=datetime.now() - timedelta(days=1)
            )
        ]
        
        session.add_all(test_data)
        session.commit()
        print("✅ Seeded test weather data")

if _name_ == "_main_":

    seed_weather_data( )
    