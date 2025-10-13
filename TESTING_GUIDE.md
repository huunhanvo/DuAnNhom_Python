# 🧪 TESTING GUIDE - BARBERSHOP WEBSITE

## Hướng dẫn test toàn bộ hệ thống

---

## 🚀 CHUẨN BỊ

### 1. Start Development Server
```bash
python manage.py runserver
```

### 2. Open Browser
```
http://127.0.0.1:8000/
```

---

## ✅ TEST CHECKLIST

## 1. 🏠 PUBLIC PAGES

### Home Page (`/`)
- [ ] Trang chủ load thành công
- [ ] Hero section hiển thị đúng
- [ ] Featured services hiển thị (top 6)
- [ ] Top stylists hiển thị
- [ ] Recent reviews hiển thị
- [ ] CTA buttons hoạt động:
  - [ ] "Đặt lịch ngay" → `/bookings/step1/`
  - [ ] "Xem dịch vụ" → `/services/`
  - [ ] "Xem tất cả stylist" → `/stylists/`

### About Page (`/about/`)
- [ ] Trang giới thiệu load thành công
- [ ] Story section hiển thị
- [ ] Team section hiển thị
- [ ] Testimonials hiển thị

### Services Page (`/services/`)
- [ ] Danh sách dịch vụ hiển thị
- [ ] Filter theo category hoạt động
- [ ] Sort (giá, thời gian) hoạt động
- [ ] Click "Đặt lịch" → `/bookings/step1/?service=<id>`
- [ ] Service combos hiển thị
- [ ] No results state hiển thị đúng

### Stylists Page (`/stylists/`)
- [ ] Danh sách stylists hiển thị
- [ ] Filter theo specialty hoạt động
- [ ] Sort (rating, experience) hoạt động
- [ ] Click vào stylist → `/stylists/<id>/`
- [ ] "Đặt lịch" button hoạt động

### Stylist Detail Page (`/stylists/<id>/`)
- [ ] Thông tin stylist hiển thị đầy đủ
- [ ] Statistics (bookings, reviews) đúng
- [ ] Services của stylist hiển thị
- [ ] Reviews hiển thị
- [ ] "Đặt lịch" button hoạt động
- [ ] "Yêu thích" button hoạt động (khi đã login)

### Promotions Page (`/promotions/`)
- [ ] Danh sách vouchers hiển thị
- [ ] Filter (all, for-new, for-loyal) hoạt động
- [ ] Voucher details đúng
- [ ] "Đặt lịch" với voucher code hoạt động
- [ ] Point rewards section hiển thị

---

## 2. 🔐 AUTHENTICATION

### Register (`/accounts/register/`)
- [ ] Form validation hoạt động:
  - [ ] Tên (required, min 2 chars)
  - [ ] SĐT (required, unique, 10 digits)
  - [ ] Email (optional, valid format, unique)
  - [ ] Mật khẩu (required, min 6 chars)
  - [ ] Xác nhận mật khẩu (match)
- [ ] Submit form thành công
- [ ] Tạo tài khoản → redirect về dashboard
- [ ] Session được tạo đúng
- [ ] Error messages hiển thị rõ ràng

### Login (`/accounts/login/`)
- [ ] Form validation hoạt động
- [ ] Login với SĐT + mật khẩu thành công
- [ ] Login sai thông tin → error message
- [ ] Session được tạo đúng
- [ ] Redirect về dashboard sau login
- [ ] "Quên mật khẩu" link hoạt động

### Forgot Password Flow
**Step 1:** `/accounts/forgot-password/`
- [ ] Nhập SĐT
- [ ] Gửi OTP thành công
- [ ] OTP được log ra console (hoặc gửi SMS)

**Step 2:** Verify OTP
- [ ] Nhập OTP đúng → tiếp tục
- [ ] Nhập OTP sai → error
- [ ] Resend OTP hoạt động
- [ ] Timer countdown hoạt động

**Step 3:** `/accounts/reset-password/`
- [ ] Nhập mật khẩu mới
- [ ] Xác nhận mật khẩu
- [ ] Submit thành công
- [ ] Redirect về login
- [ ] Login với mật khẩu mới OK

### Logout (`/accounts/logout/`)
- [ ] Logout thành công
- [ ] Session bị xóa
- [ ] Redirect về home
- [ ] Không thể access dashboard sau logout

---

## 3. 📅 BOOKING FLOW

