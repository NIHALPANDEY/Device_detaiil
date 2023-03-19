from django.urls import path
from .views import get_device_info, get_device_location, get_all_location

urlpatterns = [
    path('get_device_info', get_device_info, name='get_device_info'),
    path('get_device_location', get_device_location, name='get_device_location'),
    path('get_all_location', get_all_location, name='get_all_location')
]