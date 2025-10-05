"""
Script để cập nhật views.py với database queries
"""

import re

# Đọc file hiện tại
with open('barbershop/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup file gốc
with open('barbershop/views_backup.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Pattern 1: Cập nhật admin_staff view
admin_staff_old = r'''def admin_staff\(request\):
    """Staff Management"""
    context = \{[^}]+\}
    return render\(request, 'admin/staff\.html', context\)'''

admin_staff_new = '''def admin_staff(request):
    """Staff Management"""
    staff_list = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        da_xoa=False
    ).select_related('thongtinnhanvien').order_by('-ngay_tao')
    
    context = {
        'staff_list': staff_list,
        'total_staff': staff_list.count(),
        'active_staff': staff_list.filter(trang_thai='hoat_dong').count(),
    }
    return render(request, 'admin/staff.html', context)'''

content = re.sub(admin_staff_old, admin_staff_new, content, flags=re.DOTALL)

# Pattern 2: Cập nhật admin_services view
admin_services_old = r'''def admin_services\(request\):
    """Services Management"""
    context = \{[^}]+categories[^}]+\}
    return render\(request, 'admin/services\.html', context\)'''

admin_services_new = '''def admin_services(request):
    """Services Management"""
    categories = DanhMucDichVu.objects.filter(da_xoa=False).prefetch_related('dichvu_set')
    all_services = DichVu.objects.filter(da_xoa=False).select_related('danh_muc')
    
    context = {
        'categories': categories,
        'services': all_services,
        'total_services': all_services.count(),
    }
    return render(request, 'admin/services.html', context)'''

content = re.sub(admin_services_old, admin_services_new, content, flags=re.DOTALL)

# Pattern 3: Cập nhật admin_bookings view  
admin_bookings_old = r'''def admin_bookings\(request\):
    """Bookings Management"""
    context = \{[^}]+pending[^}]+\}
    return render\(request, 'admin/bookings\.html', context\)'''

admin_bookings_new = '''def admin_bookings(request):
    """Bookings Management"""
    bookings = DatLich.objects.filter(
        da_xoa=False
    ).select_related('khach_hang', 'nhan_vien').prefetch_related('dichvudatlich_set__dich_vu').order_by('-ngay_dat', '-gio_bat_dau')
    
    # Filter by status
    status = request.GET.get('status', 'all')
    if status != 'all':
        bookings = bookings.filter(trang_thai=status)
    
    context = {
        'bookings': bookings,
        'total_bookings': bookings.count(),
        'pending': bookings.filter(trang_thai='cho_xac_nhan').count(),
        'confirmed': bookings.filter(trang_thai='da_xac_nhan').count(),
        'completed': bookings.filter(trang_thai='hoan_thanh').count(),
        'cancelled': bookings.filter(trang_thai='da_huy').count(),
    }
    return render(request, 'admin/bookings.html', context)'''

content = re.sub(admin_bookings_old, admin_bookings_new, content, flags=re.DOTALL)

# Pattern 4: Cập nhật admin_customers view
admin_customers_old = r'''def admin_customers\(request\):
    """Customers Management"""
    context = \{[^}]+loyal_customers[^}]+\}
    return render\(request, 'admin/customers\.html', context\)'''

admin_customers_new = '''def admin_customers(request):
    """Customers Management"""
    customers = NguoiDung.objects.filter(
        vai_tro='khach_hang',
        da_xoa=False
    ).annotate(
        total_bookings=Count('datlich_khachhang', filter=Q(datlich_khachhang__da_xoa=False))
    ).order_by('-ngay_tao')
    
    context = {
        'customers': customers,
        'total_customers': customers.count(),
        'new_customers': customers.filter(ngay_tao__gte=timezone.now() - timedelta(days=30)).count(),
    }
    return render(request, 'admin/customers.html', context)'''

content = re.sub(admin_customers_old, admin_customers_new, content, flags=re.DOTALL)

# Ghi file mới
with open('barbershop/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Đã cập nhật views.py")
print("📝 File backup: barbershop/views_backup.py")
