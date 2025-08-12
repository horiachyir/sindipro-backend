from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.field_requests, name='field-requests'),
]
