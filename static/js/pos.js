// POS System JavaScript
let cart = [];
let subtotal = 0;
let discount = 0;
let selectedCustomer = null;

// Add service to cart
function addService(id, name, price) {
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    
    updateCart();
}

// Update cart display
function updateCart() {
    const cartEl = document.getElementById('cart');
    
    if (cart.length === 0) {
        cartEl.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-shopping-cart fa-3x mb-3"></i>
                <div>Chưa có dịch vụ nào</div>
            </div>
        `;
        subtotal = 0;
    } else {
        let html = '';
        subtotal = 0;
        
        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            subtotal += itemTotal;
            
            html += `
                <div class="cart-item">
                    <div>
                        <div class="fw-bold">${item.name}</div>
                        <small class="text-muted">${item.price.toLocaleString('vi-VN')}đ</small>
                    </div>
                    <div class="d-flex align-items-center gap-3">
                        <div class="quantity-control">
                            <button class="btn btn-sm btn-outline-secondary" onclick="decreaseQty(${item.id})">
                                <i class="fas fa-minus"></i>
                            </button>
                            <span class="fw-bold">${item.quantity}</span>
                            <button class="btn btn-sm btn-outline-secondary" onclick="increaseQty(${item.id})">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                        <div class="fw-bold">${itemTotal.toLocaleString('vi-VN')}đ</div>
                        <button class="btn btn-sm btn-outline-danger" onclick="removeItem(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        });
        
        cartEl.innerHTML = html;
    }
    
    updateTotals();
}

// Quantity controls
function increaseQty(id) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.quantity += 1;
        updateCart();
    }
}

function decreaseQty(id) {
    const item = cart.find(i => i.id === id);
    if (item && item.quantity > 1) {
        item.quantity -= 1;
        updateCart();
    }
}

function removeItem(id) {
    cart = cart.filter(i => i.id !== id);
    updateCart();
}

// Calculate discount
function calculateDiscount() {
    discount = 0;
    
    // Apply voucher
    const voucherSelect = document.getElementById('voucher');
    if (voucherSelect && voucherSelect.value) {
        const option = voucherSelect.options[voucherSelect.selectedIndex];
        const discountType = option.getAttribute('data-type');
        const discountValue = parseInt(option.getAttribute('data-value'));
        
        if (discountType === 'tien') {
            discount += discountValue;
        } else if (discountType === 'phan_tram') {
            discount += Math.floor(subtotal * discountValue / 100);
        }
    }
    
    // Apply points (1 point = 1,000 VND)
    const pointsInput = document.getElementById('points-use');
    if (pointsInput && pointsInput.value) {
        const pointsUsed = parseInt(pointsInput.value) || 0;
        discount += pointsUsed * 1000;
    }
    
    updateTotals();
}

// Update totals
function updateTotals() {
    document.getElementById('subtotal').textContent = subtotal.toLocaleString('vi-VN') + 'đ';
    document.getElementById('discount').textContent = '-' + discount.toLocaleString('vi-VN') + 'đ';
    const total = Math.max(0, subtotal - discount);
    document.getElementById('total').textContent = total.toLocaleString('vi-VN') + 'đ';
}

// Calculate change for cash payment
function calculateChange() {
    const total = subtotal - discount;
    const given = parseInt(document.getElementById('cash-given').value) || 0;
    const change = given - total;
    
    document.getElementById('change').value = change > 0 ? change.toLocaleString('vi-VN') + 'đ' : '0đ';
}

