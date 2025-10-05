import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import *

print("✅ Kết nối thành công!")
print(f"Người dùng: {NguoiDung.objects.count()}")
print(f"Dịch vụ: {DichVu.objects.count()}")
print(f"Đặt lịch: {DatLich.objects.count()}")
print(f"Hóa đơn: {HoaDon.objects.count()}")