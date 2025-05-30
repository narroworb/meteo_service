from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("autocomplete/", views.autocomplete_city, name="autocomplete_city"),
    path('login/', auth_views.LoginView.as_view(template_name='weather/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('my-searches/', views.user_search_stats, name='user_search_stats'),
]
