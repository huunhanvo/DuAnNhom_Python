# 🔗 URL PATTERNS REFERENCE - BARBERSHOP WEBSITE

## Quick Reference Guide cho tất cả URL patterns

---

## 📱 CUSTOMER URLS

### Public Pages (core app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/` | `core:home` | `customer/home.html` | Trang chủ |
| `/about/` | `core:about` | `customer/about.html` | Giới thiệu |
| `/services/` | `core:services` | `customer/services.html` | Danh sách dịch vụ |
| `/stylists/` | `core:stylists` | `customer/stylists.html` | Danh sách stylist |
| `/stylists/<id>/` | `core:stylist_detail` | `customer/stylist_detail.html` | Chi tiết stylist |
| `/promotions/` | `core:promotions` | `customer/promotions.html` | Khuyến mãi |

### Authentication (accounts app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/accounts/register/` | `accounts:register` | `customer/register.html` | Đăng ký khách hàng |
| `/accounts/login/` | `accounts:customer_login` | `customer/login.html` | Đăng nhập |
| `/accounts/logout/` | `accounts:customer_logout` | - | Đăng xuất |
| `/accounts/forgot-password/` | `accounts:forgot_password` | `customer/forgot_password.html` | Quên mật khẩu |
| `/accounts/verify-otp/` | `accounts:verify_otp` | - | Xác thực OTP |
| `/accounts/reset-password/` | `accounts:reset_password` | `customer/reset_password.html` | Đặt lại mật khẩu |
| `/accounts/send-otp/` | `accounts:send_otp` | - | Gửi OTP (AJAX) |

### Booking Flow (bookings app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/bookings/step1/` | `bookings:booking_step1` | `customer/booking_step1.html` | Chọn dịch vụ |
| `/bookings/step2/` | `bookings:booking_step2` | `customer/booking_step2.html` | Chọn stylist |
| `/bookings/step3/` | `bookings:booking_step3` | `customer/booking_step3.html` | Chọn ngày giờ |
| `/bookings/step4/` | `bookings:booking_step4` | `customer/booking_step4.html` | Xác nhận & thanh toán |
| `/bookings/create/` | `bookings:create_booking` | - | Tạo booking (POST) |
| `/bookings/success/` | `bookings:booking_success` | `customer/booking_success.html` | Đặt lịch thành công |

### Booking APIs (bookings app)
| URL | View Name | Method | Description |
|-----|-----------|--------|-------------|
| `/bookings/api/time-slots/` | `bookings:get_time_slots` | GET | Lấy khung giờ trống |
| `/bookings/api/validate-voucher/` | `bookings:validate_voucher` | POST | Kiểm tra mã voucher |

### Customer Dashboard (core app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/customer/dashboard/` | `core:customer_dashboard` | `customer/customer_dashboard.html` | Tổng quan |
| `/customer/bookings/` | `core:customer_bookings` | `customer/customer_bookings.html` | Lịch đặt |
| `/customer/bookings/<id>/` | `core:customer_booking_detail` | `customer/customer_booking_detail.html` | Chi tiết lịch |
| `/customer/history/` | `core:customer_history` | `customer/customer_history.html` | Lịch sử |
| `/customer/bookings/<id>/cancel/` | `core:cancel_booking` | - | Hủy lịch (POST) |

### Rewards & Profile (core app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/customer/rewards/` | `core:customer_rewards` | `customer/customer_rewards.html` | Điểm & voucher |
| `/customer/rewards/<id>/redeem/` | `core:redeem_reward` | - | Đổi quà (POST) |
| `/customer/profile/` | `core:customer_profile` | `customer/customer_profile.html` | Thông tin cá nhân |
| `/customer/profile/update/` | `core:update_profile` | - | Cập nhật profile (POST) |
| `/customer/profile/change-password/` | `core:change_password` | `customer/customer_change_password.html` | Đổi mật khẩu |

### Favorites & Reviews (core app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/customer/favorites/` | `core:customer_favorite_stylists` | `customer/customer_favorite_stylists.html` | Thợ yêu thích |
| `/customer/favorites/<id>/toggle/` | `core:toggle_favorite` | - | Thêm/bỏ yêu thích (POST) |
| `/customer/bookings/<id>/review/` | `core:customer_review` | `customer/customer_review.html` | Đánh giá |

---

## 👔 STAFF URLS

### Staff Dashboard (core app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/staff/` | `core:staff_dashboard` | `staff/dashboard.html` | Staff dashboard |
| `/staff/dashboard/` | `core:staff_dashboard` | `staff/dashboard.html` | Staff dashboard |

