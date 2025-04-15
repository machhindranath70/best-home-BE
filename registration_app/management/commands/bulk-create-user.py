# create_users_from_properties.py
import random
import string
from django.contrib.auth.models import User
from registration_app.models import PropertyInfo

def generate_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run():
    for prop in PropertyInfo.objects.all():
        contact = prop.contact.strip()
        if not contact:
            continue  # Skip if no contact

        if not User.objects.filter(username=contact).exists():
            password = generate_password()
            user = User.objects.create_user(username=contact, password=password)
            print(f"Created user: {contact} | password: {password}")
        else:
            print(f"User already exists: {contact}")
