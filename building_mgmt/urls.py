from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_buildings, name='get_buildings'),
    path('create/', views.create_building, name='create_building'),
]
