from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_equipment, name='list_equipment'),
    path('create/', views.create_equipment, name='create_equipment'),
]
