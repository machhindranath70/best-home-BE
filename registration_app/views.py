from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from .models import PropertyInfo
from .serializers import PropertyInfoSerializer
from rest_framework.decorators import api_view
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Registration successful",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyInfoListAPI(APIView):
    def get(self, request):
        data = PropertyInfo.objects.all()
        serializer = PropertyInfoSerializer(data, many=True)
        return Response(serializer.data)


class PropertyInfoByCityAPI(APIView):
    def get(self, request):
        city = request.GET.get('city')
        if not city:
            return Response({'error': 'City parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        properties = PropertyInfo.objects.filter(city__iexact=city)
        serializer = PropertyInfoSerializer(properties, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def nearby_properties_api(request):
    try:
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
        radius = float(request.GET.get('radius', 5000))  # Default 5000 meters
    except (TypeError, ValueError):
        return Response({"error": "Please provide valid lat, lon, and radius"}, status=400)

    user_location = Point(lon, lat, srid=4326)

    properties = PropertyInfo.objects.annotate(
        distance=Distance('location', user_location)
    ).filter(
        distance__lte=radius
    ).order_by('distance')

    serializer = PropertyInfoSerializer(properties, many=True)
    return Response(serializer.data)
