# HƯỚNG DẪN DI CHUYỂN URL PATTERNS

## 📋 TỔNG QUAN
File `barbershop/urls.py` hiện có **125 URL patterns**. 
Bạn sẽ di chuyển chúng sang 7 apps, **GIỮ LẠI** 3 Auth URLs trong barbershop/urls.py.

---

## 🎯 URL PATTERNS CẦN GIỮ LẠI TRONG barbershop/urls.py

### Auth URLs (3 patterns) - KHÔNG DI CHUYỂN
```python
from barbershop import views

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    
    # ========== GIỮ LẠI - Auth URLs ==========
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # ========== KẾT THÚC - Auth URLs ==========
    
    # Thêm include cho 7 apps VÀO ĐÂY (xem phần dưới)
    
    # Media files (GIỮ LẠI)
    # ... (phần serve media files cuối file)
]
```

---

## 📦 URL PATTERNS DI CHUYỂN - CORE APP

### File đích: `core/urls.py`

Copy các URL patterns sau vào `core/urls.py`:

```python
"""
URL configuration for core app (Dashboard, Settings, Content)
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # ========== BẮT ĐẦU - Di chuyển từ barbershop/urls.py ==========
    
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Staff Dashboard
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Admin Settings
    path('admin/settings/', views.admin_settings, name='admin_settings'),
    
    # Settings API endpoints
    path('api/settings/general/', views.admin_settings_api_general, name='admin_settings_api_general'),
    path('api/settings/business-hours/', views.admin_settings_api_business_hours, name='admin_settings_api_business_hours'),
    path('api/settings/services/', views.admin_settings_api_services, name='admin_settings_api_services'),
    path('api/settings/payments/', views.admin_settings_api_payments, name='admin_settings_api_payments'),
    
    # Admin Content
    path('admin/content/', views.admin_content, name='admin_content'),
    
    # ========== KẾT THÚC ==========
]
```

### Vị trí trong barbershop/urls.py:
- Line 17: `path('admin/', views.admin_dashboard, name='admin_dashboard')`
- Line 18: `path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard')`
- Line 39: `path('admin/settings/', views.admin_settings, name='admin_settings')`
- Lines 41-44: Settings API endpoints
- Line 61: `path('admin/content/', views.admin_content, name='admin_content')`
- Lines 64-65: Staff dashboard

---

## 📦 URL PATTERNS DI CHUYỂN - ACCOUNTS APP

### File đích: `accounts/urls.py`

```python
"""
URL configuration for accounts app (Staff, Customers, Profile)
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # ========== BẮT ĐẦU - Di chuyển từ barbershop/urls.py ==========
    
    # Admin Staff
    path('admin/staff/', views.admin_staff, name='admin_staff'),
    path('admin/staff/<int:staff_id>/', views.admin_staff_detail, name='admin_staff_detail'),
    path('admin/staff/edit/<int:staff_id>/', views.admin_staff_edit, name='admin_staff_edit'),
    
    # Admin Customers
    path('admin/customers/', views.admin_customers, name='admin_customers'),
    
    # API Customer
    path('api/customers/<int:customer_id>/', views.api_customer_detail, name='api_customer_detail'),
    path('api/customers/<int:customer_id>/detail/', views.api_customer_detail_staff, name='api_customer_detail_staff'),
    
    # Staff Profile
    path('staff/profile/', views.staff_profile, name='staff_profile'),
    path('api/staff/update-profile/', views.api_staff_update_profile, name='api_staff_update_profile'),
    path('api/staff/change-password/', views.api_staff_change_password, name='api_staff_change_password'),
    path('api/staff/upload-avatar/', views.api_staff_upload_avatar, name='api_staff_upload_avatar'),
    path('api/staff/update-notifications/', views.api_staff_update_notifications, name='api_staff_update_notifications'),
    
    # Staff My Customers
    path('staff/my-customers/', views.staff_my_customers, name='staff_my_customers'),
    path('staff/my-customers/export/', views.staff_customers_export, name='staff_customers_export'),
    
    # ========== KẾT THÚC ==========
]
```

### Vị trí trong barbershop/urls.py:
- Line 19: `path('admin/staff/', ...)`
- Line 48: `path('admin/staff/<int:staff_id>/', ...)`
- Line 49: `path('admin/staff/edit/<int:staff_id>/', ...)`
- Line 22: `path('admin/customers/', ...)`
- Lines 69, 108-111: Staff profile URLs
- Lines 112-113: Staff my-customers URLs

---

