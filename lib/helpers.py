import requests
from lib.db.models import Location, CurrentWeather, Forecast
from lib.db.base import get_db
from datetime import datetime, timedelta

class WeatherAPI:
    def _init_(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"
    
    def fetch_current(self, location):
        url = f"{self.base_url}/current.json?key={self.api_key}&q={location.latitude},{location.longitude}"
        response = requests.get(url)
        data = response.json()
        
        db = next(get_db())
        
        # Update current weather
        current = db.query(CurrentWeather).filter(CurrentWeather.location_id == location.id).first()
        if not current:
            current = CurrentWeather(location_id=location.id)
            db.add(current)
        
        current_data = data['current']
        current.temp_c = current_data['temp_c']
        current.temp_f = current_data['temp_f']
        current.condition_text = current_data['condition']['text']
        current.wind_kph = current_data['wind_kph']
        current.wind_dir = current_data['wind_dir']
        current.humidity = current_data['humidity']
        current.feelslike_c = current_data['feelslike_c']
        current.timestamp = datetime.now()
        
        db.commit()
    
    def fetch_forecast(self, location, days=3):
        url = f"{self.base_url}/forecast.json?key={self.api_key}&q={location.latitude},{location.longitude}&days={days}"
        response = requests.get(url)
        data = response.json()
        
        db = next(get_db())
        
        # Clear old forecasts
        db.query(Forecast).filter(Forecast.location_id == location.id).delete()
        
        # Add new forecasts
        for day in data['forecast']['forecastday']:
            daily = Forecast(
                location_id=location.id,
                forecast_date=datetime.strptime(day['date'], '%Y-%m-%d').date(),
                is_daily=True,
                maxtemp_c=day['day']['maxtemp_c'],
                mintemp_c=day['day']['mintemp_c'],
                chance_of_rain=day['day']['daily_chance_of_rain'],
                condition_text=day['day']['condition']['text']
            )
            db.add(daily)
        
        db.commit()