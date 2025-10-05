#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import NguoiDung
from django.contrib.auth.hashers import make_password

# Create or get admin user
admin_user, created = NguoiDung.objects.get_or_create(
    so_dien_thoai='0999999999',
    defaults={
        'ho_ten': 'Administrator',
        'email': 'admin@test.com',
        'mat_khau_hash': make_password('admin123'),
        'vai_tro': 'quan_ly',
        'trang_thai': True
    }
)

if created:
    print(f'Created admin user: {admin_user.ho_ten}')
else:
    print(f'Admin user exists: {admin_user.ho_ten} - Role: {admin_user.vai_tro}')

print(f'User ID: {admin_user.id}')