# create_superuser.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_placement.settings")
django.setup()

from django.contrib.auth.models import User

# Change these values as needed
username = "admin"
email = "admin@example.com"
password = "Admin1234"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")
