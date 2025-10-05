# HƯỚNG DẪN CÀI ĐẶT VÀ CẤU HÌNH

## 1. Cài đặt psycopg2 (PostgreSQL adapter)

```bash
pip install psycopg2-binary
```

## 2. Cấu hình PostgreSQL trong settings.py

Mở file `barbershop/settings.py` và tìm dòng:

```python
'PASSWORD': 'your_password',  # Thay bằng password PostgreSQL của bạn
```

Thay đổi thành mật khẩu PostgreSQL thực tế của bạn.

## 3. Chạy migrations

**LƯU Ý**: Django sẽ TỰ ĐỘNG quản lý database schema. Tuy nhiên vì bạn đã tạo sẵn database bằng script SQL, chúng ta cần làm như sau:

### Option 1: Sử dụng database hiện có (KHUYẾN NGHỊ)

```bash
# Tạo migrations từ models
python manage.py makemigrations barbershop

# KHÔNG chạy migrate, vì tables đã tồn tại
# Thay vào đó, fake migrate:
python manage.py migrate --fake-initial
```

### Option 2: Django tạo lại database (nếu muốn)

```bash
# Xóa tất cả tables trong database quan_ly_barbershop
# Sau đó chạy:
python manage.py makemigrations barbershop
python manage.py migrate
```

## 4. Test kết nối database

```bash
python manage.py dbshell
```

Nếu kết nối thành công, bạn sẽ thấy PostgreSQL prompt.

## 5. Chạy server

```bash
python manage.py runserver
```

## 6. Các thay đổi chính

### File đã sửa:
1. **barbershop/settings.py** - Đổi từ SQLite sang PostgreSQL
2. **barbershop/models.py** - Tạo mới với 12 models chính

### Cần làm tiếp:
- Cập nhật tất cả views để query từ database thay vì dữ liệu tĩnh
- Implement authentication system
- Implement CRUD operations

## 7. Troubleshooting

### Lỗi: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Lỗi: "FATAL: password authentication failed"
- Kiểm tra username/password trong settings.py
- Kiểm tra pg_hba.conf của PostgreSQL

### Lỗi: "database quan_ly_barbershop does not exist"
- Tạo database trong pgAdmin4 hoặc:
```sql
CREATE DATABASE quan_ly_barbershop;
```

### Lỗi: "table already exists"
- Sử dụng `--fake-initial` khi migrate:
```bash
python manage.py migrate --fake-initial
```
