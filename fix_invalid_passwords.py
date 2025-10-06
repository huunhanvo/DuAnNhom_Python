#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import NguoiDung
import bcrypt

# Find users with invalid password hashes
invalid_users = NguoiDung.objects.filter(
    mat_khau_hash__in=['hashed_password']
)

print(f"Found {invalid_users.count()} users with invalid password hashes")

# Update them with bcrypt hash for password '123456'
default_password = '123456'
hashed = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
hashed_str = hashed.decode('utf-8')

for user in invalid_users:
    print(f"Updating password for: {user.ho_ten} ({user.so_dien_thoai})")
    user.mat_khau_hash = hashed_str
    user.save()

print(f"\nAll invalid password hashes updated to default password: {default_password}")
print("Users can now login with this password.")