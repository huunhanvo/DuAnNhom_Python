#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import Voucher
from datetime import date

def test_create_voucher_direct():
    """Test creating voucher directly via model"""
    print("Testing direct voucher creation...")
    
    try:
        # Test data
        voucher_data = {
            'ma_voucher': 'DIRECT2025',
            'ten_voucher': 'Direct Test Voucher',
            'mo_ta': 'Test voucher created directly',
            'loai_giam': 'phan_tram',
            'gia_tri_giam': 15.0,
            'gia_tri_don_toi_thieu': 50000.0,
            'giam_toi_da': 100000.0,
            'ngay_bat_dau': date(2025, 1, 1),
            'ngay_ket_thuc': date(2025, 6, 30),
            'so_luong_tong': 50,
            'trang_thai': True,
        }
        
        print(f"Creating voucher with data: {voucher_data}")
        
        # Check if voucher already exists
        if Voucher.objects.filter(ma_voucher='DIRECT2025', da_xoa=False).exists():
            print("Voucher DIRECT2025 already exists, updating...")
            voucher = Voucher.objects.get(ma_voucher='DIRECT2025', da_xoa=False)
            for key, value in voucher_data.items():
                setattr(voucher, key, value)
            voucher.save()
            print(f"Updated voucher {voucher.id}")
        else:
            # Create new voucher
            voucher = Voucher.objects.create(**voucher_data)
            print(f"Created new voucher {voucher.id}: {voucher.ma_voucher}")
        
        # Verify creation
        created_voucher = Voucher.objects.get(id=voucher.id)
        print(f"Verification - Voucher: {created_voucher.ma_voucher} - {created_voucher.ten_voucher}")
        print(f"Status: {created_voucher.trang_thai}, Value: {created_voucher.gia_tri_giam}")
        
    except Exception as e:
        print(f"Error creating voucher: {e}")
        import traceback
        traceback.print_exc()

def list_current_vouchers():
    """List all current vouchers"""
    print("\nCurrent vouchers in database:")
    vouchers = Voucher.objects.filter(da_xoa=False).order_by('-id')
    for voucher in vouchers:
        print(f"  {voucher.id}: {voucher.ma_voucher} - {voucher.ten_voucher} - Active: {voucher.trang_thai}")

if __name__ == "__main__":
    list_current_vouchers()
    test_create_voucher_direct()
    list_current_vouchers()