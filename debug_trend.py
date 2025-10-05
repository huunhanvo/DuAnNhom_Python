#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import DanhGia, DichVu, NguoiDung
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

print("=== DEBUG TREND DATA ===")

# Simulate same logic as admin_reviews view
trend_labels = []
trend_data = []
trend_counts = []

for i in range(6, -1, -1):
    date = timezone.now().date() - timedelta(days=i)
    trend_labels.append(date.strftime('%d/%m'))
    
    daily_reviews = DanhGia.objects.filter(
        da_xoa=False,
        ngay_tao__date=date
    )
    
    daily_avg = daily_reviews.aggregate(avg=Avg('so_sao'))['avg'] or 0
    daily_count = daily_reviews.count()
    
    trend_data.append(round(daily_avg, 1))
    trend_counts.append(daily_count)
    
    print(f"Ngày {date.strftime('%d/%m')}: {daily_count} đánh giá, TB: {daily_avg:.1f}")

print(f"\nTrend Labels: {trend_labels}")
print(f"Trend Data: {trend_data}")
print(f"Trend Counts: {trend_counts}")

print(f"\nJSON Labels: {json.dumps(trend_labels)}")
print(f"JSON Data: {json.dumps(trend_data)}")
print(f"JSON Counts: {json.dumps(trend_counts)}")

# Kiểm tra có đánh giá nào trong 7 ngày gần đây không
recent = DanhGia.objects.filter(
    da_xoa=False,
    ngay_tao__date__gte=timezone.now().date() - timedelta(days=7)
).count()
print(f"\nĐánh giá trong 7 ngày gần đây: {recent}")

if recent == 0:
    print("⚠️ Không có đánh giá nào trong 7 ngày gần đây - biểu đồ sẽ trống!")