### Step 1: Select Services (`/bookings/step1/`)
- [ ] ✅ **Page loads successfully** (Fixed!)
- [ ] Featured services hiển thị (top 6)
- [ ] All services hiển thị grouped by category
- [ ] Chọn service → thêm vào giỏ
- [ ] Số lượng service có thể thay đổi
- [ ] Xóa service khỏi giỏ hoạt động
- [ ] Tổng tiền tính đúng
- [ ] Button "Tiếp tục" khi có ít nhất 1 service
- [ ] Session lưu `booking_services`

**Test với URL parameters:**
- [ ] `/bookings/step1/?service=<id>` → auto select service
- [ ] `/bookings/step1/?voucher=<code>` → pre-fill voucher

### Step 2: Select Stylist (`/bookings/step2/`)
- [ ] Redirect về step1 nếu chưa chọn service
- [ ] Danh sách stylists hiển thị
- [ ] Stylists sorted by total bookings
- [ ] Average rating hiển thị
- [ ] Chọn stylist hoạt động
- [ ] "Để hệ thống chọn" option hoạt động
- [ ] Button "Quay lại" về step1
- [ ] Button "Tiếp tục" hoạt động
- [ ] Session lưu `booking_stylist`

**Test với URL parameters:**
- [ ] `/bookings/step2/?stylist=<id>` → auto select stylist

### Step 3: Select Date & Time (`/bookings/step3/`)
- [ ] Redirect về step2 nếu chưa chọn stylist
- [ ] Calendar hiển thị
- [ ] Chỉ cho chọn ngày >= hôm nay
- [ ] Click ngày → load time slots (AJAX)
- [ ] Time slots hiển thị đúng
  - [ ] Available slots enabled
  - [ ] Booked slots disabled
  - [ ] Past times disabled
- [ ] Chọn time slot hoạt động
- [ ] Ghi chú (optional) hoạt động
- [ ] Voucher input hoạt động
  - [ ] Validate voucher (AJAX)
  - [ ] Show discount amount
  - [ ] Error nếu voucher invalid
- [ ] Summary section hiển thị:
  - [ ] Selected services
  - [ ] Selected stylist
  - [ ] Date & time
  - [ ] Tạm tính
  - [ ] Giảm giá (nếu có)
  - [ ] Thành tiền
- [ ] Button "Quay lại" về step2
- [ ] Button "Tiếp tục" hoạt động
- [ ] Session lưu `booking_datetime`, `booking_voucher`

**Login Required:**
- [ ] Nếu chưa login → show login prompt
- [ ] Link "Đăng ký ngay" hoạt động

### Step 4: Confirm & Payment (`/bookings/step4/`)
- [ ] Redirect về step3 nếu chưa chọn datetime
- [ ] Booking summary đầy đủ:
  - [ ] Customer info
  - [ ] Services list
  - [ ] Stylist info
  - [ ] Date & time
  - [ ] Pricing breakdown
- [ ] Customer points hiển thị
- [ ] Sử dụng điểm hoạt động:
  - [ ] Input points
  - [ ] Validate số điểm hợp lệ
  - [ ] Tính discount từ points
  - [ ] Update thành tiền
- [ ] Payment method selection:
  - [ ] Tiền mặt
  - [ ] Thẻ
  - [ ] Chuyển khoản
- [ ] Terms & conditions checkbox
- [ ] Button "Quay lại" về step3
- [ ] Button "Xác nhận đặt lịch" hoạt động
  - [ ] Create booking (AJAX POST)
  - [ ] Redirect về success page

### Booking Success (`/bookings/success/`)
- [ ] Booking info hiển thị:
  - [ ] Booking ID
  - [ ] Date & time
  - [ ] Services
  - [ ] Stylist
  - [ ] Total amount
- [ ] Countdown to booking time
- [ ] Buttons hoạt động:
  - [ ] "Xem chi tiết" → dashboard
  - [ ] "Về trang chủ" → home
  - [ ] "Đặt lịch mới" (nếu chưa login)

---

## 4. 👤 CUSTOMER DASHBOARD

### Dashboard Overview (`/customer/dashboard/`)
- [ ] **Redirect nếu chưa login**
- [ ] Sidebar menu hoạt động
- [ ] User info hiển thị
- [ ] Points hiển thị
- [ ] Quick stats:
  - [ ] Upcoming bookings count
  - [ ] Completed bookings count
  - [ ] Total points
  - [ ] Available vouchers
- [ ] Upcoming bookings list:
  - [ ] Hiển thị 5 bookings gần nhất
  - [ ] Status badges đúng
  - [ ] Click vào booking → detail page
- [ ] "Đặt lịch mới" button hoạt động

