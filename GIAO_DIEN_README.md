# HỆ THỐNG QUẢN LÝ BARBERSHOP - GIAO DIỆN ADMIN & STAFF

## 📋 TỔNG QUAN

Hệ thống giao diện hoàn chỉnh cho **Chủ tiệm (Admin)** và **Nhân viên (Staff/Stylist)** của Barbershop Hoàng Gia.

### ✨ Công nghệ sử dụng
- **Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **Charts**: Chart.js 4.4.0
- **JavaScript**: jQuery 3.7.0
- **Template Engine**: Django Templates

---

## 📁 CẤU TRÚC FILE ĐÃ TẠO

```
templates/
├── base.html                    # Template gốc với CSS/JS chung
├── admin/
│   ├── dashboard.html          # ✅ Dashboard Admin
│   ├── staff.html              # ✅ Quản lý Nhân viên
│   ├── customers.html          # 🔜 Quản lý Khách hàng
│   ├── services.html           # 🔜 Quản lý Dịch vụ
│   ├── bookings.html           # 🔜 Quản lý Booking
│   ├── invoices.html           # 🔜 Quản lý Hóa đơn
│   ├── pos-report.html         # 🔜 Báo cáo POS
│   ├── promotions.html         # 🔜 Quản lý Khuyến mãi
│   ├── reports.html            # 🔜 Báo cáo Thống kê
│   ├── work-schedule.html      # 🔜 Lịch làm việc
│   ├── reviews.html            # 🔜 Quản lý Đánh giá
│   ├── settings.html           # 🔜 Cài đặt Hệ thống
│   └── content.html            # 🔜 Quản lý Nội dung
│
└── staff/
    ├── dashboard.html          # ✅ Dashboard Nhân viên
    ├── pos.html                # ✅ POS - Thanh toán (QUAN TRỌNG)
    ├── schedule.html           # 🔜 Lịch làm việc
    ├── register-shift.html     # 🔜 Đăng ký ca làm
    ├── today-bookings.html     # 🔜 Lịch hẹn hôm nay
    ├── my-customers.html       # 🔜 Khách hàng của tôi
    ├── revenue.html            # 🔜 Doanh thu cá nhân
    └── profile.html            # 🔜 Thông tin cá nhân
```

**Chú thích:**
- ✅ = Đã tạo hoàn chỉnh
- 🔜 = Chưa tạo (cần tạo tiếp)

---

## 🎨 CÁC FILE ĐÃ TẠO CHI TIẾT

### 1. **base.html** - Template gốc
**Chức năng:**
- CSS tùy chỉnh với color scheme chuyên nghiệp
- Sidebar navigation styles
- Card, table, button components
- Responsive design
- Integration Bootstrap 5, Font Awesome, Chart.js

**Đặc điểm:**
- Color palette: `#8b4513` (primary - nâu gỗ), `#d2691e` (secondary)
- Gradient backgrounds cho sidebar
- Hover effects mượt mà
- Badge notifications
- Mobile responsive

---

### 2. **admin/dashboard.html** - Dashboard Admin
**Chức năng:**
- **Statistics Cards (4 thẻ):**
  - Doanh thu hôm nay
  - Số booking hôm nay  
  - Khách hàng mới tháng này
  - Nhân viên đang làm
  
- **Biểu đồ:**
  - Revenue Chart: Doanh thu 7 ngày (Line chart)
  - Services Chart: Top 3 dịch vụ (Doughnut chart)
  
- **Danh sách chờ xử lý:**
  - Booking chờ xác nhận
  - Yêu cầu nghỉ phép

**Menu Sidebar Admin:**
1. Tổng quan
2. Quản lý Nhân viên
3. Quản lý Khách hàng
4. Quản lý Dịch vụ
5. Quản lý Booking
6. Quản lý Hóa đơn
7. Khuyến mãi & Voucher
8. Báo cáo Thống kê
9. Báo cáo POS
10. Lịch làm việc
11. Quản lý Đánh giá
12. Nội dung Website
13. Cài đặt Hệ thống

---

