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

from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
import random
import string
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated

import base64

def encode_image_to_base64(image_file):
    if not image_file:
        return None
    return base64.b64encode(image_file.read()).decode('utf-8')


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

class UpdateMyPropertyView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        try:
            property = PropertyInfo.objects.get(phone=request.user.username)
        except PropertyInfo.DoesNotExist:
            return Response({"error": "No property found for this user"}, status=404)

        serializer = PropertyInfoSerializer(property, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Property updated successfully",
                "property": serializer.data
            })
        return Response(serializer.errors, status=400)

class PropertyInfoByCityAPI(APIView):
    def get(self, request):
        city = request.GET.get('city')
        if not city:
            return Response({'error': 'City parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        properties = PropertyInfo.objects.filter(city__iexact=city)
        serializer = PropertyInfoSerializer(properties, many=True)
        return Response(serializer.data)

class MyPropertyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            property = PropertyInfo.objects.get(phone=request.user.username)
            serializer = PropertyInfoSerializer(property)
            return Response({
                "user": request.user.username,
                "email": request.user.email,
                "property": serializer.data
            })
        except PropertyInfo.DoesNotExist:
            return Response({"error": "No property found for this user"}, status=404)



class UserAndPropertyRegisterAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Register a user and their property in one request.",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, description="Username", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('email', openapi.IN_FORM, description="Email", type=openapi.TYPE_STRING),
            openapi.Parameter('password', openapi.IN_FORM, description="Password", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('site', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('subtypes', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('category', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('phone', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('full_address', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('city', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('latitude', openapi.IN_FORM, type=openapi.TYPE_NUMBER, format='float'),
            openapi.Parameter('longitude', openapi.IN_FORM, type=openapi.TYPE_NUMBER, format='float'),
            openapi.Parameter('photo', openapi.IN_FORM, type=openapi.TYPE_FILE),
            openapi.Parameter('rating', openapi.IN_FORM, type=openapi.TYPE_NUMBER, format='float'),
            openapi.Parameter('reviews_link', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('reviews_tags', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('street_view', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ],
        responses={201: openapi.Response('User and Property Registered')}
    )


    def post(self, request):
        data = request.data.copy()

        # Step 1: Create User
        # username = data.get('username')
        raw_username = data.get('username', '')
        cleaned_phone = raw_username.replace(" ", "").replace("+91", "").strip()
        username = cleaned_phone
        email = data.get('email', '')
        password = data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=400)

        # user = User.objects.create_user(username=username, email=email, password=password)
        user = User.objects.create_user(username=username, email=email, password=password)
        data['phone'] = username  # Ensure phone matches login username

        # Step 2: Link Property to User
        data['owner'] = user.id
        photo_file = request.FILES.get('photo')
        if photo_file:
            data['photo'] = encode_image_to_base64(photo_file)

        serializer = PropertyInfoSerializer(data=data)
        if serializer.is_valid():
            property_instance = serializer.save()
            property_instance.user = user  # 💥 Now this works!
            property_instance.save()
            # serializer.save()
            return Response({
                "message": "User and Property registered successfully.",
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
                "property": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            user.delete()  # Rollback if property fails
            return Response(serializer.errors, status=400)
        

class LoginTokenView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Login using phone number (username) and password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Phone number used as username"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="Auto-generated or provided password"),
            },
        ),
        responses={200: openapi.Response('JWT token pair')}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
        

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
