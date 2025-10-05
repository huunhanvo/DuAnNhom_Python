#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import DanhGia, DichVu, NguoiDung

print('=== THỐNG KÊ ĐÁNH GIÁ ===')
print(f'Tổng số đánh giá: {DanhGia.objects.count()}')
print(f'Đánh giá chưa xóa: {DanhGia.objects.filter(da_xoa=False).count()}')
print(f'Đánh giá có phản hồi: {DanhGia.objects.filter(phan_hoi__isnull=False).count()}')
print('')

if DanhGia.objects.exists():
    print('5 đánh giá gần nhất:')
    for dg in DanhGia.objects.order_by('-ngay_tao')[:5]:
        print(f'  ID: {dg.id}, Sao: {dg.so_sao}, KH: {dg.khach_hang.ho_ten if dg.khach_hang else "N/A"}, Nội dung: {dg.noi_dung[:50]}...')
else:
    print('❌ Không có đánh giá nào trong database')
    print('Cần tạo dữ liệu mẫu...')
    
    # Kiểm tra dữ liệu cần thiết
    customers = NguoiDung.objects.filter(vai_tro='khach_hang', da_xoa=False)
    staff = NguoiDung.objects.filter(vai_tro='nhan_vien', da_xoa=False)  
    services = DichVu.objects.filter(da_xoa=False)
    
    print(f'Khách hàng có sẵn: {customers.count()}')
    print(f'Nhân viên có sẵn: {staff.count()}')
    print(f'Dịch vụ có sẵn: {services.count()}')