## 📦 URL PATTERNS DI CHUYỂN - SERVICES APP

### File đích: `services/urls.py`

```python
"""
URL configuration for services app (Services, Promotions, Vouchers)
"""
from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # ========== BẮT ĐẦU - Di chuyển từ barbershop/urls.py ==========
    
    # Admin Services
    path('admin/services/', views.admin_services, name='admin_services'),
    
    # Services API URLs
    path('api/services/', views.api_service_crud, name='api_services_create'),
    path('api/services/<int:service_id>/', views.api_service_crud, name='api_services_detail'),
    path('api/services/<int:service_id>/toggle-status/', views.api_service_toggle_status, name='api_service_toggle_status'),
    path('api/services/update-order/', views.api_service_update_order, name='api_service_update_order'),
    
    # Admin Promotions
    path('admin/promotions/', views.admin_promotions, name='admin_promotions'),
    path('admin/promotions/stats/<int:voucher_id>/', views.admin_promotion_stats, name='admin_promotion_stats'),
    path('admin/promotions/delete/<int:voucher_id>/', views.admin_delete_promotion, name='admin_delete_promotion'),
    path('admin/promotions/export/', views.admin_export_promotions, name='admin_promotions_export'),
    
    # Test Promotions
    path('test/promotions/', views.test_promotions, name='test_promotions'),
    
    # ========== KẾT THÚC ==========
]
```

### Vị trí trong barbershop/urls.py:
- Line 23: `path('admin/services/', ...)`
- Lines 78-81: Services API URLs
- Lines 25-28: Admin promotions
- Line 50: Test promotions
- Line 59: Admin promotions export

---

## 📦 URL PATTERNS DI CHUYỂN - BOOKINGS APP

### File đích: `bookings/urls.py`

```python
"""
URL configuration for bookings app (Bookings, Invoices, POS)
"""
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # ========== BẮT ĐẦU - Di chuyển từ barbershop/urls.py ==========
    
    # Admin Bookings
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/bookings/create/', views.admin_bookings_create, name='admin_bookings_create'),
    path('admin/bookings/<int:booking_id>/', views.admin_booking_detail, name='admin_booking_detail'),
    path('admin/bookings/<int:booking_id>/cancel/', views.admin_booking_cancel, name='admin_booking_cancel'),
    path('admin/bookings/<int:booking_id>/checkin/', views.admin_booking_checkin, name='admin_booking_checkin'),
    path('admin/bookings/<int:booking_id>/complete/', views.admin_booking_complete, name='admin_booking_complete'),
    path('admin/bookings/export/', views.admin_bookings_export, name='admin_bookings_export'),
    
    # Dashboard action endpoints
    path('admin/booking-approve/<int:booking_id>/', views.admin_booking_approve, name='admin_booking_approve'),
    path('admin/booking-reject/<int:booking_id>/', views.admin_booking_reject, name='admin_booking_reject'),
    
    # Admin Invoices
    path('admin/invoices/', views.admin_invoices, name='admin_invoices'),
    path('admin/invoices/export/excel/', views.admin_invoices_export_excel, name='admin_invoices_export_excel'),
    path('admin/invoices/export/pdf/', views.admin_invoices_export_pdf, name='admin_invoices_export_pdf'),
    
    # Staff POS
    path('staff/pos/', views.staff_pos, name='staff_pos'),
    
    # Staff Bookings
    path('staff/bookings/create/', views.staff_bookings_create, name='staff_bookings_create'),
    
    # Staff action endpoints
    path('staff/booking-checkin/<int:booking_id>/', views.staff_booking_checkin, name='staff_booking_checkin'),
    path('staff/booking-complete/<int:booking_id>/', views.staff_booking_complete, name='staff_booking_complete'),
    
    # API URLs
    path('api/search-customer/', views.api_search_customer, name='api_search_customer'),
    path('api/load-booking/', views.api_load_booking, name='api_load_booking'),
    
    # Booking API endpoints
    path('api/bookings/<int:booking_id>/confirm/', views.api_booking_confirm, name='api_booking_confirm'),
    path('api/bookings/<int:booking_id>/check-in/', views.api_booking_checkin, name='api_booking_checkin'),
    path('api/bookings/<int:booking_id>/complete/', views.api_booking_complete_today, name='api_booking_complete_today'),
    path('api/bookings/<int:booking_id>/cancel/', views.api_booking_cancel, name='api_booking_cancel'),
    path('api/bookings/<int:booking_id>/', views.api_booking_detail, name='api_booking_detail'),
    
    # ========== KẾT THÚC ==========
]
```