### 3. **admin/staff.html** - Quản lý Nhân viên
**Chức năng:**
- **Filter/Search:**
  - Tìm kiếm theo tên, SĐT, email
  - Filter theo trạng thái (đang làm/nghỉ việc)
  - Sắp xếp (tên, đánh giá, doanh thu)

- **Bảng danh sách:**
  - Avatar + thông tin nhân viên
  - Liên hệ (email, SĐT)
  - Chuyên môn
  - Kinh nghiệm (số năm)
  - Đánh giá trung bình (sao)
  - Lượt phục vụ
  - Trạng thái
  - Hành động (Xem/Sửa/Xóa)

- **Modal thêm nhân viên:**
  - Form đầy đủ: Họ tên, SĐT, Email, Mật khẩu
  - Ngày sinh, Giới tính
  - Chuyên môn, Kinh nghiệm, Chứng chỉ
  - Mô tả, Upload ảnh đại diện

**Tính năng:**
- Pagination
- Inline editing
- Soft delete
- Reset password
- View detailed stats per staff

---

### 4. **staff/dashboard.html** - Dashboard Nhân viên
**Chức năng:**
- **Quick Stats (4 thẻ):**
  - Ca làm hôm nay (sáng/chiều/tối)
  - Số lịch hẹn hôm nay
  - Doanh thu tháng này
  - Đánh giá trung bình

- **Lịch hẹn tiếp theo:**
  - Hiển thị booking sắp tới nhất
  - Mã booking, khách hàng, thời gian
  - Dịch vụ, ghi chú
  - Nút Check-in nhanh

- **Hiệu suất tháng này:**
  - Số lượt phục vụ
  - Tổng doanh thu
  - Trung bình/booking
  - Tỷ lệ khách quay lại
  - Bar chart theo tuần

- **Lịch trình hôm nay:**
  - Timeline các booking
  - Trạng thái real-time
  - Quick actions (Check-in, Hoàn thành)

**Menu Sidebar Staff:**
1. Tổng quan
2. **POS - Thanh toán** ⭐
3. Lịch làm việc
4. Đăng ký ca làm
5. Lịch hẹn hôm nay
6. Khách hàng của tôi
7. Doanh thu cá nhân
8. Thông tin cá nhân

---

### 5. **staff/pos.html** - POS System (Hệ thống Thanh toán) ⭐⭐⭐
**ĐÂY LÀ TÍNH NĂNG CỐT LÕI NHẤT!**

#### Layout: 2 cột (Responsive)
**Cột Trái (60%) - Thông tin KH & Dịch vụ:**

**Tab 1: Khách vãng lai (Walk-in)**
- Input: Tên khách, SĐT
- Nhanh chóng, đơn giản

**Tab 2: Khách có tài khoản**
- Search bar: Tìm theo SĐT/Tên
- Hiển thị info box sau khi tìm:
  - Avatar, tên, SĐT
  - Điểm hiện có
  - Lịch sử (số lần đến)
  - Ghi chú của stylist (nếu có)

**Tab 3: Từ booking**
- Input: Mã booking hoặc dropdown "Booking hôm nay"
- Auto-load toàn bộ thông tin:
  - Thông tin khách
  - Dịch vụ đã đặt (pre-checked)
  - Stylist, giờ hẹn, voucher
- Cho phép thêm/bớt dịch vụ

**Chọn dịch vụ:**
- Grid view (6 cột responsive)
- Mỗi service card:
  - Icon
  - Tên dịch vụ
  - Giá
  - Click để thêm vào cart
- Search bar tìm nhanh dịch vụ

**Chọn Stylist:**
- Dropdown list
- Mặc định: nhân viên hiện tại
- Có thể đổi sang stylist khác

---

**Cột Phải (40%) - Giỏ hàng & Thanh toán:**

**Cart (Giỏ hàng):**
- Danh sách dịch vụ đã chọn
- Mỗi item:
  - Tên dịch vụ + Giá
  - Quantity controls (+/-)
  - Thành tiền
  - Nút xóa
- Empty state khi chưa có dịch vụ

**Áp dụng giảm giá (collapsible):**
- **Voucher:** Dropdown chọn voucher của khách
  - Tự động load nếu khách có tài khoản
  - Hiển thị: Mã, tên, giá trị, điều kiện
  - Auto-calculate giảm giá
  
