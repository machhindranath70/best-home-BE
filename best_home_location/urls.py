from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="Best Home Location API",
        default_version='v1',
        description="API documentation for Registration",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your@email.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('registration_app.urls')),

    # ✅ Set Swagger as homepage
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-home'),

    # Also available at /swagger/ if needed
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
