from django.urls import path
# from .views import RegistrationAPIView
# from .views import PropertyInfoListAPI
# from .views import PropertyInfoByCityAPI
from .views import nearby_properties_api
from .views import (
    RegistrationAPIView,
    PropertyInfoListAPI,
    PropertyInfoByCityAPI,  # ✅ Make sure this is included
)


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('property-info/', PropertyInfoListAPI.as_view(), name='property-info'),
    path('property-info-by-city/', PropertyInfoByCityAPI.as_view(), name='property-info-by-city'),
    # path('property-info-nearby/', nearby_properties, name='property-info-nearby'),  # ✅ function-based 
    path('property-info-nearby/', nearby_properties_api, name='property-info-nearby'),

]

