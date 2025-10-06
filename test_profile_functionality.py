#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
import json

def test_profile_functionality():
    print("🧪 Testing Staff Profile Functionality\n")
    
    # Create test client and login
    client = Client()
    
    # Test login
    print("1. Testing Login...")
    response = client.post('/login/', {
        'username': '0902222222',
        'password': '123456'
    })
    print(f"   Login status: {response.status_code}")
    
    if response.status_code != 302:
        print("   ❌ Login failed!")
        return
    print("   ✅ Login successful")
    
    # Test profile page access
    print("\n2. Testing Profile Page Access...")
    response = client.get('/staff/profile/')
    print(f"   Profile page status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Profile page accessible")
    else:
        print("   ❌ Profile page failed")
        return
    
    # Test update profile API
    print("\n3. Testing Update Profile API...")
    response = client.post('/api/staff/update-profile/', {
        'ho_ten': 'Trần Minh Hoàng (Updated)',
        'email': 'updated@barbershop.vn',
        'dia_chi': '123 Test Street',
        'gioi_thieu': 'Đây là phần giới thiệu test'
    })
    print(f"   Update profile status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("   ✅ Profile update successful")
        else:
            print(f"   ❌ Profile update failed: {data.get('message')}")
    else:
        print(f"   ❌ Profile update failed with status {response.status_code}")
    
    # Test change password API
    print("\n4. Testing Change Password API...")
    response = client.post('/api/staff/change-password/', {
        'old_password': '123456',
        'new_password': '654321',
        'confirm_password': '654321'
    })
    print(f"   Change password status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("   ✅ Password change successful")
            
            # Test login with new password
            print("   Testing login with new password...")
            client_new = Client()
            new_login = client_new.post('/login/', {
                'username': '0902222222',
                'password': '654321'
            })
            if new_login.status_code == 302:
                print("   ✅ New password works")
                
                # Change back to original password
                new_login = client_new.post('/api/staff/change-password/', {
                    'old_password': '654321',
                    'new_password': '123456',
                    'confirm_password': '123456'
                })
                print("   Password reverted to original")
            else:
                print("   ❌ New password doesn't work")
        else:
            print(f"   ❌ Password change failed: {data.get('message')}")
    else:
        print(f"   ❌ Password change failed with status {response.status_code}")
    
    # Test avatar upload API
    print("\n5. Testing Avatar Upload API...")
    # Create a dummy image file
    image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
    uploaded_file = SimpleUploadedFile(
        "test_avatar.png", 
        image_content, 
        content_type="image/png"
    )
    
    response = client.post('/api/staff/upload-avatar/', {
        'avatar': uploaded_file
    })
    print(f"   Avatar upload status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("   ✅ Avatar upload successful")
            print(f"   Avatar URL: {data.get('avatar_url', 'N/A')}")
        else:
            print(f"   ❌ Avatar upload failed: {data.get('message')}")
    else:
        print(f"   ❌ Avatar upload failed with status {response.status_code}")
    
    # Test notifications API
    print("\n6. Testing Notifications API...")
    response = client.post('/api/staff/update-notifications/', {
        'emailBooking': 'on',
        'emailReminder': 'on',
        'pushBooking': 'on'
    })
    print(f"   Notifications update status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("   ✅ Notifications update successful")
        else:
            print(f"   ❌ Notifications update failed: {data.get('message')}")
    else:
        print(f"   ❌ Notifications update failed with status {response.status_code}")
    
    print("\n🎉 Profile functionality testing completed!")

if __name__ == "__main__":
    test_profile_functionality()