// Search customer
function searchCustomer() {
    const query = document.getElementById('search-customer').value.trim();
    
    if (!query) {
        alert('Vui lòng nhập số điện thoại hoặc tên khách hàng');
        return;
    }
    
    fetch(`/api/search-customer?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.customer) {
                selectedCustomer = data.customer;
                displayCustomerInfo(data.customer);
            } else {
                alert('Không tìm thấy khách hàng');
                document.getElementById('customer-info').style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra khi tìm kiếm');
        });
}

// Display customer info
function displayCustomerInfo(customer) {
    const infoDiv = document.getElementById('customer-info');
    infoDiv.innerHTML = `
        <div class="d-flex align-items-center mb-2">
            <img src="https://ui-avatars.com/api/?name=${encodeURIComponent(customer.ho_ten)}&background=8b4513&color=fff" 
                 class="rounded-circle me-3" width="50" height="50">
            <div>
                <h6 class="mb-0">${customer.ho_ten}</h6>
                <small class="text-muted">${customer.so_dien_thoai}</small>
            </div>
        </div>
        <div class="row g-2">
            <div class="col-6">
                <small class="text-muted">Điểm hiện có:</small>
                <div class="fw-bold text-primary">${customer.diem_tich_luy || 0} điểm</div>
            </div>
            <div class="col-6">
                <small class="text-muted">Lượt đến:</small>
                <div class="fw-bold">${customer.so_lan_den || 0} lần</div>
            </div>
        </div>
    `;
    infoDiv.style.display = 'block';
    
    // Update points limit
    const pointsInput = document.getElementById('points-use');
    if (pointsInput) {
        pointsInput.max = customer.diem_tich_luy || 0;
        pointsInput.placeholder = `Tối đa ${customer.diem_tich_luy || 0} điểm`;
    }
}

// Load booking
function loadBooking() {
    const bookingCode = document.getElementById('booking-code').value.trim();
    
    if (!bookingCode) {
        alert('Vui lòng nhập mã booking');
        return;
    }
    
    fetch(`/api/load-booking?code=${encodeURIComponent(bookingCode)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.booking) {
                applyBookingData(data.booking);
            } else {
                alert('Không tìm thấy booking');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra khi tải booking');
        });
}

