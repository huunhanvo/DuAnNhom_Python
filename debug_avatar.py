#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import NguoiDung
from django.conf import settings

def debug_avatar_issue():
    print("🔍 Debugging Avatar Display Issue\n")
    
    # Check user with avatar
    user = NguoiDung.objects.filter(so_dien_thoai='0902222222').first()
    if user:
        print(f"✅ User found: {user.ho_ten}")
        print(f"📱 Phone: {user.so_dien_thoai}")
        print(f"🖼️  Avatar field: {user.anh_dai_dien}")
        
        if user.anh_dai_dien:
            avatar_path = os.path.join(settings.MEDIA_ROOT, str(user.anh_dai_dien))
            print(f"📁 Full path: {avatar_path}")
            print(f"📂 File exists: {os.path.exists(avatar_path)}")
            
            if os.path.exists(avatar_path):
                file_size = os.path.getsize(avatar_path)
                print(f"📊 File size: {file_size} bytes")
            
            # Expected URL
            expected_url = f"{settings.MEDIA_URL}{user.anh_dai_dien}"
            print(f"🌐 Expected URL: {expected_url}")
        else:
            print("❌ No avatar set in database")
    else:
        print("❌ User not found")
    
    # Check media settings
    print(f"\n⚙️ Media Settings:")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    # Check media directory
    avatars_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    print(f"\n📂 Avatars Directory: {avatars_dir}")
    print(f"Directory exists: {os.path.exists(avatars_dir)}")
    
    if os.path.exists(avatars_dir):
        avatar_files = os.listdir(avatars_dir)
        print(f"Files in avatars directory: {len(avatar_files)}")
        for f in avatar_files[:5]:  # Show first 5 files
            print(f"  - {f}")
        if len(avatar_files) > 5:
            print(f"  ... and {len(avatar_files) - 5} more files")

if __name__ == "__main__":
    debug_avatar_issue()