#!/usr/bin/env python
"""
Fix invalid trang_thai values in DichVu table
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db import connection
from barbershop.models import DichVu

def fix_service_status():
    """Fix invalid trang_thai values in DichVu table"""
    print("Checking and fixing DichVu trang_thai field...")
    
    # Use raw SQL to check and fix invalid values
    with connection.cursor() as cursor:
        # First, let's see what values we have
        cursor.execute("SELECT DISTINCT trang_thai FROM dich_vu")
        all_values = cursor.fetchall()
        print("Current trang_thai values in database:")
        for row in all_values:
            print(f"  '{row[0]}'")
        
        # Fix text values that should be boolean True
        cursor.execute("UPDATE dich_vu SET trang_thai = TRUE WHERE trang_thai::text = 'hoat_dong'")
        affected1 = cursor.rowcount
        print(f"Fixed {affected1} 'hoat_dong' values to TRUE")
        
        cursor.execute("UPDATE dich_vu SET trang_thai = TRUE WHERE trang_thai::text = 'active'")
        affected2 = cursor.rowcount
        print(f"Fixed {affected2} 'active' values to TRUE")
        
        # Fix text values that should be boolean False  
        cursor.execute("UPDATE dich_vu SET trang_thai = FALSE WHERE trang_thai::text = 'khong_hoat_dong'")
        affected3 = cursor.rowcount
        print(f"Fixed {affected3} 'khong_hoat_dong' values to FALSE")
        
        cursor.execute("UPDATE dich_vu SET trang_thai = FALSE WHERE trang_thai::text = 'inactive'")
        affected4 = cursor.rowcount
        print(f"Fixed {affected4} 'inactive' values to FALSE")
        
        print("Standardized boolean values.")
        
        # Show final state
        cursor.execute("SELECT trang_thai, COUNT(*) FROM dich_vu GROUP BY trang_thai")
        final_state = cursor.fetchall()
        print("Final trang_thai distribution:")
        for row in final_state:
            print(f"  '{row[0]}': {row[1]} records")

if __name__ == '__main__':
    fix_service_status()
    print("Done!")