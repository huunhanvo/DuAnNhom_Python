# HƯỚNG DẪN CẬP NHẬT VIEWS - LẤY DỮ LIỆU TỪ DATABASE

## BƯỚC 1: Cập nhật Password PostgreSQL

Mở file `barbershop/settings.py` và thay đổi dòng:

```python
'PASSWORD': 'your_password',
```

Thành password PostgreSQL thực tế của bạn (ví dụ: 'postgres' hoặc password bạn đã đặt)

## BƯỚC 2: Tạo Migrations

```bash
python manage.py makemigrations barbershop
python manage.py migrate --fake-initial
```

## BƯỚC 3: Test Database Connection

Tạo file test_db.py trong thư mục gốc:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from barbershop.models import *

# Test query
print("Tổng số người dùng:", NguoiDung.objects.count())
print("Tổng số dịch vụ:", DichVu.objects.count())
print("Tổng số đặt lịch:", DatLich.objects.count())
```

Chạy:
```bash
python test_db.py
```

## BƯỚC 4: Cập nhật Views - VÍ DỤ

### 4.1. Admin Dashboard (views.py)

**TỪ:**
```python
def admin_dashboard(request):
    context = {
        'today_bookings': 15,
        'today_revenue': 4500000,
        # ... hardcoded data
    }
    return render(request, 'admin/dashboard.html', context)
```

**THÀNH:**
```python
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import date, timedelta
from barbershop.models import *

def admin_dashboard(request):
    today = date.today()
    
    # Lấy số lịch hẹn hôm nay
    today_bookings = DatLich.objects.filter(
        ngay_hen=today,
        da_xoa=False
    ).count()
    
    # Doanh thu hôm nay từ hóa đơn
    today_revenue = HoaDon.objects.filter(
        ngay_thanh_toan__date=today,
        da_xoa=False
    ).aggregate(total=Sum('thanh_tien'))['total'] or 0
    
    # Tổng khách hàng
    total_customers = NguoiDung.objects.filter(
        vai_tro='khach_hang',
        da_xoa=False
    ).count()
    
    # Lịch hẹn chờ xác nhận
    pending_bookings = DatLich.objects.filter(
        trang_thai='cho_xac_nhan',
        da_xoa=False
    ).count()
    
    # Doanh thu 7 ngày qua
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    revenue_chart_data = []
    revenue_chart_labels = []
    
    for day in last_7_days:
        revenue = HoaDon.objects.filter(
            ngay_thanh_toan__date=day,
            da_xoa=False
        ).aggregate(total=Sum('thanh_tien'))['total'] or 0
        revenue_chart_data.append(float(revenue))
        revenue_chart_labels.append(day.strftime('%d/%m'))
    
    # Top dịch vụ
    top_services = DichVuDatLich.objects.filter(
        dat_lich__da_xoa=False,
        dat_lich__trang_thai='hoan_thanh'
    ).values('ten_dich_vu').annotate(
        count=Count('id'),
        revenue=Sum('thanh_tien')
    ).order_by('-revenue')[:3]
    
    # Lịch hẹn sắp tới hôm nay
    upcoming_bookings = DatLich.objects.filter(
        ngay_hen=today,
        gio_hen__gte=timezone.now().time(),
        trang_thai__in=['cho_xac_nhan', 'da_xac_nhan'],
        da_xoa=False
    ).select_related('khach_hang', 'nhan_vien')[:5]
    
    context = {
        'today_bookings': today_bookings,
        'today_revenue': today_revenue,
        'total_customers': total_customers,
        'pending_bookings': pending_bookings,
        'revenue_chart_labels': revenue_chart_labels,
        'revenue_chart_data': revenue_chart_data,
        'top_services': [
            {
                'name': s['ten_dich_vu'],
                'count': s['count'],
                'revenue': s['revenue']
            } for s in top_services
        ],
        'upcoming_bookings': [
            {
                'time': booking.gio_hen.strftime('%H:%M'),
                'customer': booking.ten_khach_hang or booking.khach_hang.ho_ten,
                'service': ', '.join([dv.ten_dich_vu for dv in booking.dich_vu_dat_lich.all()]),
                'staff': booking.nhan_vien.ho_ten if booking.nhan_vien else 'Chưa phân'
            } for booking in upcoming_bookings
        ]
    }
    return render(request, 'admin/dashboard.html', context)
