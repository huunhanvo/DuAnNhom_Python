# HƯỚNG DẪN DI CHUYỂN CODE - BARBERSHOP REFACTORING

## 📋 TỔNG QUAN
Bạn sẽ di chuyển code từ `barbershop/views.py` (6050 dòng) sang 7 apps modular.
Tổng cộng: **~80 view functions** cần di chuyển

---

## 🎯 QUY TẮC QUAN TRỌNG

### ✅ ĐƯỢC PHÉP:
- Copy code từ barbershop/views.py sang app/views.py
- Xóa code trong các app mới (core, accounts, services...)
- Sửa đổi code trong các app mới

### ❌ KHÔNG ĐƯỢC PHÉP:
- **KHÔNG được xóa code trong barbershop/views.py**
- **CHỈ được comment** code trong barbershop/views.py sau khi đã copy xong

---

## 📦 CẤU TRÚC 7 APPS ĐÃ TẠO

### 1. **core** - Dashboard, Settings, Decorators
- ✅ Đã tạo: `core/views.py`, `core/urls.py`, `core/decorators.py`
- ✅ Decorators đã sẵn sàng trong `core/decorators.py`

### 2. **accounts** - Staff, Customers, Profile
- ✅ Đã tạo: `accounts/views.py`, `accounts/urls.py`

### 3. **services** - Services, Promotions, Vouchers
- ✅ Đã tạo: `services/views.py`, `services/urls.py`

### 4. **bookings** - Bookings, Invoices, POS
- ✅ Đã tạo: `bookings/views.py`, `bookings/urls.py`

### 5. **attendance** - Work Schedule, Leave, Salary
- ✅ Đã tạo: `attendance/views.py`, `attendance/urls.py`

### 6. **reports** - Analytics, Exports
- ✅ Đã tạo: `reports/views.py`, `reports/urls.py`

### 7. **reviews** - Reviews, Loyalty
- ✅ Đã tạo: `reviews/views.py`, `reviews/urls.py`

---

## 📝 CHI TIẾT DI CHUYỂN - CORE APP

### File đích: `core/views.py`

#### Views cần copy:

1. **admin_dashboard** (dòng ~122-200 trong barbershop/views.py)
   ```python
   @require_role(['quan_ly'])
   def admin_dashboard(request):
       """Admin Dashboard"""
       # ... COPY TOÀN BỘ CODE ...
   ```
   👉 Vị trí trong barbershop/views.py: Tìm `def admin_dashboard`

2. **staff_dashboard** 
   ```python
   @require_role(['nhan_vien', 'quan_ly'])
   def staff_dashboard(request):
       """Staff Dashboard"""
       # ... COPY TOÀN BỘ CODE ...
   ```

3. **admin_settings**
   ```python
   @require_role(['quan_ly'])
   def admin_settings(request):
       """Admin Settings"""
       # ... COPY TOÀN BỘ CODE ...
   ```

4. **admin_settings_api_general**
   ```python
   @require_role(['quan_ly'])  
   def admin_settings_api_general(request):
       """Settings API - General"""
       # ... COPY TOÀN BỘ CODE ...
   ```

5. **admin_settings_api_business_hours**
   ```python
   @require_role(['quan_ly'])
   def admin_settings_api_business_hours(request):
       """Settings API - Business Hours"""
       # ... COPY TOÀN BỘ CODE ...
   ```

6. **admin_settings_api_services**
   ```python
   @require_role(['quan_ly'])
   def admin_settings_api_services(request):
       """Settings API - Services"""
       # ... COPY TOÀN BỘ CODE ...
   ```

7. **admin_settings_api_payments**
   ```python
   @require_role(['quan_ly'])
   def admin_settings_api_payments(request):
       """Settings API - Payments"""
       # ... COPY TOÀN BỘ CODE ...
   ```

8. **admin_content**
   ```python
   @require_role(['quan_ly'])
   def admin_content(request):
       """Admin Content Management"""
       # ... COPY TOÀN BỘ CODE ...
   ```

---

## 📝 CHI TIẾT DI CHUYỂN - ACCOUNTS APP

### File đích: `accounts/views.py`

#### Views cần copy:

