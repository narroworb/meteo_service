from django.shortcuts import render
from weather.services.weather_context import WeatherContext
from weather.strategies.open_meteo import APIOpenMeteo
from weather.strategies.open_meteo_geo import APIOpenMeteoGeo
from django.http import JsonResponse
from .models import CitySearch
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Count

geocoding_strategy = APIOpenMeteoGeo()
weather_strategy = APIOpenMeteo()
        
context = WeatherContext(weather_strategy, geocoding_strategy)

@login_required(login_url='login')
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
            
            user = request.user if request.user.is_authenticated else None
            CitySearch.objects.create(user=user, city_name=city)

    user = request.user if request.user.is_authenticated else None
    last_cities = CitySearch.objects.filter(user=user).values('city_name').distinct()[:5]

    return render(request, "weather/index.html", {
        "weather": cur_weather_data,
        "error": error,
        "city": city,
        "weather_forecast": weather_forecast,
        "last_cities": last_cities
    })

def autocomplete_city(request):
    query = request.GET.get("q", "")

    results = context.autocomplete(query)

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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'weather/register.html', {'form': form})


@login_required
def user_search_stats(request):
    stats = (
        CitySearch.objects
        .filter(user=request.user)
        .values('city_name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    return render(request, 'weather/user_search_stats.html', {'stats': stats})