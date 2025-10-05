#!/usr/bin/env python
"""
Script to check database table structure
"""
import os
import sys
import django
from django.db import connection

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

def check_table_structure():
    with connection.cursor() as cursor:
        # Kiểm tra cấu trúc bảng danh_gia
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'danh_gia'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print("Cấu trúc bảng danh_gia hiện tại:")
        print("-" * 50)
        for col in columns:
            print(f"{col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'}) {col[3] if col[3] else ''}")
        
        print(f"\nTổng số cột: {len(columns)}")

if __name__ == '__main__':
    check_table_structure()