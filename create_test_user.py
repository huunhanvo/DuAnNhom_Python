"""
Script tạo tài khoản khách hàng test
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import NguoiDung
import bcrypt

# Xóa user test cũ nếu có
NguoiDung.objects.filter(so_dien_thoai='0901234567').delete()

# Tạo user test mới
password = '123456'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

user = NguoiDung.objects.create(
    ho_ten='Nguyễn Văn Test',
    so_dien_thoai='0901234567',
    email='test@example.com',
    mat_khau_hash=hashed.decode('utf-8'),
    vai_tro='khach_hang',
    trang_thai=True,
    diem_tich_luy=0,
    da_xoa=False
)

print("✅ Đã tạo tài khoản test thành công!")
print("\n📋 Thông tin đăng nhập:")
print(f"   Số điện thoại: 0901234567")
print(f"   Mật khẩu: 123456")
print(f"\n🔗 Truy cập: http://127.0.0.1:8000/accounts/login/")
