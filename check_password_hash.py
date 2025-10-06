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

user = NguoiDung.objects.filter(so_dien_thoai='0902222222').first()
if user:
    print(f'Password hash: {user.mat_khau_hash}')
    print(f'Hash length: {len(user.mat_khau_hash)}')
    print(f'Hash starts with $2b$: {user.mat_khau_hash.startswith("$2b$")}')
    
    # Try to check if it's a valid bcrypt hash
    try:
        # Test password verification with a known password
        test_result = bcrypt.checkpw('123456'.encode('utf-8'), user.mat_khau_hash.encode('utf-8'))
        print(f'Password check successful: {test_result}')
    except Exception as e:
        print(f'Password check failed: {e}')
        print(f'Error type: {type(e)}')
else:
    print('User not found')