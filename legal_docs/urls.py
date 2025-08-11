from django.urls import path
from . import views

urlpatterns = [
    path('template/', views.legal_template_handler, name='legal_template_handler'),
]
