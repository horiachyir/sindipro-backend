from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_buildings, name='get_buildings'),
    path('all/', views.get_all_buildings, name='get_all_buildings'),
    path('create/', views.create_building, name='create_building'),
    path('<int:id>/', views.update_building, name='update_building'),
    path('<int:id>/units/', views.create_unit, name='create_unit'),
    path('units/', views.get_units, name='get_units'),
]
