from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_buildings, name='get_buildings'),
    path('create/', views.create_building, name='create_building'),
    path('<int:tower_id>/units/', views.create_unit, name='create_unit'),
    path('units/', views.get_units, name='get_units'),
]
