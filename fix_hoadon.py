import re

with open('barbershop/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Xóa trang_thai='da_thanh_toan' khỏi HoaDon filter
# Pattern 1: Trong filter()
content = re.sub(r",\s*trang_thai='da_thanh_toan'", '', content)
content = re.sub(r"trang_thai='da_thanh_toan',\s*", '', content)

# Pattern 2: Trong Q() objects
content = re.sub(r",\s*hoadon_set__trang_thai='da_thanh_toan'", '', content)
content = re.sub(r"hoadon_set__trang_thai='da_thanh_toan',\s*", '', content)

# Pattern 3: Dòng độc lập
lines = content.split('\n')
new_lines = []
for line in lines:
    if line.strip() == "trang_thai='da_thanh_toan'":
        continue
    new_lines.append(line)

content = '\n'.join(new_lines)

with open('barbershop/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Removed trang_thai='da_thanh_toan' from HoaDon queries")
print("   (HoaDon model doesn't have trang_thai field)")
