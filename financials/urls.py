from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.create_financial_account, name='create_financial_account'),
]