### Staff Booking Management (bookings app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/staff/pos/` | `bookings:staff_pos` | `staff/pos.html` | POS system |
| `/staff/bookings/create/` | `bookings:staff_bookings_create` | `staff/bookings-create.html` | Tạo booking |

### Staff Attendance (attendance app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/staff/today-bookings/` | `attendance:staff_today_bookings` | `staff/today-bookings.html` | Lịch hôm nay |
| `/staff/schedule/` | `attendance:staff_schedule` | `staff/schedule.html` | Lịch làm việc |
| `/staff/register-shift/` | `attendance:staff_register_shift` | `staff/register-shift.html` | Đăng ký ca |

### Staff My Customers (accounts app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/staff/my-customers/` | `accounts:staff_my_customers` | `staff/my-customers.html` | Khách hàng của tôi |
| `/staff/my-customers/export/` | `accounts:staff_customers_export` | - | Export khách hàng |

### Staff Profile (staff app - if exists)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/staff/profile/` | `staff:staff_profile` | `staff/profile.html` | Thông tin cá nhân |

---

## 👨‍💼 ADMIN URLS

### Admin Dashboard (core app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/` | `core:admin_dashboard` | `admin/dashboard.html` | Admin dashboard |
| `/admin/dashboard/` | `core:admin_dashboard` | `admin/dashboard.html` | Admin dashboard |

### Admin Staff Management (accounts app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/staff/` | `accounts:admin_staff` | `admin/staff.html` | Quản lý nhân viên |
| `/admin/staff/<id>/` | `accounts:admin_staff_detail` | `admin/staff-detail.html` | Chi tiết nhân viên |
| `/admin/staff/edit/<id>/` | `accounts:admin_staff_edit` | `admin/staff-edit.html` | Sửa nhân viên |

### Admin Customers (accounts app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/customers/` | `accounts:admin_customers` | `admin/customers.html` | Quản lý khách hàng |

### Admin Bookings (bookings app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/bookings/` | `bookings:admin_bookings` | `admin/bookings.html` | Quản lý lịch hẹn |
| `/admin/bookings/<id>/` | `bookings:admin_booking_detail` | `admin/booking-detail.html` | Chi tiết lịch |
| `/admin/bookings/create/` | `bookings:admin_bookings_create` | `admin/bookings-create.html` | Tạo lịch |
| `/admin/bookings/<id>/checkin/` | `bookings:admin_booking_checkin` | - | Check-in (POST) |
| `/admin/bookings/<id>/complete/` | `bookings:admin_booking_complete` | - | Hoàn thành (POST) |
| `/admin/bookings/export/` | `bookings:admin_bookings_export` | - | Export Excel |

### Admin Invoices (bookings app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/invoices/` | `bookings:admin_invoices` | `admin/invoices.html` | Quản lý hóa đơn |
| `/admin/invoices/export/excel/` | `bookings:admin_invoices_export_excel` | - | Export Excel |
| `/admin/invoices/export/pdf/` | `bookings:admin_invoices_export_pdf` | - | Export PDF |

### Admin Services (services app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/services/` | `services:admin_services` | `admin/services.html` | Quản lý dịch vụ |

### Admin Promotions (services app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/promotions/` | `services:admin_promotions` | `admin/promotions.html` | Quản lý khuyến mãi |
| `/admin/promotions/stats/<id>/` | `services:admin_promotion_stats` | - | Thống kê voucher |
| `/admin/promotions/delete/<id>/` | `services:admin_delete_promotion` | - | Xóa voucher |
| `/admin/promotions/export/` | `services:admin_promotions_export` | - | Export Excel |

### Admin Schedule (attendance app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/work-schedule/` | `attendance:admin_work_schedule` | `admin/work-schedule.html` | Lịch làm việc |
| `/admin/schedule/export/` | `attendance:admin_export_schedule` | - | Export Excel |

### Admin Reports (reports app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/reports/` | `reports:admin_reports` | `admin/reports.html` | Báo cáo |
| `/admin/reports/export/excel/` | `reports:admin_reports_export_excel` | - | Export Excel |
| `/admin/reports/export/pdf/` | `reports:admin_reports_export_pdf` | - | Export PDF |

### Admin Reviews (reviews app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/reviews/` | `reviews:admin_reviews` | `admin/reviews.html` | Quản lý đánh giá |
| `/admin/reviews/export/` | `reviews:admin_reviews_export` | - | Export Excel |

### Admin Settings (core app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/settings/` | `core:admin_settings` | `admin/settings.html` | Cài đặt hệ thống |

### Admin Content (core app)
| URL | View Name | Template | Description |
|-----|-----------|----------|-------------|
| `/admin/content/` | `core:admin_content` | `admin/content.html` | Quản lý nội dung |

---

## 🔧 API URLS

