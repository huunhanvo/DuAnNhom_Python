#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import DanhGia
from django.utils import timezone
from datetime import datetime, timedelta

print('=== NGÀY TẠO CÁC ĐÁNH GIÁ ===')
reviews = DanhGia.objects.filter(da_xoa=False).order_by('-ngay_tao')[:10]
for r in reviews:
    print(f'ID: {r.id}, Ngày: {r.ngay_tao.strftime("%d/%m/%Y %H:%M")}, Sao: {r.so_sao}')

print(f'\nHôm nay: {timezone.now().date()}')
print(f'7 ngày trước: {timezone.now().date() - timedelta(days=7)}')

# Kiểm tra xem có đánh giá nào trong khoảng ngày gần đây không
recent_dates = {}
for i in range(7):
    date = timezone.now().date() - timedelta(days=i)
    count = DanhGia.objects.filter(da_xoa=False, ngay_tao__date=date).count()
    recent_dates[date.strftime('%d/%m')] = count

print('\nĐánh giá theo ngày (7 ngày gần đây):')
for date, count in recent_dates.items():
    print(f'  {date}: {count} đánh giá')