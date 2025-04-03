from django.urls import path
from .views import RegistrationAPIView
from .views import PropertyInfoListAPI


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('property-info/', PropertyInfoListAPI.as_view(), name='property-info'),
]
