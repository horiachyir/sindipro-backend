from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_equipment, name='create_equipment'),
]
