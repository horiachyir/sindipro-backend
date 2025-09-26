from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_buildings, name='get_buildings'),
    path('all/', views.get_all_buildings, name='get_all_buildings'),
    path('create/', views.create_building, name='create_building'),
    path('<int:id>/', views.update_building, name='update_building'),
    path('<int:id>/units/', views.create_unit, name='create_unit'),
    path('<int:id>/units/export/excel/', views.export_units_excel, name='export_units_excel'),
    path('units/', views.get_units, name='get_units'),
    path('units/<int:id>/', views.update_unit, name='update_unit'),
]
