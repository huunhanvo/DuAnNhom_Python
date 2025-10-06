import os

files = ['barbershop/views.py', 'barbershop/urls.py', 'barbershop/settings.py']

for f in files:
    try:
        with open(f, 'rb') as file:
            content = file.read()
            if b'\x00' in content:
                print(f'{f}: NULL BYTES FOUND')
            else:
                print(f'{f}: CLEAN')
    except Exception as e:
        print(f'{f}: ERROR - {e}')