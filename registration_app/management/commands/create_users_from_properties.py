from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from registration_app.models import PropertyInfo

class Command(BaseCommand):
    help = 'Create User accounts from PropertyInfo table using phone as username and password column as password'

    def handle(self, *args, **kwargs):
        created_count = 0
        skipped = 0

        for prop in PropertyInfo.objects.all():
            username = (prop.phone or "").strip()
            password = (prop.password or "").strip()

            # Skip if no phone or password
            if not username or not password:
                self.stdout.write(f"⛔ Skipped: Missing phone or password for {prop.name}")
                skipped += 1
                continue

            if User.objects.filter(username=username).exists():
                self.stdout.write(f"⚠️ Already exists: {username}")
                skipped += 1
                continue

            # Create user
            user = User.objects.create_user(username=username, password=password)
            self.stdout.write(f"✅ Created user: {username} for property: {prop.name}")
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Done. Users created: {created_count}, Skipped: {skipped}"))
