from weather.strategies.base import APIWeather
from weather.strategies.base import APIGeocoding

class WeatherContext:
    def __init__(self, weather_strategy: APIWeather, geocoding_strategy: APIGeocoding):
        self.weather_strategy = weather_strategy
        self.geocoding_strategy = geocoding_strategy
        
    def get_weather(self, city: str) -> dict:
        coordinates = self.geocoding_strategy.get_coordinates(city)

        if "error" in coordinates:
            return {"error": coordinates["error"]}
        
        lat = coordinates["latitude"]
        lon = coordinates["longitude"]

        return self.weather_strategy.get_weather(lat, lon)
        
    def autocomplete(self, query: str) -> list[str]:
        return self.geocoding_strategy.autocomplete(query)