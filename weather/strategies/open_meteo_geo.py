import requests
from .base import APIGeocoding

class APIOpenMeteoGeo(APIGeocoding):
    def get_coordinates(self, city: str) -> dict:
        city = self.parse_city(city)
        api_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&language=ru&count=1"
        if "|" in city:
            code = city[city.index("|")+1:]
            city = city[:city.index("|")] 
            api_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&country={code}&language=ru&count=1"
        api_resp = requests.get(api_url)
        data = api_resp.json()

        if not data.get("results"):
            return {"error": "Город не найден"}
        
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        
        return {
            "latitude": lat,
            "longitude": lon
        }
    
    def autocomplete(self, query: str) -> list[str]:
        api_url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=5&language=ru"
        api_resp = requests.get(api_url)
        api_resp.raise_for_status()
        data = api_resp.json()

        return [
            f"{item['name']}, {item['admin1']}, {item['country']} [{item['country_code']}]"
            for item in data.get("results", [])
        ]
    
    def parse_city(self, city: str) -> str:
        city_els = city.split(",")
        if len(city_els) == 1:
            return city
        elif len(city_els) == 2: 
            code = ''
            if "[" in city_els[1]:
                start_code = city_els[1].index("[") + 1
                end_code = city_els[1].index("]")
                
                code = city_els[1][start_code:end_code]
            return city_els[0] + "|" + code
        elif len(city_els) == 3: 
            code = ''
            if "[" in city_els[2]:
                start_code = city_els[2].index("[") + 1
                end_code = city_els[2].index("]")
                
                code = city_els[2][start_code:end_code]
            return city_els[0] + "|" + code