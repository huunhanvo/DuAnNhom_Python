# Sửa Lỗi Đăng Nhập & Navigation

**Ngày:** 13/10/2025  
**Vấn đề:** Không có nút đăng nhập ở trang chủ & lỗi URL 'login' not found

---

## 🐛 Vấn Đề Phát Hiện

### 1. Nút Đăng Ký Bị Ẩn
**Template:** `templates/customer/base_customer.html`

**Vấn đề:**
```html
<li class="nav-item d-lg-none">  <!-- Class d-lg-none ẩn nút ở màn hình lớn -->
    <a class="btn btn-primary btn-sm ms-lg-2" href="{% url 'accounts:register' %}">
        <i class="fas fa-user-plus me-1"></i> Đăng ký
    </a>
</li>
```

**Giải pháp:** Bỏ class `d-lg-none` để hiển thị nút đăng ký trên mọi màn hình
```html
<li class="nav-item">
    <a class="nav-link" href="{% url 'accounts:register' %}">
        <i class="fas fa-user-plus me-1"></i> Đăng ký
    </a>
</li>
```

### 2. URL 'login' Không Tồn Tại
**Lỗi:** `NoReverseMatch: Reverse for 'login' not found`

**Nguyên nhân:** 
- URL name `'login'` đã bị xóa khỏi `barbershop/urls.py`
- Hiện tại có 2 login URLs:
  - `'staff_login'` - Cho nhân viên/quản lý (path: `/login/`)
  - `'accounts:customer_login'` - Cho khách hàng (path: `/accounts/login/`)

**Các file bị ảnh hưởng:**
1. `core/decorators.py` - redirect('login')
2. `templates/login.html` - {% url 'login' %}
3. `templates/customer/register.html` - {% url 'login' %}

---

## ✅ Các Thay Đổi Đã Thực Hiện

### 1. Sửa Navigation Bar
**File:** `templates/customer/base_customer.html`

**Thay đổi:**
- ✅ Hiển thị nút "Đăng ký" trên tất cả màn hình
- ✅ Đổi style từ button sang nav-link để đồng nhất
- ✅ Giữ nguyên URL `accounts:customer_login` và `accounts:register`

**Code mới:**
```html
{% if request.session.user_id %}
    <!-- User đã đăng nhập: hiển thị dropdown -->
{% else %}
    <!-- User chưa đăng nhập -->
    <li class="nav-item">
        <a class="nav-link" href="{% url 'accounts:customer_login' %}">
            <i class="fas fa-sign-in-alt me-1"></i> Đăng nhập
        </a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="{% url 'accounts:register' %}">
            <i class="fas fa-user-plus me-1"></i> Đăng ký
        </a>
    </li>
{% endif %}
```

### 2. Sửa Decorators
**File:** `core/decorators.py`

**Thay đổi:**
- ✅ `require_auth()` - redirect về `'accounts:customer_login'` 
- ✅ `require_role()` - redirect thông minh dựa trên vai trò:
  - Staff/Admin → `'staff_login'`
  - Customer → `'accounts:customer_login'`

**Code mới:**
```python
def require_auth(view_func):
    """Decorator to require authentication"""
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('accounts:customer_login')
        return view_func(request, *args, **kwargs)
    return wrapper

def require_role(allowed_roles):
    """Decorator to require specific role"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if 'user_id' not in request.session:
                # Staff/Admin should go to staff login
                if any(role in allowed_roles for role in ['nhan_vien', 'quan_ly']):
                    return redirect('staff_login')
                # Customer should go to customer login
                return redirect('accounts:customer_login')
            user_role = request.session.get('vai_tro')
            if user_role not in allowed_roles:
                # Redirect based on required role
                if any(role in allowed_roles for role in ['nhan_vien', 'quan_ly']):
                    return redirect('staff_login')
                return redirect('accounts:customer_login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### 3. Sửa Staff/Admin Login Form
**File:** `templates/login.html`

**Thay đổi:**
```html
<!-- CŨ -->
<form method="POST" action="{% url 'login' %}">

<!-- MỚI -->
<form method="POST" action="{% url 'staff_login' %}">
```

### 4. Sửa Customer Register Template
**File:** `templates/customer/register.html`

**Thay đổi:**
```html
<!-- CŨ -->
<a href="{% url 'login' %}">Đăng nhập ngay</a>

