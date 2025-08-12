from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_consumption_register, name='create_consumption_register'),
    path('account/', views.create_consumption_account, name='create_consumption_account'),
]
