import os
import django
import bcrypt

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import NguoiDung

# Tài khoản cần fix
phone = '0990123456'
new_password = '123456'

try:
    # Tìm user
    user = NguoiDung.objects.get(so_dien_thoai=phone)
    
    print(f"✓ Tìm thấy user: {user.ho_ten} ({user.vai_tro})")
    print(f"  Số điện thoại: {user.so_dien_thoai}")
    print(f"  Hash cũ: {user.mat_khau_hash[:50]}...")
    
    # Tạo hash mới
    new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    user.mat_khau_hash = new_hash.decode('utf-8')
    user.save()
    
    print(f"\n✓ ĐÃ CẬP NHẬT MẬT KHẨU THÀNH CÔNG!")
    print(f"  Hash mới: {user.mat_khau_hash[:50]}...")
    print(f"\nThông tin đăng nhập:")
    print(f"  - Số điện thoại: {phone}")
    print(f"  - Mật khẩu: {new_password}")
    
    # Verify
    verify = bcrypt.checkpw(new_password.encode('utf-8'), user.mat_khau_hash.encode('utf-8'))
    print(f"\n✓ Xác minh mật khẩu: {'THÀNH CÔNG' if verify else 'THẤT BẠI'}")
    
except NguoiDung.DoesNotExist:
    print(f"✗ Không tìm thấy user với số điện thoại: {phone}")
except Exception as e:
    print(f"✗ Lỗi: {e}")
