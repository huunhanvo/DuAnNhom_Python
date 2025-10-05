import psycopg2
import bcrypt

# Connect to database
conn = psycopg2.connect(
    dbname='quan_ly_barbershop',
    user='postgres',
    password='nhan123',
    host='localhost'
)

cur = conn.cursor()

# Get user info
cur.execute('''
    SELECT id, ho_ten, so_dien_thoai, mat_khau_hash, vai_tro 
    FROM nguoi_dung 
    WHERE so_dien_thoai = %s AND da_xoa = FALSE
''', ('0901111111',))

row = cur.fetchone()

if row:
    print(f"ID: {row[0]}")
    print(f"Ho ten: {row[1]}")
    print(f"SDT: {row[2]}")
    print(f"Password (first 60 chars): {row[3][:60]}")
    print(f"Password length: {len(row[3])}")
    print(f"Vai tro: {row[4]}")
    print(f"Starts with $2: {row[3].startswith('$2')}")
    
    # Test bcrypt
    print("\n--- Testing bcrypt ---")
    test_password = '123456'
    try:
        result = bcrypt.checkpw(test_password.encode('utf-8'), row[3].encode('utf-8'))
        print(f"Password '123456' matches: {result}")
    except Exception as e:
        print(f"bcrypt error: {e}")
        print("Password is NOT bcrypt hash!")
else:
    print("User not found!")

# List all users
print("\n--- All users ---")
cur.execute("SELECT id, ho_ten, so_dien_thoai, vai_tro FROM nguoi_dung WHERE da_xoa = FALSE LIMIT 5")
for row in cur.fetchall():
    print(f"{row[0]}: {row[2]} - {row[1]} ({row[3]})")

cur.close()
conn.close()
