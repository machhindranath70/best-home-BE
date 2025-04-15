from django.core.management.base import BaseCommand
from registration_app.models import PropertyInfo
import random
import string

class Command(BaseCommand):
    help = 'Auto-fill missing phone numbers and generate machine passwords for PropertyInfo records'

    def handle(self, *args, **kwargs):
        updated = 0
        for property in PropertyInfo.objects.all():
            changed = False

            # If phone is missing, use name
            if not property.phone:
                property.phone = (property.name or 'Unknown')[:10]  # 👈 Take only first 10 characters


            # If password is missing, generate a new one
            if not property.password:
                property.password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                changed = True

            if changed:
                property.save()
                updated += 1
                self.stdout.write(f"✅ Updated: {property.name} | phone: {property.phone} | password: {property.password}")

        self.stdout.write(self.style.SUCCESS(f'Finished. Total properties updated: {updated}'))
