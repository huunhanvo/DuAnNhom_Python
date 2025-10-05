#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import HoaDon, DatLich
from django.db.models import Sum, Count, Avg

print("=== KIỂM TRA DỮ LIỆU DATABASE ===")

# Kiểm tra hoá đơn gần nhất
recent = HoaDon.objects.filter(da_xoa=False).order_by('-ngay_thanh_toan')[:5]
print('\n5 hoá đơn gần nhất:')
for h in recent:
    print(f'  ID: {h.id}, Thành tiền: {h.thanh_tien}, Ngày: {h.ngay_thanh_toan}')

# Kiểm tra tổng doanh thu
total = HoaDon.objects.filter(da_xoa=False).aggregate(total=Sum('thanh_tien'))['total']
print(f'\nTổng doanh thu: {total}')

# Kiểm tra phương thức thanh toán
payment_methods = HoaDon.objects.filter(da_xoa=False).values('phuong_thuc_thanh_toan').annotate(count=Count('id'))
print('\nPhương thức thanh toán:')
for pm in payment_methods:
    print(f'  {pm["phuong_thuc_thanh_toan"]}: {pm["count"]} hoá đơn')

print("\n=== KẾT QUẢ THỐNG KÊ ===")
print(f"Tổng số hoá đơn: {HoaDon.objects.filter(da_xoa=False).count()}")
print(f"Tổng số đặt lịch: {DatLich.objects.filter(da_xoa=False).count()}")