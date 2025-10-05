#!/usr/bin/env python
import os
import django

# Setup Django FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from barbershop.views import admin_reports
from barbershop.models import NguoiDung

print("=== TEST DIRECT VIEW CALL ===")

try:
    # Tạo request factory
    factory = RequestFactory()
    request = factory.get('/admin/reports/')
    
    # Tạo user admin giả
    admin_user = NguoiDung(
        id=999,
        ho_ten='Test Admin',
        so_dien_thoai='0901234567',
        mat_khau_hash='dummy_hash',
        vai_tro='quan_ly',
        da_xoa=False
    )
    
    # Mock is_authenticated attribute và session
    admin_user.is_authenticated = True
    request.user = admin_user
    
    # Tạo session giả
    from django.contrib.sessions.backends.db import SessionStore
    request.session = SessionStore()
    request.session['user_id'] = 999
    request.session['vai_tro'] = 'quan_ly'  # Cần thiết cho decorator require_role
    request.session['ho_ten'] = 'Test Admin'
    
    print("Gọi admin_reports view...")
    response = admin_reports(request)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ View hoạt động bình thường")
        # Kiểm tra context data
        content = response.content.decode('utf-8')
        
        if "4750000" in content:  # Tổng doanh thu
            print("✅ Dữ liệu doanh thu có trong response")
        else:
            print("❌ Không thấy dữ liệu doanh thu")
            
        if "Chart.js" in content:
            print("✅ Chart.js được load")
        else:
            print("❌ Chart.js không được load")
            
        # Tìm các debug message
        if "DEBUG Reports - Full context created successfully" in content:
            print("✅ Context được tạo thành công")
        else:
            print("⚠️ Không thấy debug message - có thể đã được xử lý")
            
    else:
        print(f"❌ Lỗi: {response.status_code}")
        print(response.content.decode('utf-8')[:1000])
        
except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()