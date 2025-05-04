from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/random-fact/', views.get_random_fact, name='random_fact'),
]