1. **admin_staff** - Quản lý nhân viên (CRUD, Search, Filter)
2. **admin_staff_detail** - Chi tiết nhân viên
3. **admin_staff_edit** - Sửa thông tin nhân viên
4. **admin_customers** - Quản lý khách hàng
5. **staff_profile** - Trang profile nhân viên
6. **api_staff_update_profile** - API cập nhật profile
7. **api_staff_change_password** - API đổi mật khẩu
8. **api_staff_upload_avatar** - API upload avatar
9. **api_staff_update_notifications** - API cập nhật thông báo
10. **staff_my_customers** - Danh sách khách hàng của nhân viên
11. **api_customer_detail** - API chi tiết khách hàng
12. **api_customer_detail_staff** - API chi tiết khách hàng (staff view)
13. **staff_customers_export** - Export danh sách khách hàng

---

## 📝 CHI TIẾT DI CHUYỂN - SERVICES APP

### File đích: `services/views.py`

#### Views cần copy:

1. **admin_services** - Quản lý dịch vụ
2. **api_service_crud** - API CRUD dịch vụ
3. **api_service_toggle_status** - API bật/tắt trạng thái dịch vụ
4. **api_service_update_order** - API cập nhật thứ tự dịch vụ
5. **admin_promotions** - Quản lý khuyến mãi/voucher
6. **admin_delete_promotion** - Xóa khuyến mãi
7. **admin_promotion_stats** - Thống kê khuyến mãi
8. **admin_export_promotions** - Export danh sách khuyến mãi
9. **test_promotions** - Test promotions (không cần auth)

---

## 📝 CHI TIẾT DI CHUYỂN - BOOKINGS APP

### File đích: `bookings/views.py`

#### Views cần copy (24 views):

**Admin Bookings:**
1. **admin_bookings** - Quản lý đặt lịch
2. **admin_bookings_create** - Tạo đặt lịch mới
3. **admin_booking_detail** - Chi tiết đặt lịch
4. **admin_booking_cancel** - Hủy đặt lịch
5. **admin_booking_checkin** - Check-in đặt lịch
6. **admin_booking_complete** - Hoàn thành đặt lịch
7. **admin_bookings_export** - Export danh sách đặt lịch
8. **admin_booking_approve** - Duyệt đặt lịch (dashboard action)
9. **admin_booking_reject** - Từ chối đặt lịch (dashboard action)

**Admin Invoices:**
10. **admin_invoices** - Quản lý hóa đơn
11. **admin_invoices_export_excel** - Export hóa đơn Excel
12. **admin_invoices_export_pdf** - Export hóa đơn PDF

**Staff:**
13. **staff_pos** - Hệ thống POS (Point of Sale)
14. **staff_bookings_create** - Tạo đặt lịch (staff)
15. **staff_booking_checkin** - Check-in (staff action)
16. **staff_booking_complete** - Hoàn thành (staff action)

**API Endpoints:**
17. **api_search_customer** - Tìm kiếm khách hàng
18. **api_load_booking** - Load thông tin đặt lịch
19. **api_booking_confirm** - Xác nhận đặt lịch
20. **api_booking_checkin** - API check-in
21. **api_booking_complete_today** - API hoàn thành (today bookings)
22. **api_booking_cancel** - API hủy đặt lịch
23. **api_booking_detail** - API chi tiết đặt lịch

---

## 📝 CHI TIẾT DI CHUYỂN - ATTENDANCE APP

### File đích: `attendance/views.py`

#### Views cần copy (16 views):

**Admin:**
1. **admin_work_schedule** - Quản lý lịch làm việc
2. **admin_leave_request_approve** - Duyệt đơn xin nghỉ
3. **admin_leave_request_reject** - Từ chối đơn xin nghỉ
4. **admin_leave_approve** - Duyệt nghỉ (dashboard action)
5. **admin_leave_reject** - Từ chối nghỉ (dashboard action)
6. **admin_attendance** - Quản lý chấm công
7. **admin_salary** - Quản lý lương
8. **admin_export_schedule** - Export lịch làm việc

**Staff:**
9. **staff_today_bookings** - Danh sách đặt lịch hôm nay
10. **staff_schedule** - Lịch làm việc của nhân viên
11. **staff_register_shift** - Đăng ký ca làm

**API Endpoints:**
12. **api_attendance_checkin** - API chấm công vào
13. **api_attendance_checkout** - API chấm công ra
14. **api_leave_request_create** - API tạo đơn xin nghỉ
15. **api_leave_request_cancel** - API hủy đơn xin nghỉ
16. **api_schedule_day_detail** - API chi tiết lịch theo ngày

