# Hướng dẫn chạy giao diện

## Bước 1: Cài đặt Django

```bash
pip install django
```

## Bước 2: Chạy server

```bash
python manage.py runserver
```

## Bước 3: Mở trình duyệt

Truy cập các URL sau để xem giao diện:

### PHẦN ADMIN:
- Dashboard: http://127.0.0.1:8000/admin/dashboard/
- Quản lý nhân viên: http://127.0.0.1:8000/admin/staff/
- Quản lý đặt lịch: http://127.0.0.1:8000/admin/bookings/
- Quản lý hóa đơn: http://127.0.0.1:8000/admin/invoices/
- Quản lý khách hàng: http://127.0.0.1:8000/admin/customers/
- Quản lý dịch vụ: http://127.0.0.1:8000/admin/services/
- Lịch làm việc: http://127.0.0.1:8000/admin/work-schedule/
- Khuyến mãi: http://127.0.0.1:8000/admin/promotions/
- Báo cáo: http://127.0.0.1:8000/admin/reports/
- Đánh giá: http://127.0.0.1:8000/admin/reviews/
- Báo cáo POS: http://127.0.0.1:8000/admin/pos-report/
- Cài đặt: http://127.0.0.1:8000/admin/settings/

### PHẦN STAFF:
- Dashboard: http://127.0.0.1:8000/staff/dashboard/
- POS: http://127.0.0.1:8000/staff/pos/
- Lịch hẹn hôm nay: http://127.0.0.1:8000/staff/today-bookings/
- Lịch làm việc: http://127.0.0.1:8000/staff/schedule/
- Khách hàng của tôi: http://127.0.0.1:8000/staff/my-customers/
- Doanh thu: http://127.0.0.1:8000/staff/revenue/
- Hồ sơ cá nhân: http://127.0.0.1:8000/staff/profile/

## Lưu ý:
- Đã có dữ liệu mẫu để xem giao diện
- Các chức năng AJAX chưa hoạt động (cần backend API)
- Biểu đồ Chart.js sẽ hiển thị với dữ liệu mẫu