- **Điểm tích lũy:**
  - Hiển thị số điểm hiện có
  - Input: Số điểm muốn dùng
  - Quy đổi: 1 điểm = 1,000đ
  - Max = min(số điểm có, tổng tiền)

**Tổng quan đơn hàng:**
```
Tạm tính:      150,000đ
Giảm giá:      -20,000đ
─────────────────────
Tổng cộng:     130,000đ
```

**Phương thức thanh toán (Radio buttons):**
- ⭕ Tiền mặt
  - Hiện thêm input "Khách đưa"
  - Auto tính "Tiền thừa"
- ⭕ Chuyển khoản
- ⭕ Ví điện tử
- ⭕ Thẻ

**Action Buttons:**
- **THANH TOÁN** (lớn, nổi bật - primary button)
- Lưu tạm (secondary)
- Hủy (danger)

---

#### Tính năng JavaScript POS:
1. **Cart Management:**
   - `addService(id, name, price)` - Thêm dịch vụ
   - `updateCart()` - Cập nhật giỏ hàng
   - `increaseQty(id)` / `decreaseQty(id)` - Điều chỉnh số lượng
   - `removeItem(id)` - Xóa item
   - `updateTotals()` - Tính tổng

2. **Discount Calculation:**
   - Apply voucher
   - Apply points
   - Real-time update totals

3. **Payment Processing:**
   - `calculateChange()` - Tính tiền thừa (nếu tiền mặt)
   - `processPayment()` - Xử lý thanh toán
   - Validation customer info
   - Confirm dialog
   - Success → Print invoice → Reset

4. **Customer Search:**
   - `searchCustomer()` - AJAX search
   - Display customer info box
   - Load customer's vouchers & points

5. **Booking Load:**
   - `loadBooking()` - AJAX load booking data
   - `selectBooking(code)` - Chọn từ dropdown
   - Pre-fill services, customer, voucher

6. **Keyboard Shortcuts:**
   - `F9` → Thanh toán
   - `Esc` → Clear/Cancel
   - `F1` → Focus search khách
   - `F2` → Focus search dịch vụ

7. **Other Features:**
   - `viewHistory()` - Xem lịch sử giao dịch
   - `clearAll()` - Reset form
   - `saveDraft()` - Lưu tạm (nếu cần)

---

#### Xử lý Backend sau khi thanh toán (Pseudo-code):

