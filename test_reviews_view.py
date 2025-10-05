#!/usr/bin/env python
import os
import django
from django.test import RequestFactory

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.views import admin_reviews
from barbershop.models import NguoiDung
from django.contrib.sessions.backends.db import SessionStore

print("=== TEST ADMIN_REVIEWS VIEW ===")

try:
    # Tạo request
    factory = RequestFactory()
    request = factory.get('/admin/reviews/')
    
    # Tạo user admin và session
    admin_user = NguoiDung(
        id=999,
        ho_ten='Test Admin',
        so_dien_thoai='0901234567',
        mat_khau_hash='dummy_hash',
        vai_tro='quan_ly',
        da_xoa=False
    )
    admin_user.is_authenticated = True
    request.user = admin_user
    
    request.session = SessionStore()
    request.session['user_id'] = 999
    request.session['vai_tro'] = 'quan_ly'
    request.session['ho_ten'] = 'Test Admin'
    
    print("Gọi admin_reviews view...")
    response = admin_reviews(request)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ View hoạt động bình thường")
        
        # Kiểm tra context data có trong response
        content = response.content.decode('utf-8')
        
        # Kiểm tra các dữ liệu quan trọng
        if "30" in content:
            print("✅ Số lượng đánh giá hiển thị trong HTML")
        else:
            print("❌ Không thấy số lượng đánh giá")
            
        # Tìm trend data trong JavaScript
        import re
        trend_match = re.search(r'labels:\s*(\[[^\]]+\])', content)
        if trend_match:
            print(f"✅ Trend labels tìm thấy: {trend_match.group(1)}")
        else:
            print("❌ Trend labels không có")
            
        # Tìm trend data
        data_match = re.search(r'data:\s*(\[[^\]]+\])', content)
        if data_match:
            print(f"✅ Trend data tìm thấy: {data_match.group(1)}")
        else:
            print("❌ Trend data không có")
            
        if "Chart.js" in content:
            print("✅ Chart.js được load")
        else:
            print("❌ Chart.js không được load")
            
        # Tìm kiếm data attributes
        if 'data-rating=' in content:
            print("✅ Review cards có data attributes")
        else:
            print("❌ Review cards thiếu data attributes")
            
        # Tìm JavaScript console.log debug
        if "console.log('Trend Labels'" in content:
            print("✅ Debug log có trong JS")
        else:
            print("❌ Debug log không có")
            
        print("\n=== JAVASCRIPT SECTION ===")
        js_start = content.find('<script>')
        if js_start > 0:
            js_section = content[js_start:js_start+2000]
            print(js_section)
            
    else:
        print(f"❌ Lỗi: {response.status_code}")
        
except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()