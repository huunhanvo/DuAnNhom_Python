#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import NguoiDung
from django.contrib.auth.hashers import check_password

# Test the administrator account
admin_user = NguoiDung.objects.filter(so_dien_thoai='0999999999').first()
if admin_user:
    print(f"Admin user: {admin_user.ho_ten}")
    print(f"Password hash: {admin_user.mat_khau_hash}")
    
    # Test with admin123 password
    test_passwords = ['admin123', 'admin', '123456', 'password']
    for pwd in test_passwords:
        if admin_user.mat_khau_hash.startswith('pbkdf2_sha256$'):
            result = check_password(pwd, admin_user.mat_khau_hash)
            if result:
                print(f"✓ Password found: {pwd}")
                break
    else:
        print("No matching password found from test list")
else:
    print("Admin user not found")