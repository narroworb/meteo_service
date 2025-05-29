from django.shortcuts import render
from weather.services.weather_context import WeatherContext
from weather.strategies.open_meteo import APIOpenMeteo
from weather.strategies.open_meteo_geo import APIOpenMeteoGeo
from django.http import JsonResponse

geocoding_strategy = APIOpenMeteoGeo()
weather_strategy = APIOpenMeteo()
        
context = WeatherContext(weather_strategy, geocoding_strategy)


def index(request):
    cur_weather_data = None
    fut_weather_data = None
    error = None
    weather_forecast = None

    city = request.GET.get("city")
    if city:
        result = context.get_weather(city)

        if "error" in result:
            error = result["error"]
        else:
            cur_weather_data = result.get("current_weather", {})
            fut_weather_data = result.get("hourly", {})

            weather_forecast = {
                "dates": fut_weather_data['time'],
                "temperatures": fut_weather_data['temperature_2m'],
                "icons": [get_icon_name(code) for code in fut_weather_data["weather_code"]]
            }


    print(fut_weather_data)

    return render(request, "weather/index.html", {
        "weather": cur_weather_data,
        "error": error,
        "city": city,
        "weather_forecast": weather_forecast
    })

def autocomplete_city(request):
    query = request.GET.get("q", "")

    results = context.autocomplete(query)

    print(results)

    return JsonResponse({"results": results})


def get_icon_name(weathercode):
    if weathercode == "Солнце":
        return 'sunny.png'
    elif weathercode  == "Облачно":
        return 'cloudy.png'
    elif weathercode  == "Дождь":
        return 'rain.png'
    elif weathercode  == "Снег":
        return 'snow.png'
    elif weathercode == "Град":
        return 'hail.png'
    else:
        return 'night.png'
