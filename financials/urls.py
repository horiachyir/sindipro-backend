from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.financial_account_view, name='financial_account_view'),
]
