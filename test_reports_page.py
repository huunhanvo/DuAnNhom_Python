#!/usr/bin/env python
import requests
import json

print("=== TEST TRANG BÁO CÁO ===")

# Test trang báo cáo
try:
    response = requests.get('http://127.0.0.1:8000/admin/reports/')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Trang báo cáo hoạt động bình thường")
        # Kiểm tra nội dung response có chứa dữ liệu không
        content = response.text
        if "4750000" in content:  # Tổng doanh thu
            print("✅ Dữ liệu doanh thu có mặt trong response")
        else:
            print("❌ Không tìm thấy dữ liệu doanh thu")
            
        if "chart" in content.lower():
            print("✅ Code chart có mặt trong response")
        else:
            print("❌ Không tìm thấy code chart")
            
    else:
        print(f"❌ Lỗi: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")

# Test với bộ lọc ngày
try:
    print("\n=== TEST BỘ LỌC NGÀY ===")
    params = {
        'from_date': '2025-09-01',
        'to_date': '2025-09-30'
    }
    response = requests.get('http://127.0.0.1:8000/admin/reports/', params=params)
    print(f"Status với bộ lọc: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Bộ lọc ngày hoạt động")
    else:
        print(f"❌ Lỗi bộ lọc: {response.status_code}")
        
except Exception as e:
    print(f"❌ Lỗi test bộ lọc: {e}")