// Select booking from dropdown
function selectBooking(bookingId) {
    if (!bookingId) return;
    
    fetch(`/api/load-booking?id=${bookingId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.booking) {
                applyBookingData(data.booking);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra');
        });
}

// Apply booking data to cart
function applyBookingData(booking) {
    // Clear current cart
    cart = [];
    
    // Add services from booking
    booking.services.forEach(service => {
        cart.push({
            id: service.id,
            name: service.ten_dich_vu,
            price: service.gia,
            quantity: service.so_luong || 1
        });
    });
    
    // Set customer info
    if (booking.khach_hang) {
        selectedCustomer = booking.khach_hang;
        displayCustomerInfo(booking.khach_hang);
    }
    
    // Update cart
    updateCart();
    
    alert('Đã tải thông tin booking thành công!');
}

// Process payment
function processPayment() {
    if (cart.length === 0) {
        alert('Vui lòng chọn ít nhất một dịch vụ!');
        return;
    }
    
    // Get active tab to determine customer type
    const activeTab = document.querySelector('.customer-tabs .nav-link.active');
    const customerType = activeTab.getAttribute('href').replace('#', '');
    
    // Validate customer info
    let customerId = null;
    let customerName = '';
    let customerPhone = '';
    let bookingId = null;
    
    if (customerType === 'walk-in') {
        customerName = document.getElementById('customer-name').value.trim();
        customerPhone = document.getElementById('customer-phone').value.trim();
        
        if (!customerName || !customerPhone) {
            alert('Vui lòng nhập tên và số điện thoại khách hàng!');
            return;
        }
    } else if (customerType === 'registered') {
        if (!selectedCustomer) {
            alert('Vui lòng tìm và chọn khách hàng!');
            return;
        }
        customerId = selectedCustomer.id;
        customerName = selectedCustomer.ho_ten;
        customerPhone = selectedCustomer.so_dien_thoai;
    } else if (customerType === 'booking') {
        // TODO: Handle booking type
    }
    
    // Get payment method
    const paymentMethod = document.querySelector('input[name="payment-method"]:checked').value;
    
    // Validate cash payment
    if (paymentMethod === 'tien_mat') {
        const cashGiven = parseInt(document.getElementById('cash-given').value) || 0;
        const total = subtotal - discount;
        
        if (cashGiven < total) {
            alert('Số tiền khách đưa chưa đủ!');
            return;
        }
    }
    
    // Get voucher and points
    const voucherId = document.getElementById('voucher').value || null;
    const pointsUsed = parseInt(document.getElementById('points-use').value) || 0;
    const stylistId = document.getElementById('stylist').value;
    
    // Confirm payment
    const total = subtotal - discount;
    if (!confirm(`Xác nhận thanh toán ${total.toLocaleString('vi-VN')}đ?`)) {
        return;
    }
    
    // Prepare data
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCsrfToken());
    formData.append('customer_type', customerType);
    if (customerId) formData.append('customer_id', customerId);
    formData.append('customer_name', customerName);
    formData.append('customer_phone', customerPhone);
    if (bookingId) formData.append('booking_id', bookingId);
    formData.append('cart_data', JSON.stringify(cart));
    formData.append('payment_method', paymentMethod);
    if (voucherId) formData.append('voucher_id', voucherId);
    formData.append('points_used', pointsUsed);
    formData.append('stylist_id', stylistId);
    
    // Send request
    fetch('/staff/pos/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Thanh toán thành công! Mã hóa đơn: ' + data.ma_hoa_don);
            // Print invoice
            if (confirm('Bạn có muốn in hóa đơn?')) {
                window.open(`/invoices/${data.invoice_id}/print`, '_blank');
            }
            // Clear and reset
            clearAll();
        } else {
            alert('Lỗi: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Có lỗi xảy ra khi xử lý thanh toán!');
    });
}

// Get CSRF token
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Clear all
function clearAll() {
    if (cart.length > 0 && !confirm('Bạn có chắc muốn xóa tất cả?')) {
        return;
    }
    
    cart = [];
    subtotal = 0;
    discount = 0;
    selectedCustomer = null;
    
    updateCart();
    
    document.getElementById('customer-name').value = '';
    document.getElementById('customer-phone').value = '';
    document.getElementById('search-customer').value = '';
    document.getElementById('customer-info').style.display = 'none';
    document.getElementById('voucher').value = '';
    document.getElementById('points-use').value = '';
    document.getElementById('cash-given').value = '';
    document.getElementById('change').value = '';
}

// View history
function viewHistory() {
    window.location.href = '/staff/pos/history';
}

// Save draft
function saveDraft() {
    if (cart.length === 0) {
        alert('Giỏ hàng trống!');
        return;
    }
    
    // Save to localStorage
    localStorage.setItem('pos_draft', JSON.stringify({
        cart: cart,
        timestamp: new Date().toISOString()
    }));
    
    alert('Đã lưu nháp thành công!');
}

// Load draft
function loadDraft() {
    const draft = localStorage.getItem('pos_draft');
    if (draft) {
        const data = JSON.parse(draft);
        cart = data.cart;
        updateCart();
        alert('Đã khôi phục giỏ hàng!');
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Show/hide cash input based on payment method
    document.querySelectorAll('input[name="payment-method"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.getElementById('cash-input').style.display = 
                this.value === 'tien_mat' ? 'block' : 'none';
        });
    });
    
    // Recalculate discount when voucher or points change
    const voucherSelect = document.getElementById('voucher');
    if (voucherSelect) {
        voucherSelect.addEventListener('change', calculateDiscount);
    }
    
    const pointsInput = document.getElementById('points-use');
    if (pointsInput) {
        pointsInput.addEventListener('input', calculateDiscount);
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.key === 'F9') {
            e.preventDefault();
            processPayment();
        } else if (e.key === 'Escape') {
            if (confirm('Xóa tất cả?')) {
                clearAll();
            }
        }
    });
    
    // Load draft if exists
    if (localStorage.getItem('pos_draft')) {
        if (confirm('Có giỏ hàng nháp, bạn có muốn khôi phục?')) {
            loadDraft();
        }
    }
});
