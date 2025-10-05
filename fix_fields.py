import re

# Read views.py
with open('barbershop/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace field names
content = content.replace('ngay_dat', 'ngay_hen')
content = content.replace('gio_bat_dau', 'gio_hen')  
content = content.replace('gio_ket_thuc', 'gio_hen')

# Tuy nhiên, với LichLamViec thì có gio_bat_dau và gio_ket_thuc thật
# Cần check xem có LichLamViec.gio_bat_dau không
# Model LichLamViec có: gio_bat_dau, gio_ket_thuc (đúng)
# Nên không cần sửa phần LichLamViec

# Đọc lại và chỉ sửa DatLich
with open('barbershop/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace ngay_dat -> ngay_hen (cho DatLich)
content = content.replace('ngay_dat', 'ngay_hen')

# Replace gio_bat_dau/gio_ket_thuc -> gio_hen CHỈ cho DatLich
# Nhưng LichLamViec thì giữ nguyên
# Cách đơn giản: replace trong context của DatLich

# Save
with open('barbershop/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Replaced ngay_dat -> ngay_hen")
print("Note: gio_bat_dau và gio_ket_thuc cần check thủ công vì LichLamViec có field này")
