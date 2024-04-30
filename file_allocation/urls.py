# file_allocation/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.filter_data, name='filter_data'),
    path('get_options/', views.get_options, name='get_options'),
]
