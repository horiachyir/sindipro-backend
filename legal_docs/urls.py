from django.urls import path
from . import views

urlpatterns = [
    path('template/', views.create_legal_template, name='create_legal_template'),
]
