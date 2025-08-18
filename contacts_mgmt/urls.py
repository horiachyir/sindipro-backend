from django.urls import path
from . import views

urlpatterns = [
    path('event/', views.create_event, name='create_event'),
]