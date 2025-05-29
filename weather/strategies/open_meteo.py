import requests
from .base import APIWeather


class APIOpenMeteo(APIWeather):
    def get_weather(self, lat: float, lon: float) -> dict:
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
            )
        weather_resp = requests.get(weather_url).json()
        return weather_resp