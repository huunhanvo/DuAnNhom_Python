import os
import django
import bcrypt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import NguoiDung, ThongTinNhanVien

# Xóa user cũ (nếu có)
NguoiDung.objects.all().delete()

# Tạo Admin
admin = NguoiDung.objects.create(
    ho_ten='Admin System',
    so_dien_thoai='0901111111',
    email='admin@barbershop.vn',
    vai_tro='quan_ly',
    ngay_sinh='1985-03-15',
    gioi_tinh='nam',
    trang_thai=True,
    da_xoa=False
)
admin.mat_khau_hash = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
admin.save()
print(f'✅ Admin: {admin.ho_ten} - SĐT: {admin.so_dien_thoai}')

# Tạo Nhân viên
staff = NguoiDung.objects.create(
    ho_ten='Trần Minh Hoàng',
    so_dien_thoai='0902222222',
    email='hoang@barbershop.vn',
    vai_tro='nhan_vien',
    ngay_sinh='1992-07-20',
    gioi_tinh='nam',
    trang_thai=True,
    da_xoa=False
)
staff.mat_khau_hash = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
staff.save()

ThongTinNhanVien.objects.create(
    nguoi_dung=staff,
    mo_ta='Stylist chuyên nghiệp',
    chuyen_mon='Cắt tóc nam Hàn Quốc',
    kinh_nghiem_nam=10
)
print(f'✅ Nhân viên: {staff.ho_ten} - SĐT: {staff.so_dien_thoai}')

print('\n🎉 HOÀN THÀNH!')
print('=' * 60)
print('THÔNG TIN ĐĂNG NHẬP:')
print('Admin - SĐT: 0901111111, Mật khẩu: 123456')
print('Staff - SĐT: 0902222222, Mật khẩu: 123456')
print('=' * 60)