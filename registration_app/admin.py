
# Register your models here.
from django.contrib import admin
from .models import Registration
from .models import PropertyService

admin.site.register(Registration)

admin.site.register(PropertyService)
