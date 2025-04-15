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
from .views import UserAndPropertyRegisterAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import MyPropertyView
from .views import UpdateMyPropertyView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('property-info/', PropertyInfoListAPI.as_view(), name='property-info'),
    path('property-info-by-city/', PropertyInfoByCityAPI.as_view(), name='property-info-by-city'),
    # path('property-info-nearby/', nearby_properties, name='property-info-nearby'),  # ✅ function-based 
    path('property-info-nearby/', nearby_properties_api, name='property-info-nearby'),
    path('register-user-with-property/', UserAndPropertyRegisterAPI.as_view(), name='register-user-property'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 🔐 Login API
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 🔄 Refresh token
    path('my-profile/', MyPropertyView.as_view(), name='my-profile'),
    path('update-property/', UpdateMyPropertyView.as_view(), name='update-property'),

]