```

### 4.2. Admin Staff List

**THÀNH:**
```python
def admin_staff(request):
    # Lấy danh sách nhân viên
    staff_list = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        da_xoa=False
    ).select_related('thong_tin_nhan_vien')
    
    staff_data = []
    for staff in staff_list:
        info = getattr(staff, 'thong_tin_nhan_vien', None)
        staff_data.append({
            'id': staff.id,
            'ho_ten': staff.ho_ten,
            'chuc_vu': info.chuyen_mon if info else 'N/A',
            'so_dien_thoai': staff.so_dien_thoai,
            'trang_thai': 'active' if staff.trang_thai else 'inactive',
            'avg_rating': float(info.danh_gia_trung_binh) if info else 0.0,
            'total_services': info.tong_luot_phuc_vu if info else 0
        })
    
    context = {
        'staff_list': staff_data,
        'total_staff': len(staff_data),
        'active_staff': sum(1 for s in staff_data if s['trang_thai'] == 'active'),
    }
    return render(request, 'admin/staff.html', context)
```

### 4.3. Admin Bookings

**THÀNH:**
```python
def admin_bookings(request):
    # Lấy danh sách đặt lịch
    bookings = DatLich.objects.filter(
        da_xoa=False
    ).select_related('khach_hang', 'nhan_vien').prefetch_related('dich_vu_dat_lich')
    
    # Đếm theo trạng thái
    total_bookings = bookings.count()
    confirmed = bookings.filter(trang_thai='da_xac_nhan').count()
    pending = bookings.filter(trang_thai='cho_xac_nhan').count()
    completed = bookings.filter(trang_thai='hoan_thanh').count()
    
    # Danh sách bookings gần nhất
    recent_bookings = bookings.order_by('-ngay_hen', '-gio_hen')[:20]
    
    booking_data = []
    for booking in recent_bookings:
        services = ', '.join([dv.ten_dich_vu for dv in booking.dich_vu_dat_lich.all()])
        booking_data.append({
            'id': booking.id,
            'ma_dat_lich': booking.ma_dat_lich,
            'date': booking.ngay_hen.strftime('%Y-%m-%d'),
            'time': booking.gio_hen.strftime('%H:%M'),
            'customer': booking.ten_khach_hang or (booking.khach_hang.ho_ten if booking.khach_hang else 'N/A'),
            'service': services,
            'staff': booking.nhan_vien.ho_ten if booking.nhan_vien else 'Chưa phân',
            'status': booking.trang_thai,
            'thanh_tien': float(booking.thanh_tien)
        })
    
    context = {
        'total_bookings': total_bookings,
        'confirmed': confirmed,
        'pending': pending,
        'completed': completed,
        'bookings': booking_data
    }
    return render(request, 'admin/bookings.html', context)
```

### 4.4. Admin Services

**THÀNH:**
```python
def admin_services(request):
    # Lấy danh sách dịch vụ
    services = DichVu.objects.filter(
        da_xoa=False
    ).select_related('danh_muc').order_by('thu_tu', 'ten_dich_vu')
    
    services_data = []
    for service in services:
        services_data.append({
            'id': service.id,
            'ten_dich_vu': service.ten_dich_vu,
            'danh_muc': service.danh_muc.ten_danh_muc if service.danh_muc else 'N/A',
            'gia': float(service.gia),
            'thoi_gian': service.thoi_gian_thuc_hien,
            'active': service.trang_thai
        })
    
    context = {
        'services': services_data,
        'total_services': len(services_data),
    }
    return render(request, 'admin/services.html', context)
