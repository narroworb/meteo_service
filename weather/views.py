from django.shortcuts import render
from weather.services.weather_context import WeatherContext
from weather.strategies.open_meteo import APIOpenMeteo
from weather.strategies.open_meteo_geo import APIOpenMeteoGeo
from django.http import JsonResponse

geocoding_strategy = APIOpenMeteoGeo()
weather_strategy = APIOpenMeteo()
        
context = WeatherContext(weather_strategy, geocoding_strategy)


def index(request):
    weather_data = None
    error = None

    city = request.GET.get("city")
    if city:
        # parsed_city = parse_city(city)
        # print(city)
        result = context.get_weather(city)

        if "error" in result:
            error = result["error"]
        else:
            weather_data = result.get("current_weather", {})


    print(weather_data)
    return render(request, "weather/index.html", {
        "weather": weather_data,
        "error": error,
        "city": city
    })

def autocomplete_city(request):
    query = request.GET.get("q", "")

    results = context.autocomplete(query)

    print(results)

    return JsonResponse({"results": results})


    
