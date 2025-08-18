from django.urls import path
from . import views

urlpatterns = [
    path('event/', views.event_handler, name='event_handler'),
]