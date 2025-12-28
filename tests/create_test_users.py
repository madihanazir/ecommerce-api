# create_test_users.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from apps.users.models import User

# Delete if exists
User.objects.filter(email__in=['admin@test.com', 'customer@test.com']).delete()

# Create admin
admin = User.objects.create_user(
    username='admin',
    email='admin@test.com',
    password='admin123',
    role='admin',
    is_active=True
)
print(f"✅ Admin created: {admin.email}")

# Create customer  
customer = User.objects.create_user(
    username='customer',
    email='customer@test.com',
    password='customer123',
    role='customer',
    is_active=True
)
print(f"✅ Customer created: {customer.email}")