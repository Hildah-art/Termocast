import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .helpers import fetch_weather, save_weather_to_db
from db.base import Base
from db.models import WeatherRecord

# Database setup
engine = create_engine("sqlite:///weather_data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@click.group()
def cli():
    """Weather Monitoring CLI"""
    pass

@cli.command()
@click.argument("city")
def weather(city):
    """Get current weather and save to DB"""
    try:
        # Fetch data
        data = fetch_weather(city)
        
        # Display results
        click.secho(f"\n🌦 Live Weather in {city}:", fg="cyan", bold=True)
        click.echo(f"  - Conditions: {data['weather'][0]['description'].title()}")
        click.echo(f"  - Temperature: {data['main']['temp']}°C (Feels like {data['main']['feels_like']}°C)")
        click.echo(f"  - Humidity: {data['main']['humidity']}%")
        click.echo(f"  - Wind: {data['wind']['speed']} km/h")
        click.echo(f"  - Pressure: {data['main']['pressure']} hPa")
        
        # Save to database
        with Session() as session:
            record = save_weather_to_db(session, city, data)
            click.secho(f"\n✅ Saved to database (Record ID: {record.id})", fg="green")
            
    except Exception as e:
        click.secho(f"❌ Error: {str(e)}", fg="red")

@cli.command()
def history():
    """Show weather query history"""
    with Session() as session:
        records = session.query(WeatherRecord).order_by(WeatherRecord.timestamp.desc()).limit(10).all()
        
        if not records:
            click.secho("No weather records found", fg="yellow")
            return
            
        click.secho("\n⏳ Last 10 Weather Queries:", fg="blue", bold=True)
        for record in records:
            click.echo(f"\n📅 {record.timestamp} | 🌍 {record.city}")
            click.echo(f"  - Temp: {record.temperature}°C (Felt like {record.feels_like}°C)")
            click.echo(f"  - Conditions: {record.conditions}")
            click.echo(f"  - Wind: {record.wind_speed} km/h")

if _name_ == "_main_":
    cli()