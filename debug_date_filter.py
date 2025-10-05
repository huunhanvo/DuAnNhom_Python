"""
Debug script để kiểm tra date filter
"""
import os
import sys
import django

# Setup Django
sys.path.append(r'd:\Project\WebsiteHotTocNam')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import DatLich
from datetime import date, timedelta

def debug_date_filter():
    """Debug date filtering issues"""
    print("=== DEBUG DATE FILTER ===")
    
    # Get all bookings
    all_bookings = DatLich.objects.filter(da_xoa=False).order_by('ngay_hen')
    print(f"Total bookings: {all_bookings.count()}")
    
    if all_bookings.exists():
        print(f"Date range: {all_bookings.first().ngay_hen} to {all_bookings.last().ngay_hen}")
        
        # Show sample dates
        print("\nSample booking dates:")
        for booking in all_bookings[:10]:
            print(f"  {booking.ma_dat_lich}: {booking.ngay_hen} ({booking.trang_thai})")
    
    # Test specific date ranges
    today = date.today()
    print(f"\nToday: {today}")
    
    # Test filter for today
    today_bookings = DatLich.objects.filter(
        da_xoa=False, 
        ngay_hen=today
    )
    print(f"Bookings for today ({today}): {today_bookings.count()}")
    
    # Test filter for this week
    week_start = today - timedelta(days=7)
    week_end = today + timedelta(days=7)
    
    week_bookings = DatLich.objects.filter(
        da_xoa=False,
        ngay_hen__gte=week_start,
        ngay_hen__lte=week_end
    )
    print(f"Bookings for ±7 days ({week_start} to {week_end}): {week_bookings.count()}")
    
    # Test filter for this month
    month_start = today.replace(day=1)
    next_month = month_start.replace(month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1)
    month_end = next_month - timedelta(days=1)
    
    month_bookings = DatLich.objects.filter(
        da_xoa=False,
        ngay_hen__gte=month_start,
        ngay_hen__lte=month_end
    )
    print(f"Bookings for this month ({month_start} to {month_end}): {month_bookings.count()}")
    
    # Test some random date ranges
    test_dates = [
        ('2025-09-01', '2025-09-30'),
        ('2025-10-01', '2025-10-31'),
        ('2025-10-01', '2025-10-10'),
    ]
    
    print("\nTesting specific date ranges:")
    for start_str, end_str in test_dates:
        test_bookings = DatLich.objects.filter(
            da_xoa=False,
            ngay_hen__gte=start_str,
            ngay_hen__lte=end_str
        )
        print(f"  {start_str} to {end_str}: {test_bookings.count()} bookings")

if __name__ == '__main__':
    debug_date_filter()