from django.urls import path
from . import views

urlpatterns = [
    path('template/', views.legal_template_handler, name='legal_template_handler'),
    path('template/<int:template_id>/', views.update_legal_template, name='update_legal_template'),
]
