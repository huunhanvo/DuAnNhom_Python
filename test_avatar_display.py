#!/usr/bin/env python3
"""
Test Avatar Display Functionality
Kiểm tra việc hiển thị avatar sau khi upload
"""

import os
import django
import requests
from django.test import Client
from django.contrib.auth import authenticate, login

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import NguoiDung

def test_avatar_display():
    print("🔍 Testing Avatar Display After Upload\n")
    
    # Test data
    phone = "0902222222"
    password = "123456"
    
    try:
        # 1. Test authentication
        print("1️⃣ Testing user authentication...")
        user = NguoiDung.objects.filter(sdt=phone).first()
        if not user:
            print("❌ User not found!")
            return
            
        print(f"✅ User found: {user.ho_ten}")
        print(f"📱 Phone: {user.sdt}")
        print(f"🖼️ Avatar field: {user.anh_dai_dien}")
        
        # 2. Test Django client login
        print("\n2️⃣ Testing Django client login...")
        client = Client()
        
        # Get login page first to get CSRF token
        login_response = client.get('/login/')
        print(f"Login page status: {login_response.status_code}")
        
        # Extract CSRF token
        csrf_token = None
        if 'csrfmiddlewaretoken' in login_response.content.decode():
            import re
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_response.content.decode())
            if csrf_match:
                csrf_token = csrf_match.group(1)
                print(f"✅ CSRF token extracted: {csrf_token[:20]}...")
        
        # Login via POST
        login_data = {
            'phone': phone,
            'password': password,
            'csrfmiddlewaretoken': csrf_token
        }
        
        post_response = client.post('/login/', login_data, follow=True)
        print(f"Login POST status: {post_response.status_code}")
        
        # 3. Test profile page
        print("\n3️⃣ Testing profile page...")
        profile_response = client.get('/staff/profile/')
        print(f"Profile page status: {profile_response.status_code}")
        
        if profile_response.status_code == 200:
            content = profile_response.content.decode()
            
            # Check if avatar URL is in the content
            expected_avatar_url = f"/media/{user.anh_dai_dien}"
            print(f"Expected avatar URL: {expected_avatar_url}")
            
            if expected_avatar_url in content:
                print("✅ Avatar URL found in profile page!")
            else:
                print("❌ Avatar URL NOT found in profile page!")
                
                # Check what avatar-related content exists
                if 'default-avatar.png' in content:
                    print("⚠️ Using default avatar instead")
                if '/media/' in content:
                    print("📁 Found other media URLs in content")
                    import re
                    media_urls = re.findall(r'/media/[^"\s]+', content)
                    for url in media_urls:
                        print(f"   - {url}")
            
            # Check for MEDIA_URL context
            if '{{ MEDIA_URL }}' in content:
                print("❌ MEDIA_URL template variable not processed!")
            else:
                print("✅ Template variables processed correctly")
                
        else:
            print(f"❌ Cannot access profile page: {profile_response.status_code}")
            
        # 4. Test direct media access
        print("\n4️⃣ Testing direct media file access...")
        if user.anh_dai_dien:
            media_url = f"http://127.0.0.1:8000/media/{user.anh_dai_dien}"
            try:
                media_response = requests.get(media_url, timeout=5)
                print(f"Direct media access status: {media_response.status_code}")
                if media_response.status_code == 200:
                    print("✅ Avatar file accessible via URL")
                else:
                    print("❌ Avatar file not accessible via URL")
            except requests.exceptions.RequestException as e:
                print(f"❌ Request failed: {e}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_avatar_display()