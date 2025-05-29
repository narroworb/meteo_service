from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from weather.models import CitySearch
import json

class WeatherViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_index_renders_form_and_last_cities(self):
        CitySearch.objects.create(user=self.user, city_name='Moscow')
        CitySearch.objects.create(user=self.user, city_name='London')

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Узнать погоду')
        self.assertContains(response, 'id="city-input"')
        self.assertContains(response, 'Moscow')
        self.assertContains(response, 'London')
        self.assertContains(response, 'Все мои запросы')

    def test_index_with_city_query_and_weather(self):
        city_name = 'Moscow'
        response = self.client.get(reverse('index'), {'city': city_name})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'value="{city_name}"')

        weather = response.context.get('weather')
        if weather:
            self.assertIn('temperature', weather)
            self.assertIn('windspeed', weather)
        weather_forecast = response.context.get('weather_forecast')
        if weather_forecast:
            self.assertIn('dates', weather_forecast)
            self.assertIn('temperatures', weather_forecast)
            self.assertIn('icons', weather_forecast)

        self.assertContains(response, 'id="tempChart"')

    def test_index_with_invalid_city_shows_error(self):
        response = self.client.get(reverse('index'), {'city': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введите город') 

        response = self.client.get(reverse('index'), {'city': 'НевалидныйГород123'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Город не найден')

    def test_last_cities_links(self):
        CitySearch.objects.create(user=self.user, city_name='Moscow')
        CitySearch.objects.create(user=self.user, city_name='Saint Petersburg')

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'href="/?city=Moscow"')
        self.assertContains(response, 'href="/?city=Saint Petersburg"')

    def test_user_search_stats_authenticated(self):
        self.client.login(username='testuser', password='12345')

        CitySearch.objects.create(user=self.user, city_name='Moscow')
        CitySearch.objects.create(user=self.user, city_name='Moscow')
        CitySearch.objects.create(user=self.user, city_name='London')

        response = self.client.get(reverse('user_search_stats'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Moscow')
        self.assertContains(response, 'London')
        self.assertContains(response, '2')
        self.assertContains(response, '1')

    def test_user_search_stats_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('user_search_stats'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)


class CitySearchModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user2', password='12345')

    def test_create_city_search(self):
        cs = CitySearch.objects.create(user=self.user, city_name='Paris')
        self.assertEqual(cs.city_name, 'Paris')
        self.assertEqual(cs.user.username, 'user2')
        self.assertIsNotNone(cs.search_datetime)