---

## 📝 CHI TIẾT DI CHUYỂN - REPORTS APP

### File đích: `reports/views.py`

#### Views cần copy (4 views):

1. **admin_reports** - Trang báo cáo & thống kê
2. **admin_reports_export_excel** - Export báo cáo Excel
3. **admin_reports_export_pdf** - Export báo cáo PDF
4. **admin_pos_report** - Báo cáo POS

---

## 📝 CHI TIẾT DI CHUYỂN - REVIEWS APP

### File đích: `reviews/views.py`

#### Views cần copy (6 views):

1. **admin_reviews** - Quản lý đánh giá
2. **admin_loyalty** - Chương trình khách hàng thân thiết
3. **admin_review_reply** - Trả lời đánh giá
4. **admin_review_detail** - Chi tiết đánh giá
5. **admin_review_delete** - Xóa đánh giá
6. **admin_reviews_export** - Export danh sách đánh giá

---

## 🔧 HƯỚNG DẪN DI CHUYỂN TỪNG BƯỚC

### Bước 1: Tìm view function trong barbershop/views.py
Ví dụ: Tìm `def admin_dashboard`

### Bước 2: Copy TOÀN BỘ code (bao gồm decorator)
```python
@require_role(['quan_ly'])
def admin_dashboard(request):
    """Admin Dashboard"""
    # ... TOÀN BỘ CODE ...
    return render(request, 'admin/dashboard.html', context)
```

### Bước 3: Paste vào file views.py của app tương ứng
- Admin dashboard → `core/views.py`
- Đảm bảo thay decorator import:
  ```python
  from core.decorators import require_auth, require_role
  ```

### Bước 4: Comment code trong barbershop/views.py
**SAU KHI đã copy xong**, thêm comment:
```python
# ========== ĐÃ DI CHUYỂN - admin_dashboard ==========
# Code đã được di chuyển tới core/views.py
# Giữ lại tạm thời, sẽ xóa sau khi test thành công

# @require_role(['quan_ly'])
# def admin_dashboard(request):
#     """Admin Dashboard"""
#     # ... CODE ...

# ========== KẾT THÚC ==========
```

---

## 📋 URL PATTERNS - Cần cập nhật barbershop/urls.py

Sau khi di chuyển xong views, bạn sẽ cần update `barbershop/urls.py`:

### Thêm include cho 7 apps:
```python
from django.urls import path, include

urlpatterns = [
    # Auth URLs (GIỮ LẠI trong barbershop/urls.py)
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Include 7 apps (THÊM MỚI)
    path('', include('core.urls')),           # Dashboard, Settings
    path('', include('accounts.urls')),       # Staff, Customers
    path('', include('services.urls')),       # Services, Promotions
    path('', include('bookings.urls')),       # Bookings, Invoices, POS
    path('', include('attendance.urls')),     # Schedule, Attendance
    path('', include('reports.urls')),        # Reports
    path('', include('reviews.urls')),        # Reviews
    
    # ... rest of URLs ...
]
```

---

## ✅ CHECKLIST HOÀN THÀNH

### App: CORE
- [ ] admin_dashboard → core/views.py
- [ ] staff_dashboard → core/views.py
- [ ] admin_settings → core/views.py
- [ ] admin_settings_api_general → core/views.py
- [ ] admin_settings_api_business_hours → core/views.py
- [ ] admin_settings_api_services → core/views.py
- [ ] admin_settings_api_payments → core/views.py
- [ ] admin_content → core/views.py

### App: ACCOUNTS
- [ ] admin_staff → accounts/views.py
- [ ] admin_staff_detail → accounts/views.py
- [ ] admin_staff_edit → accounts/views.py
- [ ] admin_customers → accounts/views.py
- [ ] staff_profile → accounts/views.py
- [ ] api_staff_update_profile → accounts/views.py
- [ ] api_staff_change_password → accounts/views.py
- [ ] api_staff_upload_avatar → accounts/views.py
- [ ] api_staff_update_notifications → accounts/views.py
- [ ] staff_my_customers → accounts/views.py
- [ ] api_customer_detail → accounts/views.py
- [ ] api_customer_detail_staff → accounts/views.py
- [ ] staff_customers_export → accounts/views.py