```python
def process_payment(request):
    # 1. Lấy data từ form
    customer_info = request.POST.get('customer_info')
    service_ids = request.POST.getlist('services')
    stylist_id = request.POST.get('stylist_id')
    voucher_id = request.POST.get('voucher_id')
    points_used = request.POST.get('points_used', 0)
    payment_method = request.POST.get('payment_method')
    total_amount = request.POST.get('total_amount')
    booking_id = request.POST.get('booking_id')  # Nếu từ booking
    
    # 2. Tạo Invoice
    invoice = Invoice.objects.create(
        invoice_number=generate_invoice_number(),
        customer_id=customer_info.get('id') if customer_info else None,
        customer_name=customer_info.get('name'),
        customer_phone=customer_info.get('phone'),
        stylist_id=stylist_id,
        subtotal=subtotal,
        discount_amount=discount,
        final_amount=total_amount,
        payment_method=payment_method,
        created_by=request.user,
        paid_at=now()
    )
    
    # 3. Tạo InvoiceItems
    for service_id in service_ids:
        service = Service.objects.get(id=service_id)
        InvoiceItem.objects.create(
            invoice=invoice,
            service=service,
            name=service.name,
            price=service.price,
            quantity=1,
            total=service.price
        )
    
    # 4. Xử lý Booking (nếu từ booking)
    if booking_id:
        booking = Booking.objects.get(id=booking_id)
        booking.status = 'completed'
        booking.completed_at = now()
        booking.invoice = invoice
        booking.save()
    else:
        # Tạo booking mới type="walk_in" để tracking
        Booking.objects.create(
            code=generate_booking_code(),
            customer_id=customer_info.get('id'),
            stylist_id=stylist_id,
            booking_date=now().date(),
            booking_time=now().time(),
            type='walk_in',
            status='completed',
            completed_at=now(),
            invoice=invoice
        )
    
    # 5. Xử lý nếu khách có tài khoản
    if customer_info.get('id'):
        customer = User.objects.get(id=customer_info['id'])
        
        # 5a. Dùng voucher → mark as used
        if voucher_id:
            voucher = CustomerVoucher.objects.get(id=voucher_id)
            voucher.is_used = True
            voucher.invoice = invoice
            voucher.used_at = now()
            voucher.save()
        
        # 5b. Dùng điểm → trừ điểm
        if points_used > 0:
            customer.points -= points_used
            PointTransaction.objects.create(
                customer=customer,
                points=-points_used,
                type='redeem',
                description=f'Sử dụng điểm cho hóa đơn {invoice.invoice_number}',
                invoice=invoice
            )
        
        # 5c. Cộng điểm mới (1000đ = 1 điểm)
        new_points = int(total_amount / 1000)
        customer.points += new_points
        customer.save()
        
        PointTransaction.objects.create(
            customer=customer,
            points=new_points,
            type='earn',
            description=f'Cộng điểm từ hóa đơn {invoice.invoice_number}',
            invoice=invoice
        )
    
    # 6. Update stylist revenue
    stylist = User.objects.get(id=stylist_id)
    stylist_info = stylist.staff_info
    stylist_info.total_served += 1
    stylist_info.save()
    
    # 7. Gửi email/SMS hóa đơn (nếu có)
    if customer_info.get('email'):
        send_invoice_email(customer_info['email'], invoice)
    
    # 8. Return success
    return JsonResponse({
        'success': True,
        'invoice_id': invoice.id,
        'invoice_number': invoice.invoice_number,
        'print_url': f'/staff/pos/print/{invoice.id}',
        'new_points': new_points if customer_info.get('id') else 0
    })
```

---

## 🎯 CÁC TÍNH NĂNG NỔI BẬT

### 1. **POS System (staff/pos.html)**
- ✅ 3 luồng thanh toán: Walk-in, Registered Customer, From Booking
- ✅ Grid dịch vụ trực quan, click để thêm
- ✅ Cart với quantity controls
- ✅ Áp dụng voucher & điểm tự động
- ✅ Multi payment methods
- ✅ Auto calculate change (tiền thừa)
- ✅ Keyboard shortcuts
- ✅ Real-time totals update
- ✅ Responsive 2-column layout

### 2. **Admin Dashboard**
- ✅ 4 stat cards với icons gradient
- ✅ 2 charts (Line + Doughnut) với Chart.js
- ✅ Pending actions tables
- ✅ Quick approve/reject buttons

### 3. **Staff Management**
- ✅ Comprehensive filter & search
- ✅ Avatar integration (ui-avatars API)
- ✅ Modal add staff với full form
- ✅ Rating display with stars
- ✅ Action buttons (View/Edit/Delete)

### 4. **Staff Dashboard**
- ✅ Next booking highlight box
- ✅ Performance metrics
- ✅ Today's schedule table
- ✅ Bar chart hiệu suất
- ✅ Quick check-in buttons

---

## 🚀 HƯỚNG DẪN SỬ DỤNG

### 1. Cài đặt Dependencies
Các thư viện đã được link từ CDN trong `base.html`:
- Bootstrap 5.3.0
- Font Awesome 6.4.0
- Chart.js 4.4.0
- jQuery 3.7.0

**Không cần cài đặt thêm gì!**

### 2. Chạy server Django
```bash
cd d:\Project\WebsiteHotTocNam
python manage.py runserver
```

### 3. Truy cập các trang

**Admin:**
- Dashboard: `http://localhost:8000/admin/dashboard`
- Quản lý Nhân viên: `http://localhost:8000/admin/staff`

**Staff:**
- Dashboard: `http://localhost:8000/staff/dashboard`
- **POS:** `http://localhost:8000/staff/pos` ⭐

---

## 📝 DANH SÁCH CÁC TRANG CẦN TẠO TIẾP

