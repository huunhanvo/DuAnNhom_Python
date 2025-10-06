import os

# Clean null bytes from views.py
with open('barbershop/views.py', 'rb') as f:
    content = f.read()

# Remove null bytes
clean_content = content.replace(b'\x00', b'')

# Write back clean content
with open('barbershop/views.py', 'wb') as f:
    f.write(clean_content)

print("Cleaned null bytes from views.py")

# Verify
with open('barbershop/views.py', 'rb') as f:
    test_content = f.read()
    if b'\x00' in test_content:
        print("ERROR: Still has null bytes")
    else:
        print("SUCCESS: No null bytes found")