### My Bookings (`/customer/bookings/`)
- [ ] List all upcoming & pending bookings
- [ ] Tabs hoạt động:
  - [ ] Tất cả
  - [ ] Chờ xác nhận
  - [ ] Đã xác nhận
  - [ ] Đã hủy
- [ ] Search hoạt động
- [ ] Filter by date range
- [ ] Pagination hoạt động
- [ ] Click vào booking → detail
- [ ] "Hủy lịch" button hoạt động
  - [ ] Confirmation dialog
  - [ ] POST request
  - [ ] Booking status updated

### Booking Detail (`/customer/bookings/<id>/`)
- [ ] Booking info đầy đủ
- [ ] Timeline hiển thị
- [ ] Services list
- [ ] Stylist info
- [ ] Payment info
- [ ] Action buttons:
  - [ ] "Hủy lịch" (nếu status = pending/confirmed)
  - [ ] "Đánh giá" (nếu status = completed)
  - [ ] "Tải hóa đơn" (nếu có - **chưa implement**)
- [ ] "Quay lại" button hoạt động

### Booking History (`/customer/history/`)
- [ ] List all completed & cancelled bookings
- [ ] Search hoạt động
- [ ] Filter by:
  - [ ] Date range
  - [ ] Status
  - [ ] Stylist
- [ ] Sort by date
- [ ] "Đánh giá" button (nếu chưa đánh giá)
- [ ] "Xem chi tiết" button

### Rewards & Points (`/customer/rewards/`)
- [ ] Current points hiển thị
- [ ] Points history:
  - [ ] Earned points
  - [ ] Used points
  - [ ] Date & description
- [ ] Available vouchers:
  - [ ] My vouchers
  - [ ] Public vouchers
  - [ ] Expiry date
  - [ ] Conditions
- [ ] Redeem rewards:
  - [ ] Gift list
  - [ ] Points required
  - [ ] "Đổi quà" button
  - [ ] Confirmation dialog
  - [ ] POST request
  - [ ] Points deducted
- [ ] "Sử dụng ngay" button → booking with voucher

### Profile (`/customer/profile/`)
- [ ] User info hiển thị
- [ ] Avatar upload hoạt động
- [ ] Edit profile form:
  - [ ] Họ tên
  - [ ] Email
  - [ ] Ngày sinh
  - [ ] Giới tính
  - [ ] Địa chỉ
- [ ] Submit form thành công
- [ ] Success message hiển thị
- [ ] Data updated in database
- [ ] "Đổi mật khẩu" link hoạt động
- [ ] "Xóa tài khoản" button (**chưa implement**)

### Change Password (`/customer/profile/change-password/`)
- [ ] Form validation:
  - [ ] Current password (required)
  - [ ] New password (required, min 6)
  - [ ] Confirm password (match)
- [ ] Verify current password đúng
- [ ] Submit form thành công
- [ ] Password updated
- [ ] Redirect về profile
- [ ] Login với password mới OK

### Favorite Stylists (`/customer/favorites/`)
- [ ] List all favorite stylists
- [ ] Stylist info hiển thị
- [ ] Rating & stats
- [ ] "Xóa khỏi yêu thích" button:
  - [ ] AJAX POST
  - [ ] Stylist removed from list
- [ ] "Xem chi tiết" → stylist detail
- [ ] "Đặt lịch" → booking with stylist
- [ ] Empty state nếu chưa có favorite
- [ ] "Khám phá stylist" button

### Review Booking (`/customer/bookings/<id>/review/`)
- [ ] **Chỉ cho access nếu booking completed**
- [ ] Booking info hiển thị
- [ ] Review form:
  - [ ] Rating service (1-5 stars)
  - [ ] Rating stylist (1-5 stars)
  - [ ] Comment (required, min 10 chars)
  - [ ] Photos upload (optional, max 3)
  - [ ] Tags (chuyên nghiệp, thân thiện, sạch sẽ, đúng giờ)
- [ ] Submit form thành công
- [ ] Review saved
- [ ] Redirect về booking detail
- [ ] "Quay lại" button hoạt động

---

## 5. 🔍 ADDITIONAL CHECKS

### Navigation
- [ ] Navbar fixed on scroll
- [ ] Mobile menu toggle hoạt động
- [ ] All navbar links hoạt động
- [ ] User dropdown menu hoạt động
- [ ] Logo click → home

### Footer
- [ ] Company info hiển thị
- [ ] Quick links hoạt động
- [ ] Social media icons
- [ ] Copyright notice

### Search & Filter
- [ ] Search input hoạt động (nếu có)
- [ ] Filter dropdowns hoạt động
- [ ] Results update correctly
- [ ] Clear filters hoạt động

