"""
Script để xóa tất cả session (đăng xuất tất cả users)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from django.contrib.sessions.models import Session

# Xóa tất cả session
count = Session.objects.all().count()
Session.objects.all().delete()
print(f"✅ Đã xóa {count} session(s)")
print("Bây giờ hãy refresh trình duyệt (Ctrl+Shift+R)")
