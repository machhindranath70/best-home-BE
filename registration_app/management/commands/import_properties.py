import csv
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from registration_app.models import PropertyInfo


class Command(BaseCommand):
    help = 'Import property data from CSV'

    def handle(self, *args, **kwargs):
        with open(r'E:\Mach\best home\home-search\best_home_location\data\property_data.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lat = float(row['latitude'])
                lon = float(row['longitude'])
                location = Point(lon, lat)

                prop = PropertyInfo(
                    name=row.get('name', ''),
                    site=row.get('site', ''),
                    subtypes=row.get('subtypes', ''),
                    category=row.get('category', ''),
                    type=row.get('type', ''),
                    phone=row.get('phone', ''),
                    full_address=row.get('full_address', ''),
                    city=row.get('city', ''),
                    latitude=lat,
                    longitude=lon,
                    location=location,
                    rating=row.get('rating') or None,
                    reviews_link=row.get('reviews_link', ''),
                    reviews_tags=row.get('reviews_tags', ''),
                    photo=row.get('photo', ''),
                    street_view=row.get('street_view', ''),
                )
                prop.save()

        self.stdout.write(self.style.SUCCESS("Properties imported successfully"))