### Responsive Design
- [ ] Mobile (< 768px) OK
- [ ] Tablet (768px - 991px) OK
- [ ] Desktop (>= 992px) OK
- [ ] Touch events hoạt động on mobile

### Performance
- [ ] Page load < 3s
- [ ] Images lazy load
- [ ] No console errors
- [ ] No 404 errors

### Security
- [ ] CSRF token in all POST forms
- [ ] Session expires after logout
- [ ] Protected pages require login
- [ ] SQL injection prevention
- [ ] XSS prevention

---

## 6. 🐛 ERROR SCENARIOS

### Test Error Handling:

**Invalid URLs:**
- [ ] `/invalid-url/` → 404 page
- [ ] `/bookings/step1/999999/` → 404

**Unauthorized Access:**
- [ ] Access `/customer/dashboard/` without login → redirect to login
- [ ] Access `/admin/` as customer → 403 or redirect

**Invalid Data:**
- [ ] Submit form với empty required fields → validation errors
- [ ] Submit form với invalid email → validation error
- [ ] Upload file > max size → error message

**Network Errors:**
- [ ] AJAX timeout → error message
- [ ] Server error → 500 page

**Business Logic:**
- [ ] Book time slot đã full → error
- [ ] Sử dụng voucher expired → error
- [ ] Hủy booking đã check-in → error
- [ ] Đổi quà với points không đủ → error

---

## 7. 📊 DATABASE CHECKS

### After Testing, Verify:

**NguoiDung:**
- [ ] New customers created correctly
- [ ] Password hashed (MD5)
- [ ] Points accumulated correctly
- [ ] Profile updates saved

**DatLich:**
- [ ] Bookings created với đầy đủ thông tin
- [ ] Status transitions correct (pending → confirmed → completed)
- [ ] Timestamps accurate
- [ ] Soft delete (da_xoa) hoạt động

**DichVuDatLich:**
- [ ] Services linked to booking correctly
- [ ] Quantities correct
- [ ] Prices saved correctly

**DanhGia:**
- [ ] Reviews created với đầy đủ fields
- [ ] Ratings (1-5) correct
- [ ] Photos uploaded correctly
- [ ] Tags saved

**StylistYeuThich:**
- [ ] Favorites added/removed correctly
- [ ] No duplicates

**VoucherKhachHang:**
- [ ] Vouchers assigned to customers
- [ ] Usage tracked
- [ ] Expiry dates checked

**QuaTangDiem:**
- [ ] Gifts redeemed
- [ ] Points deducted
- [ ] Transaction logged

---

## 8. 🎯 PRIORITY LEVELS

### 🔴 CRITICAL (Must work):
1. Home page loads
2. Register & login
3. Booking flow (all 4 steps)
4. Customer dashboard

### 🟡 IMPORTANT (Should work):
1. Services & stylists pages
2. Profile management
3. Bookings management
4. Reviews

### 🟢 NICE TO HAVE:
1. Favorites
2. Rewards
3. Promotions
4. Export features

---

## 9. ✅ SIGN-OFF CHECKLIST

### Before Deploy:

- [ ] All CRITICAL tests pass
- [ ] All IMPORTANT tests pass
- [ ] No console errors
- [ ] No 500 errors
- [ ] No SQL errors
- [ ] Responsive design OK
- [ ] Cross-browser tested (Chrome, Firefox, Safari, Edge)
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] Debug mode OFF in production

---

## 📝 BUG REPORT TEMPLATE

Nếu phát hiện lỗi, ghi chú theo format:

```
## BUG: [Short description]

**URL:** http://...
**Steps to reproduce:**
1. Go to ...
2. Click on ...
3. Enter ...
4. See error

**Expected:** Should do X
**Actual:** Does Y instead

**Error message:** [Copy error message]
**Console errors:** [Copy console.log]
**Screenshot:** [If applicable]

**Priority:** 🔴 Critical / 🟡 Important / 🟢 Low
```

---

## 🎉 SUCCESS CRITERIA

### Website được coi là "HOÀN HẢO" khi:

✅ Tất cả public pages load thành công  
✅ Authentication flow hoạt động 100%  
✅ Booking flow hoàn chỉnh từ step1 → success  
✅ Dashboard pages hiển thị đúng data  
✅ AJAX calls hoạt động (voucher, time slots, favorites)  
✅ Forms validation chính xác  
✅ Database operations đúng  
✅ Responsive design OK trên mọi devices  
✅ Không có errors trong console  
✅ Performance tốt (load < 3s)  

---

**Created:** October 13, 2025  
**Status:** 📋 Ready for Testing  
**Next:** Run through all test cases and report results!
