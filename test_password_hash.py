import bcrypt

# Test password hash từ database mới
hash_from_db = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq'
password = b'123456'

result = bcrypt.checkpw(password, hash_from_db)
print(f"Password '123456' matches hash: {result}")

if result:
    print("✅ Hash is correct!")
else:
    print("❌ Hash doesn't match - need to update passwords")
