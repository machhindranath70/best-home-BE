from django.urls import path
from .views import RegistrationAPIView
from .views import PropertyInfoListAPI
from .views import PropertyInfoByCityAPI


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('property-info/', PropertyInfoListAPI.as_view(), name='property-info'),
    path('property-info-by-city/', PropertyInfoByCityAPI.as_view(), name='property-info-by-city'),
]

