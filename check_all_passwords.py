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

print("Checking all users for password hash validity...")
users = NguoiDung.objects.filter(da_xoa=False)

for user in users:
    print(f"\nUser: {user.ho_ten} ({user.so_dien_thoai})")
    print(f"Hash: {user.mat_khau_hash}")
    print(f"Length: {len(user.mat_khau_hash)}")
    print(f"Starts with $2b$: {user.mat_khau_hash.startswith('$2b$')}")
    
    # Try to use the hash with bcrypt
    try:
        # Test with a dummy password to see if hash is valid
        test_result = bcrypt.checkpw('test'.encode('utf-8'), user.mat_khau_hash.encode('utf-8'))
        print(f"Hash is valid: ✓")
    except ValueError as e:
        print(f"Hash is INVALID: {e}")
    except Exception as e:
        print(f"Other error: {e}")