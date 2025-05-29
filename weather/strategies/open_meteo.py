import requests
from .base import APIWeather


class APIOpenMeteo(APIWeather):
    def get_weather(self, lat: float, lon: float) -> dict:
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,weather_code"
            )
        weather_resp = requests.get(weather_url).json()
        for i in range(len(weather_resp['hourly']['weather_code'])):
            if weather_resp['hourly']['time'][i][-5:] >= "21:00" or weather_resp['hourly']['time'][i][-5:] <= "05:00":
                weather_resp['hourly']['weather_code'][i] = "Ночь"
                continue
            weather_resp['hourly']['weather_code'][i] = self.get_status_weather_by_code(weather_resp['hourly']['weather_code'][i])
        
        weather_resp['current_weather']['weathercode'] = self.get_status_weather_by_code(weather_resp['current_weather']['weathercode'])
        return weather_resp
    
    def get_status_weather_by_code(self, code: int) -> str:
        weatherCodeMap = {
            0: "Солнце",
            1: "Солнце",
            2: "Облачно",
            3: "Облачно",
            45: "Облачно",
            48: "Облачно",
            51: "Дождь",
            53: "Дождь",
            55: "Дождь",
            56: "Дождь",
            57: "Дождь",
            61: "Дождь",
            63: "Дождь",
            65: "Дождь",
            66: "Дождь",
            67: "Дождь",
            71: "Снег",
            73: "Снег",
            75: "Снег",
            77: "Снег",
            80: "Дождь",
            81: "Дождь",
            82: "Дождь",
            85: "Снег",
            86: "Снег",
            95: "Дождь",
            96: "Град",
            99: "Град"
        }

        return weatherCodeMap[code]
