import re

with open('barbershop/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace field names
content = content.replace('ngay_lam_viec', 'ngay_lam')
content = content.replace('ca_lam_viec', 'ca_lam')

with open('barbershop/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed LichLamViec field names:")
print("  - ngay_lam_viec → ngay_lam")
print("  - ca_lam_viec → ca_lam")