### App: SERVICES
- [ ] admin_services → services/views.py
- [ ] api_service_crud → services/views.py
- [ ] api_service_toggle_status → services/views.py
- [ ] api_service_update_order → services/views.py
- [ ] admin_promotions → services/views.py
- [ ] admin_delete_promotion → services/views.py
- [ ] admin_promotion_stats → services/views.py
- [ ] admin_export_promotions → services/views.py
- [ ] test_promotions → services/views.py

### App: BOOKINGS
- [ ] admin_bookings → bookings/views.py
- [ ] admin_bookings_create → bookings/views.py
- [ ] admin_booking_detail → bookings/views.py
- [ ] admin_booking_cancel → bookings/views.py
- [ ] admin_booking_checkin → bookings/views.py
- [ ] admin_booking_complete → bookings/views.py
- [ ] admin_bookings_export → bookings/views.py
- [ ] admin_booking_approve → bookings/views.py
- [ ] admin_booking_reject → bookings/views.py
- [ ] admin_invoices → bookings/views.py
- [ ] admin_invoices_export_excel → bookings/views.py
- [ ] admin_invoices_export_pdf → bookings/views.py
- [ ] staff_pos → bookings/views.py
- [ ] staff_bookings_create → bookings/views.py
- [ ] api_search_customer → bookings/views.py
- [ ] api_load_booking → bookings/views.py
- [ ] api_booking_confirm → bookings/views.py
- [ ] api_booking_checkin → bookings/views.py
- [ ] api_booking_complete_today → bookings/views.py
- [ ] api_booking_cancel → bookings/views.py
- [ ] api_booking_detail → bookings/views.py
- [ ] staff_booking_checkin → bookings/views.py
- [ ] staff_booking_complete → bookings/views.py

### App: ATTENDANCE
- [ ] admin_work_schedule → attendance/views.py
- [ ] admin_leave_request_approve → attendance/views.py
- [ ] admin_leave_request_reject → attendance/views.py
- [ ] admin_leave_approve → attendance/views.py
- [ ] admin_leave_reject → attendance/views.py
- [ ] admin_attendance → attendance/views.py
- [ ] admin_salary → attendance/views.py
- [ ] admin_export_schedule → attendance/views.py
- [ ] staff_today_bookings → attendance/views.py
- [ ] staff_schedule → attendance/views.py
- [ ] staff_register_shift → attendance/views.py
- [ ] api_attendance_checkin → attendance/views.py
- [ ] api_attendance_checkout → attendance/views.py
- [ ] api_leave_request_create → attendance/views.py
- [ ] api_leave_request_cancel → attendance/views.py
- [ ] api_schedule_day_detail → attendance/views.py

### App: REPORTS
- [ ] admin_reports → reports/views.py
- [ ] admin_reports_export_excel → reports/views.py
- [ ] admin_reports_export_pdf → reports/views.py
- [ ] admin_pos_report → reports/views.py

### App: REVIEWS
- [ ] admin_reviews → reviews/views.py
- [ ] admin_loyalty → reviews/views.py
- [ ] admin_review_reply → reviews/views.py
- [ ] admin_review_detail → reviews/views.py
- [ ] admin_review_delete → reviews/views.py
- [ ] admin_reviews_export → reviews/views.py

---

## 🎯 LƯU Ý QUAN TRỌNG

1. **Imports**: Đảm bảo thay đổi decorators import trong mỗi app:
   ```python
   from core.decorators import require_auth, require_role
   ```

2. **Models**: Giữ nguyên import từ barbershop.models:
   ```python
   from barbershop.models import NguoiDung, DatLich, ...
   ```

3. **KHÔNG XÓA** code trong barbershop/views.py, CHỈ COMMENT sau khi copy xong

4. **GIỮ LẠI** trong barbershop/views.py:
   - login_view
   - logout_view
   - page_not_found
   - Decorators (require_auth, require_role) - tạm thời

5. **Test từng app** sau khi di chuyển xong để đảm bảo không có lỗi

---

## 📞 HỖ TRỢ

Nếu bạn cần hỗ trợ với view cụ thể nào, hãy hỏi tôi!
Ví dụ: "Tìm giúp tôi code của admin_staff trong barbershop/views.py"
