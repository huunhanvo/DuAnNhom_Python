"""
Test script để tạo dữ liệu mẫu cho booking system
"""
import os
import sys
import django
from datetime import datetime, date, time, timedelta
import random

# Setup Django environment
sys.path.append(r'd:\Project\WebsiteHotTocNam')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import *

def create_sample_bookings():
    """Tạo dữ liệu mẫu bookings"""
    
    # Lấy hoặc tạo khách hàng mẫu
    customer, created = NguoiDung.objects.get_or_create(
        so_dien_thoai='0912345678',
        defaults={
            'ho_ten': 'Nguyễn Văn A',
            'vai_tro': 'khach_hang',
            'email': 'customer1@test.com',
            'mat_khau_hash': 'hashed_password',
            'trang_thai': True
        }
    )
    
    customer2, created = NguoiDung.objects.get_or_create(
        so_dien_thoai='0987654321',
        defaults={
            'ho_ten': 'Trần Thị B',
            'vai_tro': 'khach_hang',
            'email': 'customer2@test.com',
            'mat_khau_hash': 'hashed_password',
            'trang_thai': True
        }
    )
    
    # Lấy hoặc tạo nhân viên mẫu
    staff, created = NguoiDung.objects.get_or_create(
        so_dien_thoai='0911111111',
        defaults={
            'ho_ten': 'Lê Văn Thợ',
            'vai_tro': 'nhan_vien',
            'email': 'staff1@test.com',
            'mat_khau_hash': 'hashed_password',
            'trang_thai': True
        }
    )
    
    # Tạo danh mục dịch vụ
    category, created = DanhMucDichVu.objects.get_or_create(
        ten_danh_muc='Cắt tóc',
        defaults={'mo_ta': 'Dịch vụ cắt tóc cơ bản'}
    )
    
    # Tạo dịch vụ mẫu
    service1, created = DichVu.objects.get_or_create(
        ten_dich_vu='Cắt tóc Basic',
        defaults={
            'danh_muc': category,
            'mo_ta_ngan': 'Cắt tóc cơ bản',
            'gia': 50000,
            'thoi_gian_thuc_hien': 30,
            'trang_thai': True
        }
    )
    
    service2, created = DichVu.objects.get_or_create(
        ten_dich_vu='Gội đầu massage',
        defaults={
            'danh_muc': category,
            'mo_ta_ngan': 'Gội đầu và massage thư giãn',
            'gia': 30000,
            'thoi_gian_thuc_hien': 20,
            'trang_thai': True
        }
    )
    
    # Tạo booking mẫu với các trạng thái khác nhau
    statuses = ['cho_xac_nhan', 'da_xac_nhan', 'da_checkin', 'hoan_thanh', 'da_huy']
    
    for i in range(10):
        # Tạo booking code duy nhất
        booking_code = f'BK{random.randint(100000, 999999)}'
        while DatLich.objects.filter(ma_dat_lich=booking_code).exists():
            booking_code = f'BK{random.randint(100000, 999999)}'
        
        # Random ngày trong 2 tuần tới
        booking_date = date.today() + timedelta(days=random.randint(-7, 14))
        booking_time = time(random.randint(8, 17), random.choice([0, 30]))
        
        customer_choice = random.choice([customer, customer2])
        status = random.choice(statuses)
        
        booking = DatLich.objects.create(
            ma_dat_lich=booking_code,
            khach_hang=customer_choice,
            ten_khach_hang=customer_choice.ho_ten,
            so_dien_thoai_khach=customer_choice.so_dien_thoai,
            email_khach=customer_choice.email,
            nhan_vien=staff,
            ngay_hen=booking_date,
            gio_hen=booking_time,
            tong_tien=80000,
            thanh_tien=80000,
            trang_thai=status,
            ghi_chu=f'Booking mẫu số {i+1}',
            da_xoa=False
        )
        
        # Thêm dịch vụ vào booking
        DichVuDatLich.objects.create(
            dat_lich=booking,
            dich_vu=service1,
            ten_dich_vu=service1.ten_dich_vu,
            gia=service1.gia,
            so_luong=1,
            thanh_tien=service1.gia
        )
        
        DichVuDatLich.objects.create(
            dat_lich=booking,
            dich_vu=service2,
            ten_dich_vu=service2.ten_dich_vu,
            gia=service2.gia,
            so_luong=1,
            thanh_tien=service2.gia
        )
        
        print(f'Tạo booking {booking_code} - {status} - {booking_date} {booking_time}')
    
    print(f'Đã tạo {DatLich.objects.count()} booking(s) trong database!')

if __name__ == '__main__':
    create_sample_bookings()