### Admin (còn 11 trang):
1. ⬜ customers.html - Quản lý Khách hàng
2. ⬜ services.html - Quản lý Dịch vụ
3. ⬜ bookings.html - Quản lý Booking
4. ⬜ invoices.html - Quản lý Hóa đơn
5. ⬜ pos-report.html - Báo cáo POS
6. ⬜ promotions.html - Khuyến mãi
7. ⬜ reports.html - Báo cáo Thống kê
8. ⬜ work-schedule.html - Lịch làm việc
9. ⬜ reviews.html - Đánh giá
10. ⬜ settings.html - Cài đặt
11. ⬜ content.html - Nội dung Website

### Staff (còn 6 trang):
1. ⬜ schedule.html - Lịch làm việc
2. ⬜ register-shift.html - Đăng ký ca
3. ⬜ today-bookings.html - Lịch hẹn hôm nay
4. ⬜ my-customers.html - Khách hàng của tôi
5. ⬜ revenue.html - Doanh thu cá nhân
6. ⬜ profile.html - Thông tin cá nhân

---

## 💡 GỢI Ý PHÁT TRIỂN TIẾP

### Priority 1 (Quan trọng nhất):
1. **today-bookings.html** (Staff) - Để check-in khách
2. **invoices.html** (Admin) - Quản lý hóa đơn từ POS
3. **bookings.html** (Admin) - Quản lý booking
4. **work-schedule.html** (Admin) - Phân ca làm việc

### Priority 2:
1. **customers.html** (Admin)
2. **services.html** (Admin)
3. **my-customers.html** (Staff)
4. **revenue.html** (Staff)

### Priority 3:
1. **pos-report.html** (Admin)
2. **reports.html** (Admin)
3. **promotions.html** (Admin)
4. **reviews.html** (Admin)
5. **settings.html** (Admin)

---

## 🎨 MÀU SẮC & THIẾT KẾ

### Color Palette:
- **Primary**: `#8b4513` (Nâu gỗ)
- **Secondary**: `#d2691e` (Nâu sáng)
- **Dark**: `#2c3e50` (Xám đen)
- **Light BG**: `#f8f9fa` (Xám nhạt)

### Gradient cho Icons:
- Revenue: Purple gradient `#667eea → #764ba2`
- Bookings: Pink gradient `#f093fb → #f5576c`
- Customers: Blue gradient `#4facfe → #00f2fe`
- Staff: Green gradient `#43e97b → #38f9d7`

### Typography:
- Font: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- Responsive font sizes
- Bold for important numbers

---

## 🔧 TÙYBIẾN VÀ MỞ RỘNG

### Thay đổi màu sắc:
Sửa trong `base.html`:
```css
:root {
    --primary-color: #8b4513;   /* Thay màu chính */
    --secondary-color: #d2691e; /* Thay màu phụ */
    --dark-color: #2c3e50;      /* Thay màu tối */
}
```

### Thêm menu mới:
Trong sidebar, thêm:
```html
<li class="nav-item">
    <a class="nav-link" href="/your-url">
        <i class="fas fa-icon-name"></i> Tên menu
    </a>
</li>
```

### Tích hợp Backend Django:
1. Tạo views trong `views.py`
2. Thêm URLs trong `urls.py`
3. Pass context data vào template
4. Replace data tĩnh bằng `{{ variable }}`

---

## 📞 HỖ TRỢ

Nếu cần:
- Tạo thêm các trang còn lại
- Tích hợp với Django backend
- Thêm tính năng mới
- Sửa lỗi hoặc tối ưu

Hãy cho tôi biết!

---

## ✅ CHECKLIST HOÀN THÀNH

- [x] Base template với CSS/JS
- [x] Admin Dashboard
- [x] Admin Staff Management
- [x] Staff Dashboard
- [x] **Staff POS System** ⭐⭐⭐
- [ ] 11 trang Admin còn lại
- [ ] 6 trang Staff còn lại
- [ ] Integration với Django models
- [ ] AJAX implementations
- [ ] Form validations
- [ ] Print invoice feature
- [ ] Export Excel/PDF

---

**Ngày tạo:** 01/10/2025
**Version:** 1.0
**Tác giả:** GitHub Copilot
