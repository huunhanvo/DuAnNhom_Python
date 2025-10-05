import re

with open('barbershop/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Đọc từng dòng để xử lý cẩn thận
lines = content.split('\n')
new_lines = []

for i, line in enumerate(lines):
    # Giữ nguyên nếu là LichLamViec (schedule)
    if 'schedule.gio_bat_dau' in line or 'schedule.gio_ket_thuc' in line:
        new_lines.append(line)
    # Sửa DatLich: order_by với gio_bat_dau -> gio_hen
    elif "order_by('gio_bat_dau')" in line or 'order_by("-gio_bat_dau")' in line or "order_by('-gio_bat_dau')" in line:
        line = line.replace("'gio_bat_dau'", "'gio_hen'").replace("'-gio_bat_dau'", "'-gio_hen'").replace('"-gio_bat_dau"', '"-gio_hen"')
        new_lines.append(line)
    # Sửa DatLich.objects.create với gio_bat_dau/gio_ket_thuc
    elif 'gio_bat_dau=request.POST.get' in line:
        # Thay thế bằng gio_hen
        line = line.replace("gio_bat_dau=request.POST.get('gio_bat_dau')", "gio_hen=request.POST.get('gio_hen')")
        new_lines.append(line)
    elif 'gio_ket_thuc=request.POST.get' in line:
        # Xóa dòng này vì DatLich không có gio_ket_thuc
        continue
    else:
        new_lines.append(line)

content = '\n'.join(new_lines)

with open('barbershop/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed DatLich field names:")
print("  - order_by('gio_bat_dau') -> order_by('gio_hen')")
print("  - gio_bat_dau=request.POST.get(...) -> gio_hen=request.POST.get(...)")
print("  - Removed gio_ket_thuc lines")
print("  - Kept LichLamViec schedule fields intact")
