import requests
from sqlalchemy.orm import Session
from db.models import WeatherRecord

# Configuration
WEATHER_API_KEY = c7bc5bc56cf424afcb473fceb611cbe1
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str) -> dict:
    """Fetch live weather data from API"""
    try:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Weather API error: {str(e)}")

def save_weather_to_db(session: Session, city: str, data: dict) -> WeatherRecord:
    """Save weather data to database"""
    record = WeatherRecord(
        city=city,
        temperature=data['main']['temp'],
        feels_like=data['main']['feels_like'],
        conditions=data['weather'][0]['description'],
        humidity=data['main']['humidity'],
        wind_speed=data['wind']['speed'],
        pressure=data['main']['pressure']
    )
    session.add(record)
    session.commit()
    return record