### Services API (services app)
| URL | View Name | Method | Description |
|-----|-----------|--------|-------------|
| `/api/services/` | `services:api_services_create` | GET, POST | CRUD dịch vụ |
| `/api/services/<id>/` | `services:api_services_detail` | GET, PUT, DELETE | Chi tiết dịch vụ |
| `/api/services/<id>/toggle-status/` | `services:api_service_toggle_status` | POST | Bật/tắt dịch vụ |
| `/api/services/update-order/` | `services:api_service_update_order` | POST | Cập nhật thứ tự |

### Bookings API (bookings app)
| URL | View Name | Method | Description |
|-----|-----------|--------|-------------|
| `/api/search-customer/` | `bookings:api_search_customer` | GET | Tìm khách hàng |
| `/api/load-booking/` | `bookings:api_load_booking` | GET | Load booking |
| `/api/bookings/<id>/confirm/` | `bookings:api_booking_confirm` | POST | Xác nhận booking |
| `/api/bookings/<id>/check-in/` | `bookings:api_booking_checkin` | POST | Check-in |
| `/api/bookings/<id>/complete/` | `bookings:api_booking_complete_today` | POST | Hoàn thành |
| `/api/bookings/<id>/cancel/` | `bookings:api_booking_cancel` | POST | Hủy booking |
| `/api/bookings/<id>/` | `bookings:api_booking_detail` | GET | Chi tiết booking |

### Settings API (core app)
| URL | View Name | Method | Description |
|-----|-----------|--------|-------------|
| `/api/settings/general/` | `core:admin_settings_api_general` | GET, POST | Cài đặt chung |
| `/api/settings/business-hours/` | `core:admin_settings_api_business_hours` | GET, POST | Giờ làm việc |
| `/api/settings/services/` | `core:admin_settings_api_services` | GET, POST | Cài đặt dịch vụ |
| `/api/settings/payments/` | `core:admin_settings_api_payments` | GET, POST | Thanh toán |

---

## 🎯 URL PATTERNS BY APP

### barbershop (main app)
- `/admin-panel/` - Django admin
- `/` - Staff/Admin login (default)
- `/login/` - Staff/Admin login
- `/logout/` - Staff/Admin logout

### core
- Public pages: `/`, `/about/`, `/services/`, `/stylists/`, `/promotions/`
- Customer dashboard: `/customer/*`
- Admin dashboard: `/admin/`, `/admin/settings/`, `/admin/content/`
- Staff dashboard: `/staff/`, `/staff/dashboard/`

### accounts
- Customer auth: `/accounts/*`
- Admin staff management: `/admin/staff/*`
- Admin customers: `/admin/customers/`
- Staff my customers: `/staff/my-customers/`

### bookings
- Customer booking flow: `/bookings/*`
- Admin bookings: `/admin/bookings/*`, `/admin/invoices/*`
- Staff POS: `/staff/pos/`
- Staff booking create: `/staff/bookings/create/`
- APIs: `/api/search-customer/`, `/api/load-booking/`, `/api/bookings/*`

### services
- Admin services: `/admin/services/`
- Admin promotions: `/admin/promotions/*`
- APIs: `/api/services/*`

### attendance
- Admin schedule: `/admin/work-schedule/`
- Staff schedule: `/staff/schedule/`, `/staff/register-shift/`
- Staff today bookings: `/staff/today-bookings/`

### reports
- Admin reports: `/admin/reports/*`

### reviews
- Admin reviews: `/admin/reviews/*`

---

## 📌 IMPORTANT NOTES

### URL Naming Conventions:
- **Customer URLs:** Prefix with `customer_` (e.g., `core:customer_dashboard`)
- **Admin URLs:** Prefix with `admin_` (e.g., `bookings:admin_bookings`)
- **Staff URLs:** Prefix with `staff_` (e.g., `attendance:staff_schedule`)
- **API URLs:** Prefix with `api_` (e.g., `services:api_services_create`)

### Namespacing:
- All apps use `app_name` for URL namespacing
- Always use full namespace in templates: `{% url 'app:view_name' %}`
- Never use bare view names without namespace

### Common Mistakes to Avoid:
- ❌ `{% url 'services:services_list' %}` → Should be `{% url 'core:services' %}`
- ❌ `{% url 'core:stylists_list' %}` → Should be `{% url 'core:stylists' %}`
- ❌ `{% url 'logout' %}` → Should be `{% url 'accounts:customer_logout' %}`
- ❌ `{% url 'login' %}` → Should be `{% url 'accounts:customer_login' %}` (customer) or bare `login` (staff/admin)

---

**Last Updated:** October 13, 2025
**Status:** ✅ Complete & Verified
