#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import NguoiDung
from django.test import Client

# Create test client and login
client = Client()

# Test login with working credentials
response = client.post('/login/', {
    'username': '0902222222',
    'password': '123456'
})

print(f'Login response status: {response.status_code}')
print(f'Redirect location: {response.get("Location", "No redirect")}')

# If login successful, test profile page
if response.status_code == 302:
    profile_response = client.get('/staff/profile/')
    print(f'Profile page status: {profile_response.status_code}')
    
    if profile_response.status_code == 200:
        print('Profile page loaded successfully!')
        # Check if context contains expected data
        context = profile_response.context
        if context:
            print(f'Context keys: {list(context.keys())}')
            if 'staff_stats' in context:
                print(f'Staff stats: {context["staff_stats"]}')
            if 'staff_data' in context:
                print(f'Staff data keys: {list(context["staff_data"].keys())}')
        else:
            print('No context data available')
    else:
        print(f'Profile page failed with status: {profile_response.status_code}')
        print(f'Response content: {profile_response.content.decode()[:500]}...')
else:
    print('Login failed')
    print(f'Response content: {response.content.decode()[:500]}...')