```

### 4.5. Login với Database

**THÀNH:**
```python
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Có thể là email hoặc SĐT
        password = request.POST.get('password')
        
        try:
            # Tìm user theo số điện thoại hoặc email
            user = NguoiDung.objects.get(
                Q(so_dien_thoai=username) | Q(email=username),
                da_xoa=False,
                trang_thai=True
            )
            
            # Kiểm tra password (sử dụng bcrypt)
            if user.check_password(password):
                # Lưu user vào session
                request.session['user_id'] = user.id
                request.session['vai_tro'] = user.vai_tro
                
                # Redirect theo vai trò
                if user.vai_tro == 'quan_ly':
                    return redirect('admin_dashboard')
                elif user.vai_tro == 'nhan_vien':
                    return redirect('staff_dashboard')
                else:
                    # Khách hàng - redirect về trang khách
                    return redirect('login')  # Hoặc customer dashboard nếu có
            else:
                context = {'error': 'Sai mật khẩu!'}
        except NguoiDung.DoesNotExist:
            context = {'error': 'Tài khoản không tồn tại!'}
    else:
        context = {}
    
    return render(request, 'login.html', context)


def logout_view(request):
    # Xóa session
    request.session.flush()
    return redirect('login')
```

## BƯỚC 5: Tạo Middleware kiểm tra đăng nhập

Tạo file `barbershop/middleware.py`:

```python
from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Các URL không cần đăng nhập
        public_urls = [
            reverse('login'),
            '/static/',
        ]
        
        # Kiểm tra nếu chưa đăng nhập và không phải URL public
        if not request.session.get('user_id'):
            if not any(request.path.startswith(url) for url in public_urls):
                return redirect('login')
        
        response = self.get_response(request)
        return response
```

Thêm vào `settings.py`:
```python
MIDDLEWARE = [
    # ... các middleware khác
    'barbershop.middleware.AuthenticationMiddleware',  # Thêm dòng này
]
```

## BƯỚC 6: Test từng view

1. Cập nhật một view (ví dụ: `admin_dashboard`)
2. Chạy server: `python manage.py runserver`
3. Truy cập URL tương ứng
4. Kiểm tra xem data có hiển thị đúng không

## LƯU Ý QUAN TRỌNG

1. **Bcrypt passwords**: Database dùng bcrypt để hash password. Model `NguoiDung` đã có methods `set_password()` và `check_password()`.

2. **Test accounts từ database**:
   - Quản lý: 0901111111 / 123456
   - Nhân viên: 0902222222 / 123456
   - Khách hàng: 0906666666 / 123456

3. **Foreign Keys**: Luôn dùng `select_related()` và `prefetch_related()` để tối ưu queries.

4. **Soft Delete**: Tất cả queries phải filter `da_xoa=False`.

5. **Timezone**: Dùng `timezone.now()` thay vì `datetime.now()`.

## CÁC VIEWS CẦN CẬP NHẬT (TỔNG: 38 VIEWS)

### Admin (21 views):
- [x] admin_dashboard (ví dụ trên)
- [x] admin_staff (ví dụ trên)
- [x] admin_bookings (ví dụ trên)
- [x] admin_services (ví dụ trên)
- [ ] admin_invoices
- [ ] admin_customers
- [ ] admin_work_schedule
- [ ] admin_promotions
- [ ] admin_reports
- [ ] admin_reviews
- [ ] admin_pos_report
- [ ] admin_settings
- [ ] admin_inventory
- [ ] admin_salary
- [ ] admin_attendance
- [ ] admin_loyalty
- [ ] admin_staff_detail
- [ ] admin_staff_edit
- [ ] admin_bookings_create
- [ ] admin_content

### Staff (9 views):
- [ ] staff_dashboard
- [ ] staff_pos
- [ ] staff_today_bookings
- [ ] staff_schedule
- [ ] staff_my_customers
- [ ] staff_revenue
- [ ] staff_profile
- [ ] staff_commission
- [ ] staff_bookings_create

### Auth (3 views):
- [x] login_view (ví dụ trên)
- [x] logout_view (ví dụ trên)
- [x] page_not_found (giữ nguyên)

## BƯỚC TIẾP THEO

Sau khi test thành công 4 views mẫu trên, bạn có thể:
1. Áp dụng pattern tương tự cho các views còn lại
2. Hoặc yêu cầu tôi cập nhật từng nhóm views cụ thể

Tôi đề xuất làm theo thứ tự ưu tiên:
1. Authentication (login/logout) - DONE
2. Dashboard views (admin + staff)
3. Booking management (tạo, sửa, xóa)
4. Service management
5. Customer management
6. Reports & Analytics
7. Settings & Configuration
