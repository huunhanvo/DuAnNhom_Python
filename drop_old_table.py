#!/usr/bin/env python
"""
Script to drop and recreate danh_gia table
"""
import os
import sys
import django
from django.db import connection

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

def drop_table():
    with connection.cursor() as cursor:
        # Drop table if exists
        cursor.execute("DROP TABLE IF EXISTS danh_gia CASCADE;")
        print("Đã xóa bảng danh_gia cũ")

if __name__ == '__main__':
    drop_table()