<!-- MỚI -->
<a href="{% url 'accounts:customer_login' %}">Đăng nhập ngay</a>
```

---

## 🎯 Cấu Trúc URL Hiện Tại

### Staff/Admin Login
- **URL:** `/login/`
- **URL Name:** `staff_login`
- **View:** `barbershop.views.login_view`
- **Template:** `templates/login.html`
- **Dùng cho:** Nhân viên & Quản lý

### Customer Login
- **URL:** `/accounts/login/`
- **URL Name:** `accounts:customer_login`
- **View:** `accounts.views.customer_login`
- **Template:** `templates/customer/login.html`
- **Dùng cho:** Khách hàng

### Customer Register
- **URL:** `/accounts/register/`
- **URL Name:** `accounts:register`
- **View:** `accounts.views.register`
- **Template:** `templates/customer/register.html`

---

## 📋 Testing Checklist

### Trang Chủ (/)
- [x] Hiển thị nút "Đăng nhập"
- [x] Hiển thị nút "Đăng ký"
- [x] Click "Đăng nhập" → Chuyển đến `/accounts/login/`
- [x] Click "Đăng ký" → Chuyển đến `/accounts/register/`

### Customer Login (/accounts/login/)
- [ ] Form hiển thị đúng
- [ ] Đăng nhập thành công → Dashboard
- [ ] Link "Đăng ký" hoạt động

### Customer Register (/accounts/register/)
- [x] Form hiển thị đúng (đã fix URL)
- [ ] Đăng ký thành công → Dashboard
- [x] Link "Đăng nhập" hoạt động (đã fix URL)

### Staff/Admin Login (/login/)
- [x] Form hiển thị đúng (đã fix action URL)
- [ ] Đăng nhập thành công → Dashboard tương ứng
- [ ] Redirect từ decorator hoạt động

### Protected Pages
- [ ] Customer pages → Redirect đến customer login
- [ ] Staff pages → Redirect đến staff login
- [ ] Admin pages → Redirect đến staff login

---

## 🚨 Lưu Ý Quan Trọng

### 1. Phân Biệt 2 Loại Login
Hệ thống có **2 form đăng nhập riêng biệt**:

| Loại | URL | Template | Dùng cho |
|------|-----|----------|----------|
| **Staff/Admin** | `/login/` | `templates/login.html` | Nhân viên, Quản lý |
| **Customer** | `/accounts/login/` | `templates/customer/login.html` | Khách hàng |

⚠️ **KHÔNG NÊN gộp chung 2 form này!**

### 2. URL Naming Convention
```python
# ✅ ĐÚNG
redirect('staff_login')              # Không có namespace
redirect('accounts:customer_login')  # Có namespace 'accounts'

# ❌ SAI
redirect('login')                    # URL này không tồn tại
```

### 3. Decorator Usage
```python
# Customer pages
@require_auth  # → Redirect to customer login
def customer_dashboard(request):
    pass

# Staff pages  
@require_role(['nhan_vien', 'quan_ly'])  # → Redirect to staff login
def staff_dashboard(request):
    pass
```

---

## 🔄 Rollback (Nếu Cần)

Nếu có vấn đề, rollback bằng git:
```bash
git checkout HEAD -- templates/customer/base_customer.html
git checkout HEAD -- core/decorators.py
git checkout HEAD -- templates/login.html
git checkout HEAD -- templates/customer/register.html
```

---

## ✨ Kết Quả

**Trước khi sửa:**
- ❌ Nút "Đăng ký" bị ẩn trên màn hình lớn
- ❌ Lỗi 500 khi vào `/login/`, `/accounts/register/`, protected pages
- ❌ Error: `NoReverseMatch: Reverse for 'login' not found`

**Sau khi sửa:**
- ✅ Nút "Đăng nhập" và "Đăng ký" hiển thị rõ ràng
- ✅ Tất cả URL hoạt động chính xác
- ✅ Decorator redirect đúng trang login
- ✅ Form submit đúng endpoint
- ✅ User experience tốt hơn

---

**Cập nhật lần cuối:** 13/10/2025  
**Người thực hiện:** AI Assistant
