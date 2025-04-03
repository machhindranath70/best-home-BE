import csv
from django.core.management.base import BaseCommand
from registration_app.models import PropertyInfo


def safe_float(value):
    try:
        return float(value)
    except:
        return None

class Command(BaseCommand):
    help = 'Import data from CSV into PropertyInfo table'

    def handle(self, *args, **kwargs):
        with open('data/property_data.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                PropertyInfo.objects.create(
                    name=row['name'],
                    site=row['site'],
                    subtypes=row['subtypes'],
                    category=row['category'],
                    type=row['type'],
                    phone=row['phone'],
                    full_address=row['full_address'],
                    city=row['city'],
                    latitude=safe_float(row['latitude']),
                    longitude=safe_float(row['longitude']),
                    rating=safe_float(row['rating']),
                    reviews_link=row['reviews_link'],
                    reviews_tags=row['reviews_tags'],
                    photo=row['photo'],
                    street_view=row['street_view'],
                )
        self.stdout.write(self.style.SUCCESS("✅ Data imported successfully"))