### Vị trí trong barbershop/urls.py:
- Line 20: Admin bookings
- Lines 51-56: Booking actions
- Line 21: Admin invoices
- Lines 57-58: Invoice exports
- Line 66: Staff POS
- Line 72: Staff bookings create
- Lines 82-92: Staff actions và Booking API endpoints
- Lines 93-97: Booking API (confirm, check-in, complete, cancel, detail)

---

## 📦 URL PATTERNS DI CHUYỂN - ATTENDANCE APP

### File đích: `attendance/urls.py`

```python
"""
URL configuration for attendance app (Work Schedule, Leave Requests, Check-in/out, Salary)
"""
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # ========== BẮT ĐẦU - Di chuyển từ barbershop/urls.py ==========
    
    # Admin Work Schedule
    path('admin/work-schedule/', views.admin_work_schedule, name='admin_work_schedule'),
    path('admin/schedule/export/', views.admin_export_schedule, name='admin_schedule_export'),
    
    # Admin Leave Requests
    path('admin/leave-requests/<int:leave_id>/approve/', views.admin_leave_request_approve, name='admin_leave_request_approve'),
    path('admin/leave-requests/<int:leave_id>/reject/', views.admin_leave_request_reject, name='admin_leave_request_reject'),
    
    # Dashboard action endpoints
    path('admin/leave-approve/<int:leave_id>/', views.admin_leave_approve, name='admin_leave_approve'),
    path('admin/leave-reject/<int:leave_id>/', views.admin_leave_reject, name='admin_leave_reject'),
    
    # Admin Attendance & Salary
    path('admin/attendance/', views.admin_attendance, name='admin_attendance'),
    path('admin/salary/', views.admin_salary, name='admin_salary'),
    
    # Staff Today Bookings
    path('staff/today-bookings/', views.staff_today_bookings, name='staff_today_bookings'),
    
    # Staff Schedule
    path('staff/schedule/', views.staff_schedule, name='staff_schedule'),
    path('staff/register-shift/', views.staff_register_shift, name='staff_register_shift'),
    
    # Attendance API endpoints
    path('api/attendance/check-in/', views.api_attendance_checkin, name='api_attendance_checkin'),
    path('api/attendance/check-out/', views.api_attendance_checkout, name='api_attendance_checkout'),
    
    # Leave Request API endpoints
    path('api/leave-requests/', views.api_leave_request_create, name='api_leave_request_create'),
    path('api/leave-requests/<int:leave_id>/', views.api_leave_request_cancel, name='api_leave_request_cancel'),
    
    # Schedule API endpoints
    path('api/schedule/day/<str:date_str>/', views.api_schedule_day_detail, name='api_schedule_day_detail'),
    
    # ========== KẾT THÚC ==========
]
```

### Vị trí trong barbershop/urls.py:
- Line 24: Admin work schedule
- Line 60: Admin schedule export
- Lines 54-55: Leave approve/reject
- Lines 90-91: Dashboard leave actions
- Lines 46-47: Admin attendance & salary
- Lines 67-70: Staff schedule URLs
- Lines 99-104: Attendance & Leave API endpoints

---

## 📦 URL PATTERNS DI CHUYỂN - REPORTS APP

### File đích: `reports/urls.py`

```python
"""
URL configuration for reports app (Analytics, Exports - Excel/PDF)
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # ========== BẮT ĐẦU - Di chuyển từ barbershop/urls.py ==========
    
    # Admin Reports
    path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('admin/reports/export/excel/', views.admin_reports_export_excel, name='admin_reports_export_excel'),
    path('admin/reports/export/pdf/', views.admin_reports_export_pdf, name='admin_reports_export_pdf'),
    
    # Admin POS Report
    path('admin/pos-report/', views.admin_pos_report, name='admin_pos_report'),
    
    # ========== KẾT THÚC ==========
]
```

### Vị trí trong barbershop/urls.py:
- Line 29: Admin reports
- Line 38: Admin POS report
- Lines 53-54: Reports export

---

## 📦 URL PATTERNS DI CHUYỂN - REVIEWS APP

### File đích: `reviews/urls.py`

