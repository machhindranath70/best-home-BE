
# Create your models here.

from django.db import models

class Registration(models.Model):
    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('land', 'Land'),
    ]

    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    property_name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.property_name}"


class PropertyInfo(models.Model):
    name = models.CharField(max_length=100, blank=True)
    site = models.CharField(max_length=255, blank=True)
    subtypes = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    full_address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    reviews_link = models.TextField(blank=True)
    reviews_tags = models.TextField(blank=True)
    photo = models.TextField(blank=True)
    street_view = models.TextField(blank=True)

    def __str__(self):
        return self.name

