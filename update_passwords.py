import bcrypt
import psycopg2

# Generate new bcrypt hash for password '123456'
password = '123456'
new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
new_hash_str = new_hash.decode('utf-8')

print(f"New bcrypt hash for '123456': {new_hash_str}")
print(f"Length: {len(new_hash_str)}")

# Update database
conn = psycopg2.connect(
    dbname='quan_ly_barbershop',
    user='postgres',
    password='nhan123',
    host='localhost'
)

cur = conn.cursor()

# Update all test accounts with password '123456'
test_accounts = ['0901111111', '0902222222', '0903333333', '0904444444', '0905555555', '0906666666']

for sdt in test_accounts:
    cur.execute('''
        UPDATE nguoi_dung 
        SET mat_khau_hash = %s 
        WHERE so_dien_thoai = %s
    ''', (new_hash_str, sdt))
    print(f"Updated password for {sdt}")

conn.commit()
cur.close()
conn.close()

print("\nAll test accounts now have password: 123456")
print("\nTest login with:")
print("- Manager: 0901111111 / 123456")
print("- Staff: 0902222222 / 123456")