```python
"""
URL configuration for reviews app (Reviews, Loyalty program)
"""
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # ========== BẮT ĐẦU - Di chuyển từ barbershop/urls.py ==========
    
    # Admin Reviews
    path('admin/reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin/reviews/export/', views.admin_reviews_export, name='admin_reviews_export'),
    path('api/reviews/<int:review_id>/', views.admin_review_detail, name='admin_review_detail'),
    path('api/reviews/<int:review_id>/reply/', views.admin_review_reply, name='admin_review_reply'),
    path('api/reviews/<int:review_id>/delete/', views.admin_review_delete, name='admin_review_delete'),
    
    # Admin Loyalty
    path('admin/loyalty/', views.admin_loyalty, name='admin_loyalty'),
    
    # ========== KẾT THÚC ==========
]
```

### Vị trí trong barbershop/urls.py:
- Lines 30-34: Admin reviews & review API
- Line 47: Admin loyalty

---

## 🔄 CẬP NHẬT barbershop/urls.py

### Thêm include cho 7 apps:

```python
"""
URL configuration for barbershop project.
"""
from django.contrib import admin
from django.urls import path, include  # ← THÊM include
from django.conf import settings
from django.conf.urls.static import static
from barbershop import views

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    
    # ========== GIỮ LẠI - Auth URLs ==========
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # ========== KẾT THÚC - Auth URLs ==========
    
    # ========== BẮT ĐẦU - Include 7 modular apps ==========
    path('', include('core.urls')),          # Dashboard, Settings
    path('', include('accounts.urls')),      # Staff, Customers, Profile
    path('', include('services.urls')),      # Services, Promotions
    path('', include('bookings.urls')),      # Bookings, Invoices, POS
    path('', include('attendance.urls')),    # Schedule, Attendance, Leave
    path('', include('reports.urls')),       # Reports, Analytics
    path('', include('reviews.urls')),       # Reviews, Loyalty
    # ========== KẾT THÚC - Include apps ==========
    
    # ========== SAU ĐÓ COMMENT TẤT CẢ CÁC URL CŨ ==========
    # path('admin/', views.admin_dashboard, name='admin_dashboard'),
    # path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # ... (comment tất cả URLs đã di chuyển)
    # ========== KẾT THÚC - Old URLs ==========
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## ✅ CHECKLIST URL PATTERNS

### CORE (10 URLs)
- [ ] admin/, admin/dashboard/ → admin_dashboard
- [ ] staff/, staff/dashboard/ → staff_dashboard
- [ ] admin/settings/ → admin_settings
- [ ] api/settings/* (4 endpoints)
- [ ] admin/content/ → admin_content

### ACCOUNTS (13 URLs)
- [ ] admin/staff/* (3 URLs)
- [ ] admin/customers/
- [ ] api/customers/* (2 URLs)
- [ ] staff/profile/ + 4 profile APIs
- [ ] staff/my-customers/ + export

### SERVICES (9 URLs)
- [ ] admin/services/
- [ ] api/services/* (4 URLs)
- [ ] admin/promotions/* (3 URLs + export)
- [ ] test/promotions/

### BOOKINGS (24 URLs)
- [ ] admin/bookings/* (7 URLs)
- [ ] admin/booking-* (2 dashboard actions)
- [ ] admin/invoices/* (3 URLs)
- [ ] staff/pos/, staff/bookings/create/
- [ ] staff/booking-* (2 staff actions)
- [ ] api/search-customer/, api/load-booking/
- [ ] api/bookings/* (5 booking APIs)

### ATTENDANCE (16 URLs)
- [ ] admin/work-schedule/, admin/schedule/export/
- [ ] admin/leave-requests/* (2 URLs)
- [ ] admin/leave-* (2 dashboard actions)
- [ ] admin/attendance/, admin/salary/
- [ ] staff/today-bookings/
- [ ] staff/schedule/, staff/register-shift/
- [ ] api/attendance/* (2 URLs)
- [ ] api/leave-requests/* (2 URLs)
- [ ] api/schedule/day/*

### REPORTS (4 URLs)
- [ ] admin/reports/ + 2 exports
- [ ] admin/pos-report/

### REVIEWS (6 URLs)
- [ ] admin/reviews/ + export
- [ ] api/reviews/* (3 URLs)
- [ ] admin/loyalty/

---

## 🎯 LƯU Ý QUAN TRỌNG

1. **Thứ tự include**: Đặt các app includes TRƯỚC các URL patterns cụ thể
2. **URL name**: Giữ nguyên URL names để templates không bị lỗi
3. **app_name**: Mỗi app phải có `app_name` để namespace
4. **Comment old URLs**: SAU KHI include xong, comment tất cả old URLs trong barbershop/urls.py

---

## 📞 HỖ TRỢ

Nếu cần giúp với URL cụ thể, hãy hỏi tôi!
