from rest_framework import serializers
from .models import Registration
from .models import PropertyInfo
from .models import PropertyService

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class PropertyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyInfo
        fields = '__all__'


class PropertyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyService
        fields = '__all__'
