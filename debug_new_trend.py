#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import DanhGia
from django.db.models import Avg
from django.utils import timezone
from datetime import datetime, timedelta
import json

print("=== DEBUG TREND DATA (NEW LOGIC) ===")

# Same logic as updated view
trend_labels = []
trend_data = []
trend_counts = []

# Get the date range with reviews (last 30 days or actual review dates)
thirty_days_ago = timezone.now().date() - timedelta(days=30)
reviews_in_period = DanhGia.objects.filter(
    da_xoa=False,
    ngay_tao__date__gte=thirty_days_ago
).dates('ngay_tao', 'day').order_by('ngay_tao')

print(f"Reviews trong 30 ngày: {len(reviews_in_period)}")
print(f"Các ngày có đánh giá: {list(reviews_in_period)}")

if reviews_in_period:
    # Use actual review dates for more meaningful chart
    review_dates = list(reviews_in_period)[-7:]  # Last 7 dates with reviews
    print(f"7 ngày gần nhất có đánh giá: {review_dates}")
    
    for date in review_dates:
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

print(f"\n✅ Biểu đồ có dữ liệu: {'Có' if any(trend_counts) else 'Không'}")