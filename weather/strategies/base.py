from abc import ABC, abstractmethod

class APIWeather(ABC):
    @abstractmethod
    def get_weather(self, lat: float, lon: float) -> dict:
        pass

class APIGeocoding(ABC):
    @abstractmethod
    def get_coordinates(self, city: str) -> dict:
        pass

    @abstractmethod
    def autocomplete(self, query: str) -> list[str]:
        pass

    
