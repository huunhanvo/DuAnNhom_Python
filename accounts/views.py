"""
Views for accounts app (Staff, Customers, Profile)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum, Q, Avg, F, Max
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from decimal import Decimal
import json
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import bcrypt

# Import decorators from core
from core.decorators import require_auth, require_role

# Import models
from barbershop.models import (
    NguoiDung,
    ThongTinNhanVien,
    DatLich,
    HoaDon,
    DichVu,
    DanhGia,
    DichVuDatLich,
    LichLamViec
)

# ============ VIEWS - Bạn sẽ copy code vào đây ============
# Các views sẽ được di chuyển vào đây:
# - admin_staff
@require_role(['quan_ly'])
def admin_staff(request):
    """Staff Management with CRUD, Search, Filter"""
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            # Create new staff with validation
            try:
                # Validate required fields
                ho_ten = request.POST.get('ho_ten', '').strip()
                so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
                email = request.POST.get('email', '').strip()
                
                if not ho_ten:
                    return JsonResponse({'success': False, 'message': 'Há» tÃªn khÃ´ng ÄÆ°á»£c Äá» trá»ng'})
                
                if not so_dien_thoai:
                    return JsonResponse({'success': False, 'message': 'Sá» Äiá»n thoáº¡i khÃ´ng ÄÆ°á»£c Äá» trá»ng'})
                
                # Check if phone already exists
                if NguoiDung.objects.filter(so_dien_thoai=so_dien_thoai, da_xoa=False).exists():
                    return JsonResponse({'success': False, 'message': f'Sá» Äiá»n thoáº¡i {so_dien_thoai} ÄÃ£ tá»n táº¡i!'})
                
                # Check if email already exists (if provided)
                if email and NguoiDung.objects.filter(email=email, da_xoa=False).exists():
                    return JsonResponse({'success': False, 'message': f'Email {email} ÄÃ£ tá»n táº¡i!'})
                
                # Validate phone format (basic)
                if not so_dien_thoai.isdigit() or len(so_dien_thoai) < 10:
                    return JsonResponse({'success': False, 'message': 'Sá» Äiá»n thoáº¡i khÃ´ng há»£p lá» (tá»i thiá»u 10 sá»)'})
                
                # Parse date
                ngay_sinh_str = request.POST.get('ngay_sinh', '').strip()
                ngay_sinh = None
                if ngay_sinh_str:
                    from datetime import datetime
                    try:
                        ngay_sinh = datetime.strptime(ngay_sinh_str, '%Y-%m-%d').date()
                    except ValueError:
                        return JsonResponse({'success': False, 'message': 'NgÃ y sinh khÃ´ng há»£p lá» (Äá»nh dáº¡ng: YYYY-MM-DD)'})
                
                # Create user account
                user = NguoiDung.objects.create(
                    ho_ten=ho_ten,
                    so_dien_thoai=so_dien_thoai,
                    email=email if email else None,
                    vai_tro='nhan_vien',
                    ngay_sinh=ngay_sinh,
                    gioi_tinh=request.POST.get('gioi_tinh', 'nam'),
                    dia_chi=request.POST.get('dia_chi', '').strip() or None,
                    trang_thai=True,
                    da_xoa=False
                )
                
                # Hash password
                password = request.POST.get('password', '123456')
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user.mat_khau_hash = hashed.decode('utf-8')
                user.save()
                
                # Create staff info (only staff-specific fields)
                chuyen_mon_raw = request.POST.get('chuyen_mon', '').strip()
                chung_chi_raw = request.POST.get('chung_chi', '').strip()
                
                ThongTinNhanVien.objects.create(
                    nguoi_dung=user,
                    cccd=request.POST.get('cccd', '').strip() or None,
                    chuyen_mon=chuyen_mon_raw if chuyen_mon_raw else None,
                    kinh_nghiem_nam=int(request.POST.get('kinh_nghiem_nam', 0) or 0),
                    chung_chi=chung_chi_raw if chung_chi_raw else None,
                    mo_ta=request.POST.get('mo_ta', '').strip() or None,
                )
                
                return JsonResponse({'success': True, 'message': 'ÄÃ£ thÃªm nhÃ¢n viÃªn má»i thÃ nh cÃ´ng!', 'staff_id': user.id})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Lá»i: {str(e)}'})
        
        elif action == 'delete':
            # Soft delete staff
            try:
                staff_id = request.POST.get('staff_id')
                user = get_object_or_404(NguoiDung, id=staff_id, vai_tro='nhan_vien', da_xoa=False)
                user.da_xoa = True
                user.ngay_xoa = timezone.now()
                user.save()
                
                return JsonResponse({'success': True, 'message': 'ÄÃ£ xÃ³a nhÃ¢n viÃªn!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        elif action == 'toggle_status':
            # Toggle active/inactive
            try:
                staff_id = request.POST.get('staff_id')
                user = get_object_or_404(NguoiDung, id=staff_id, vai_tro='nhan_vien', da_xoa=False)
                user.trang_thai = not user.trang_thai
                user.save()
                
                status_text = 'kÃ­ch hoáº¡t' if user.trang_thai else 'táº¡m ngá»«ng'
                return JsonResponse({'success': True, 'message': f'ÄÃ£ {status_text} nhÃ¢n viÃªn!', 'new_status': user.trang_thai})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
    
    # GET request - list staff with filters
    staff_query = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        da_xoa=False
    ).select_related('thong_tin_nhan_vien')
    
    # Search
    search = request.GET.get('search', '').strip()
    if search:
        staff_query = staff_query.filter(
            Q(ho_ten__icontains=search) |
            Q(so_dien_thoai__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        staff_query = staff_query.filter(trang_thai=True)
    elif status_filter == 'inactive':
        staff_query = staff_query.filter(trang_thai=False)
    
    # Sort
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'name':
        staff_query = staff_query.order_by('ho_ten')
    elif sort_by == 'rating':
        staff_query = staff_query.order_by('-thong_tin_nhan_vien__danh_gia_trung_binh')
    elif sort_by == 'revenue':
        # Sort by total revenue (bookings count as proxy)
        staff_query = staff_query.annotate(
            total_bookings=Count('dat_lich_nhan_vien', filter=Q(dat_lich_nhan_vien__da_xoa=False))
        ).order_by('-total_bookings')
    else:
        staff_query = staff_query.order_by('-ngay_tao')
    
    # Annotate with statistics
    staff_users = staff_query.annotate(
        booking_count=Count('dat_lich_nhan_vien', filter=Q(dat_lich_nhan_vien__da_xoa=False)),
    )
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(staff_users, 10)  # 10 per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'staff_list': page_obj,
        'total_staff': staff_users.count(),
        'active_staff': staff_users.filter(trang_thai=True).count(),
        'search': search,
        'status_filter': status_filter,
        'sort_by': sort_by,
    }
    return render(request, 'admin/staff.html', context)
# - admin_staff_detail
@require_role(['quan_ly'])
def admin_staff_detail(request, staff_id):
    """Staff Detail with Statistics"""
    user = get_object_or_404(NguoiDung, id=staff_id, vai_tro='nhan_vien', da_xoa=False)
    
    # Get staff details
    staff_info = None
    if hasattr(user, 'thong_tin_nhan_vien'):
        staff_info = user.thong_tin_nhan_vien
    
    # Calculate statistics
    from django.db.models import Count
    
    # Total bookings
    total_bookings = DatLich.objects.filter(nhan_vien=user, da_xoa=False).count()
    
    # Unique customers
    total_customers = DatLich.objects.filter(nhan_vien=user, da_xoa=False).values('khach_hang').distinct().count()
    
    # Average rating from ThongTinNhanVien
    avg_rating = 0
    if staff_info and staff_info.danh_gia_trung_binh:
        avg_rating = round(float(staff_info.danh_gia_trung_binh), 1)
    
    # Get bookings
    bookings = DatLich.objects.filter(
        nhan_vien=user,
        da_xoa=False
    ).select_related('khach_hang').prefetch_related('dich_vu_dat_lich__dich_vu').order_by('-ngay_hen', '-gio_hen')[:10]
    
    # Get work schedule
    schedules = LichLamViec.objects.filter(
        nhan_vien=user,
        da_xoa=False
    ).order_by('ngay_lam')[:7]
    
    # Skills (from chuyen_mon)
    skills = []
    if staff_info and staff_info.chuyen_mon:
        if isinstance(staff_info.chuyen_mon, str):
            skills = [s.strip() for s in staff_info.chuyen_mon.split(',') if s.strip()]
        elif isinstance(staff_info.chuyen_mon, list):
            skills = staff_info.chuyen_mon
    
    # Certificates
    certificates = []
    if staff_info and staff_info.chung_chi:
        if isinstance(staff_info.chung_chi, str):
            certificates = [c.strip() for c in staff_info.chung_chi.split(',') if c.strip()]
        elif isinstance(staff_info.chung_chi, list):
            certificates = staff_info.chung_chi
    
    context = {
        'staff': user,
        'user': user,
        'staff_info': staff_info,
        'bookings': bookings,
        'schedules': schedules,
        'skills': skills,
        'certificates': certificates,
        # Statistics
        'chuc_vu': 'NhÃ¢n viÃªn',  # Default role
        'avg_rating': avg_rating,
        'total_services': total_bookings,  # Total bookings as proxy
        'total_customers': total_customers,
    }
    return render(request, 'admin/staff-detail.html', context)

# - admin_staff_edit
@require_role(['quan_ly'])
def admin_staff_edit(request, staff_id):
    """Staff Edit with Complete Fields"""
    user = get_object_or_404(NguoiDung, id=staff_id, vai_tro='nhan_vien', da_xoa=False)
    
    if request.method == 'POST':
        try:
            # Update user info (NguoiDung fields)
            user.ho_ten = request.POST.get('ho_ten', user.ho_ten)
            user.email = request.POST.get('email', user.email) or None
            user.so_dien_thoai = request.POST.get('so_dien_thoai', user.so_dien_thoai)
            user.dia_chi = request.POST.get('dia_chi', '') or None
            
            # Update ngay_sinh, gioi_tinh (NguoiDung fields, not ThongTinNhanVien!)
            ngay_sinh_str = request.POST.get('ngay_sinh', '').strip()
            if ngay_sinh_str:
                from datetime import datetime
                try:
                    user.ngay_sinh = datetime.strptime(ngay_sinh_str, '%Y-%m-%d').date()
                except:
                    pass
            
            gioi_tinh = request.POST.get('gioi_tinh', '').strip()
            if gioi_tinh:
                user.gioi_tinh = gioi_tinh
            
            # Handle trang_thai checkbox
            user.trang_thai = request.POST.get('trang_thai') == 'on' or request.POST.get('trang_thai') == '1' or request.POST.get('trang_thai') == 'True'
            user.save()
            
            # Update or create staff info (ThongTinNhanVien fields only)
            staff_info, created = ThongTinNhanVien.objects.get_or_create(
                nguoi_dung=user,
                defaults={'da_xoa': False}
            )
            
            # Update ThongTinNhanVien fields (NOT ngay_sinh, gioi_tinh)
            cccd_raw = request.POST.get('cccd', '').strip()
            chuyen_mon_raw = request.POST.get('chuyen_mon', '').strip()
            chung_chi_raw = request.POST.get('chung_chi', '').strip()
            mo_ta_raw = request.POST.get('mo_ta', '').strip()
            
            staff_info.cccd = cccd_raw if cccd_raw else None
            staff_info.chuyen_mon = chuyen_mon_raw if chuyen_mon_raw else None
            
            kinh_nghiem = request.POST.get('kinh_nghiem_nam', '0')
            staff_info.kinh_nghiem_nam = int(kinh_nghiem) if kinh_nghiem else 0
            
            staff_info.chung_chi = chung_chi_raw if chung_chi_raw else None
            staff_info.mo_ta = mo_ta_raw if mo_ta_raw else None
            staff_info.save()
            
            from django.contrib import messages
            messages.success(request, 'ÄÃ£ cáº­p nháº­t thÃ´ng tin nhÃ¢n viÃªn!')
            return redirect('admin_staff_detail', staff_id=staff_id)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'CÃ³ lá»i xáº£y ra: {str(e)}')
    
    staff_info = None
    if hasattr(user, 'thong_tin_nhan_vien'):
        staff_info = user.thong_tin_nhan_vien
    
    context = {
        'staff': user,
        'user': user,
        'staff_info': staff_info,
        'chuc_vu': 'NhÃ¢n viÃªn',  # Default role
    }
    return render(request, 'admin/staff-edit.html', context)

# - admin_customers
@require_role(['quan_ly'])
def admin_customers(request):
    """Customer Management with stats, filters and CRUD"""
    from datetime import datetime, timedelta
    
    if request.method == 'POST':
        # Handle add customer
        try:
            # Validate required fields
            ho_ten = request.POST.get('ho_ten', '').strip()
            so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
            email = request.POST.get('email', '').strip()
            
            if not ho_ten:
                return JsonResponse({'success': False, 'message': 'Há» tÃªn khÃ´ng ÄÆ°á»£c Äá» trá»ng'})
            
            if not so_dien_thoai:
                return JsonResponse({'success': False, 'message': 'Sá» Äiá»n thoáº¡i khÃ´ng ÄÆ°á»£c Äá» trá»ng'})
            
            # Check if phone already exists
            if NguoiDung.objects.filter(so_dien_thoai=so_dien_thoai, da_xoa=False).exists():
                return JsonResponse({'success': False, 'message': f'Sá» Äiá»n thoáº¡i {so_dien_thoai} ÄÃ£ tá»n táº¡i!'})
            
            # Process email - set to None if empty
            email = email.strip() if email else None
            if email == '':
                email = None
                
            # Check if email already exists (if provided)
            if email and NguoiDung.objects.filter(email__iexact=email, da_xoa=False).exists():
                return JsonResponse({'success': False, 'message': f'Email {email} ÄÃ£ tá»n táº¡i!'})
            
            # Validate phone format
            if not so_dien_thoai.isdigit() or len(so_dien_thoai) < 10:
                return JsonResponse({'success': False, 'message': 'Sá» Äiá»n thoáº¡i khÃ´ng há»£p lá» (tá»i thiá»u 10 sá»)'})
            
            # Parse birth date
            ngay_sinh_str = request.POST.get('ngay_sinh', '').strip()
            ngay_sinh = None
            if ngay_sinh_str:
                try:
                    ngay_sinh = datetime.strptime(ngay_sinh_str, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'NgÃ y sinh khÃ´ng há»£p lá» (Äá»nh dáº¡ng: YYYY-MM-DD)'})
            
            # Create customer
            import bcrypt
            customer = NguoiDung.objects.create(
                ho_ten=ho_ten,
                so_dien_thoai=so_dien_thoai,
                email=email,
                vai_tro='khach_hang',
                ngay_sinh=ngay_sinh,
                dia_chi=request.POST.get('dia_chi', '').strip() or None,
                mat_khau_hash=bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),  # Default password
                trang_thai=True,
                da_xoa=False
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'ÄÃ£ thÃªm khÃ¡ch hÃ ng {ho_ten} thÃ nh cÃ´ng!',
                'customer_id': customer.id
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Lá»i: {str(e)}'})
    
    # GET request - Base query
    customers_query = NguoiDung.objects.filter(
        vai_tro='khach_hang',
        da_xoa=False
    )
    
    # Apply filters
    search = request.GET.get('search', '').strip()
    if search:
        customers_query = customers_query.filter(
            Q(ho_ten__icontains=search) |
            Q(so_dien_thoai__icontains=search) |
            Q(email__icontains=search)
        )
    
    tier = request.GET.get('tier', '')
    status = request.GET.get('status', '')
    
    # Add annotations for stats
    customers = customers_query.annotate(
        so_lan_cat=Count('dat_lich', filter=Q(dat_lich__da_xoa=False, dat_lich__trang_thai='hoan_thanh')),
        tong_chi_tieu=Sum('hoa_don__thanh_tien', filter=Q(hoa_don__da_xoa=False)) or 0
    ).order_by('-ngay_tao')
    
    # Add customer tier calculation
    customer_list = []
    for customer in customers:
        points = customer.diem_tich_luy or 0
        if points >= 1000:
            hang_thanh_vien = 'platinum'
        elif points >= 500:
            hang_thanh_vien = 'gold'
        elif points >= 200:
            hang_thanh_vien = 'silver'
        else:
            hang_thanh_vien = 'bronze'
        
        # Add tier to customer object
        customer.hang_thanh_vien = hang_thanh_vien
        customer_list.append(customer)
    
    # Apply tier filter
    if tier:
        customer_list = [c for c in customer_list if c.hang_thanh_vien == tier]
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(customer_list, 20)
    page = request.GET.get('page', 1)
    customers_page = paginator.get_page(page)
    
    # Statistics
    total_customers = customers_query.count()
    new_customers_month = customers_query.filter(
        ngay_tao__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    vip_customers = sum(1 for c in customer_list if c.hang_thanh_vien in ['gold', 'platinum'])
    active_customers = sum(1 for c in customer_list if c.so_lan_cat > 0)
    
    # Calculate averages
    total_visits = sum(c.so_lan_cat for c in customer_list)
    total_spending = sum(float(c.tong_chi_tieu or 0) for c in customer_list)
    
    avg_visits = total_visits / total_customers if total_customers > 0 else 0
    avg_spending = total_spending / total_customers if total_customers > 0 else 0
    
    context = {
        'customers': customers_page,
        'total_customers': total_customers,
        'new_customers_month': new_customers_month,
        'vip_customers': vip_customers,
        'active_customers': active_customers,
        'avg_visits': avg_visits,
        'avg_spending': avg_spending,
        'search': search,
        'tier': tier,
        'status': status,
    }
    return render(request, 'admin/customers.html', context)
# - staff_profile
@require_role(['nhan_vien', 'quan_ly'])
def staff_profile(request):
    """My Profile with Update Capability"""
    user_id = request.session.get('user_id')
    user = get_object_or_404(NguoiDung, id=user_id, da_xoa=False)
    
    staff_info = None
    try:
        staff_info = ThongTinNhanVien.objects.get(nguoi_dung=user, da_xoa=False)
    except ThongTinNhanVien.DoesNotExist:
        pass
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_info':
            # Update basic info
            try:
                user.ho_ten = request.POST.get('ho_ten', user.ho_ten)
                user.email = request.POST.get('email', user.email)
                user.dia_chi = request.POST.get('dia_chi', user.dia_chi)
                user.save()
                
                # Update staff info if exists
                if staff_info:
                    staff_info.cccd = request.POST.get('cccd', staff_info.cccd)
                    staff_info.ngay_sinh = request.POST.get('ngay_sinh', staff_info.ngay_sinh)
                    staff_info.gioi_tinh = request.POST.get('gioi_tinh', staff_info.gioi_tinh)
                    staff_info.save()
                
                return JsonResponse({'success': True, 'message': 'ÄÃ£ cáº­p nháº­t thÃ´ng tin!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        elif action == 'change_password':
            # Change password
            try:
                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                
                # Verify old password
                if not bcrypt.checkpw(old_password.encode('utf-8'), user.mat_khau_hash.encode('utf-8')):
                    return JsonResponse({'success': False, 'message': 'Máº­t kháº©u cÅ© khÃ´ng ÄÃºng!'})
                
                # Check new password match
                if new_password != confirm_password:
                    return JsonResponse({'success': False, 'message': 'Máº­t kháº©u xÃ¡c nháº­n khÃ´ng khá»p!'})
                
                # Check password strength
                if len(new_password) < 6:
                    return JsonResponse({'success': False, 'message': 'Máº­t kháº©u pháº£i cÃ³ Ã­t nháº¥t 6 kÃ½ tá»±!'})
                
                # Update password
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.mat_khau_hash = hashed.decode('utf-8')
                user.save()
                
                return JsonResponse({'success': True, 'message': 'ÄÃ£ Äá»i máº­t kháº©u thÃ nh cÃ´ng!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
    
    # Calculate statistics for GET request
    today = timezone.now().date()
    month_start = today.replace(day=1)
    
    # Total services completed
    total_services = DatLich.objects.filter(
        nhan_vien_id=user_id,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).count()
    
    # Monthly services
    monthly_services = DatLich.objects.filter(
        nhan_vien_id=user_id,
        ngay_hen__gte=month_start,
        ngay_hen__lte=today,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).count()
    
    # Monthly revenue
    monthly_revenue = DatLich.objects.filter(
        nhan_vien_id=user_id,
        ngay_hen__gte=month_start,
        ngay_hen__lte=today,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).aggregate(total=Sum('thanh_tien'))['total'] or 0
    
    # Average rating
    avg_rating = DanhGia.objects.filter(
        nhan_vien_id=user_id,
        da_xoa=False
    ).aggregate(avg=Avg('so_sao'))['avg'] or 0
    
    # Monthly rating
    monthly_rating = DanhGia.objects.filter(
        nhan_vien_id=user_id,
        ngay_tao__gte=month_start,
        ngay_tao__lte=timezone.now(),
        da_xoa=False
    ).aggregate(avg=Avg('so_sao'))['avg'] or 0
    
    # Years of experience
    years_experience = 0
    if staff_info and staff_info.ngay_tao:
        work_start = staff_info.ngay_tao.date() if staff_info.ngay_tao else today
        years_experience = (today - work_start).days // 365
    
    # Skills (mock data)
    skills = [
        'Cắt tóc cơ bản',
        'Gội đầu massage', 
        'Tạo kiểu tóc',
        'Cắt râu'
    ]
    
    # Recent work history (last 10 completed bookings)
    recent_work = DatLich.objects.filter(
        nhan_vien_id=user_id,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).select_related('khach_hang').prefetch_related('dich_vu_dat_lich').order_by('-ngay_hen')[:10]
    
    # Format work history
    work_history = []
    for booking in recent_work:
        services_list = []
        for service_booking in booking.dich_vu_dat_lich.all():
            services_list.append(service_booking.ten_dich_vu)
        
        work_history.append({
            'date': booking.ngay_hen,
            'customer': booking.khach_hang.ho_ten if booking.khach_hang else booking.ten_khach_hang or 'Khách vãng lai',
            'services': ', '.join(services_list) if services_list else 'Dịch vụ khác',
            'revenue': booking.thanh_tien
        })
    
    # Staff context for template
    staff_context = {
        'ho_ten': user.ho_ten,
        'so_dien_thoai': user.so_dien_thoai,
        'email': user.email,
        'ngay_sinh': getattr(user, 'ngay_sinh', None),
        'dia_chi': user.dia_chi,
        'chuc_vu': 'Nhân viên',
        'ngay_vao_lam': staff_info.ngay_tao.date() if staff_info and staff_info.ngay_tao else None,
        'cccd': staff_info.cccd if staff_info else '',
        'gioi_thieu': getattr(staff_info, 'mo_ta', ''),
        'anh_dai_dien': user.anh_dai_dien if user.anh_dai_dien else None,
        'total_services': total_services,
        'avg_rating': avg_rating,
        'years_experience': years_experience,
    }
    
    # GET request - show profile
    context = {
        'user': user,
        'staff_info': staff_info,
        'staff': staff_context,
        'monthly_services': monthly_services,
        'monthly_revenue': monthly_revenue,
        'monthly_rating': monthly_rating,
        'skills': skills,
        'work_history': work_history,
    }
    return render(request, 'staff/profile.html', context)
# - api_staff_update_profile
@csrf_exempt
@require_role(['nhan_vien', 'quan_ly'])
def api_staff_update_profile(request):
    """API endpoint for updating staff profile"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(NguoiDung, id=user_id, da_xoa=False)
            
            # Update basic user info
            user.ho_ten = request.POST.get('ho_ten', user.ho_ten)
            user.so_dien_thoai = request.POST.get('so_dien_thoai', user.so_dien_thoai)
            user.email = request.POST.get('email', user.email)
            user.dia_chi = request.POST.get('dia_chi', user.dia_chi)
            
            # Update ngay_sinh (belongs to NguoiDung)
            ngay_sinh = request.POST.get('ngay_sinh')
            if ngay_sinh:
                from datetime import datetime
                try:
                    user.ngay_sinh = datetime.strptime(ngay_sinh, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            user.save()
            
            # Update or create staff info
            staff_info, created = ThongTinNhanVien.objects.get_or_create(
                nguoi_dung=user,
                defaults={}
            )
            
            # Update staff specific fields (avoid problematic fields)
            gioi_thieu = request.POST.get('gioi_thieu')
            if gioi_thieu is not None:
                staff_info.mo_ta = gioi_thieu
            
            cccd = request.POST.get('cccd')
            if cccd is not None:
                staff_info.cccd = cccd
            
            # Only save if there are actual changes to avoid triggering constraints
            fields_to_update = []
            if gioi_thieu is not None:
                fields_to_update.append('mo_ta')
            if cccd is not None:
                fields_to_update.append('cccd')
                
            if fields_to_update:
                staff_info.save(update_fields=fields_to_update + ['ngay_cap_nhat'])
            else:
                # Just update the timestamp
                staff_info.ngay_cap_nhat = timezone.now()
                staff_info.save(update_fields=['ngay_cap_nhat'])
            
            return JsonResponse({
                'success': True,
                'message': 'Cập nhật thông tin thành công!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Lỗi cập nhật: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - api_staff_change_password
@csrf_exempt
@require_role(['nhan_vien', 'quan_ly'])
def api_staff_change_password(request):
    """API endpoint for changing password"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(NguoiDung, id=user_id, da_xoa=False)
            
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validate inputs
            if not all([old_password, new_password, confirm_password]):
                return JsonResponse({
                    'success': False,
                    'message': 'Vui lòng điền đầy đủ thông tin'
                })
            
            # Verify old password (support multiple hash formats)
            password_matches = False
            
            if user.mat_khau_hash.startswith('$2b$'):
                try:
                    password_matches = bcrypt.checkpw(old_password.encode('utf-8'), user.mat_khau_hash.encode('utf-8'))
                except ValueError:
                    pass
            elif user.mat_khau_hash.startswith('pbkdf2_sha256$'):
                from django.contrib.auth.hashers import check_password
                try:
                    password_matches = check_password(old_password, user.mat_khau_hash)
                except Exception:
                    pass
            
            if not password_matches:
                return JsonResponse({
                    'success': False,
                    'message': 'Mật khẩu cũ không đúng!'
                })
            
            # Check new password match
            if new_password != confirm_password:
                return JsonResponse({
                    'success': False,
                    'message': 'Mật khẩu xác nhận không khớp!'
                })
            
            # Check password strength
            if len(new_password) < 6:
                return JsonResponse({
                    'success': False,
                    'message': 'Mật khẩu phải có ít nhất 6 ký tự!'
                })
            
            # Update password
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.mat_khau_hash = hashed.decode('utf-8')
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Đổi mật khẩu thành công!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Lỗi đổi mật khẩu: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - api_staff_upload_avatar
@csrf_exempt
@require_role(['nhan_vien', 'quan_ly'])
def api_staff_upload_avatar(request):
    """API endpoint for uploading avatar"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(NguoiDung, id=user_id, da_xoa=False)
            
            if 'avatar' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'message': 'Không có file được tải lên'
                })
            
            avatar_file = request.FILES['avatar']
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if avatar_file.content_type not in allowed_types:
                return JsonResponse({
                    'success': False,
                    'message': 'Chỉ chấp nhận file ảnh (JPG, PNG, GIF)'
                })
            
            # Validate file size (5MB max)
            if avatar_file.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'message': 'File quá lớn. Tối đa 5MB'
                })
            
            # Get or create staff info
            staff_info, created = ThongTinNhanVien.objects.get_or_create(
                nguoi_dung=user,
                defaults={}
            )
            
            # Save avatar to media folder
            import os
            from django.conf import settings
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            
            # Create avatars directory if it doesn't exist
            avatars_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
            os.makedirs(avatars_dir, exist_ok=True)
            
            # Generate unique filename
            file_extension = os.path.splitext(avatar_file.name)[1]
            filename = f'staff_{user_id}_{timezone.now().strftime("%Y%m%d_%H%M%S")}{file_extension}'
            
            # Save file
            file_path = os.path.join('avatars', filename)
            saved_path = default_storage.save(file_path, ContentFile(avatar_file.read()))
            
            # Update user's avatar field
            user.anh_dai_dien = saved_path
            user.save()
            
            avatar_url = settings.MEDIA_URL + saved_path
            
            return JsonResponse({
                'success': True,
                'message': 'Cập nhật ảnh đại diện thành công!',
                'avatar_url': avatar_url
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Lỗi tải ảnh: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - api_staff_update_notifications
@csrf_exempt
@require_role(['nhan_vien', 'quan_ly'])
def api_staff_update_notifications(request):
    """API endpoint for updating notification settings"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(NguoiDung, id=user_id, da_xoa=False)
            
            # Get notification settings (mock implementation)
            settings = {
                'email_booking': request.POST.get('emailBooking') == 'on',
                'email_reminder': request.POST.get('emailReminder') == 'on', 
                'email_review': request.POST.get('emailReview') == 'on',
                'push_booking': request.POST.get('pushBooking') == 'on',
                'push_reminder': request.POST.get('pushReminder') == 'on',
                'sms_booking': request.POST.get('smsBooking') == 'on',
            }
            
            # In a real app, you'd save these to a NotificationSettings model
            # For now, just return success
            
            return JsonResponse({
                'success': True,
                'message': 'Cập nhật cài đặt thông báo thành công!',
                'settings': settings
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Lỗi cập nhật cài đặt: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - staff_my_customers
@require_role(['nhan_vien', 'quan_ly'])
def staff_my_customers(request):
    """My Customers - Simple version"""
    user_id = request.session.get('user_id')
    
    # Get customers who booked with this staff
    customer_bookings = DatLich.objects.filter(
        nhan_vien_id=user_id,
        da_xoa=False
    ).exclude(trang_thai='da_huy')
    
    customer_ids = customer_bookings.values_list('khach_hang_id', flat=True).distinct()
    
    customers_list = []
    for customer_id in customer_ids:
        try:
            customer = NguoiDung.objects.get(id=customer_id, da_xoa=False)
            
            # Add basic attributes
            customer.visit_count = 0
            customer.total_revenue = 0
            customer.last_visit = None
            customer.loyalty_score = 50
            customer.hang_thanh_vien = 'bronze'
            customer.recent_visits = []
            customer.preferences = []
            
            customers_list.append(customer)
        except:
            continue
    
    context = {
        'customers': customers_list,
        'total_customers': len(customers_list),
        'regular_customers': 0,
        'this_month_customers': 0,
        'avg_rating': 0,
        'search_query': '',
        'sort_by': '',
        'tier_filter': '',
        'loyalty_filter': '',
    }
    return render(request, 'staff/my-customers.html', context)
# - api_customer_detail
def api_customer_detail(request, customer_id):
    """API: Get customer detail"""
    try:
        customer = get_object_or_404(NguoiDung, id=customer_id, vai_tro='khach_hang', da_xoa=False)
        
        # Calculate customer stats
        bookings = DatLich.objects.filter(khach_hang=customer, da_xoa=False)
        completed_bookings = bookings.filter(trang_thai='hoan_thanh')
        total_spending = sum(booking.thanh_tien or 0 for booking in completed_bookings)
        
        # Get customer tier
        points = customer.diem_tich_luy or 0
        if points >= 1000:
            hang_thanh_vien = 'platinum'
            hang_display = 'Báº¡ch kim'
        elif points >= 500:
            hang_thanh_vien = 'gold'
            hang_display = 'VÃ ng'
        elif points >= 200:
            hang_thanh_vien = 'silver'
            hang_display = 'Báº¡c'
        else:
            hang_thanh_vien = 'bronze'
            hang_display = 'Äá»ng'
        
        # Get history
        history = []
        for booking in bookings.order_by('-ngay_hen', '-gio_hen')[:10]:
            services = []
            for service in booking.dich_vu_dat_lich.all():
                services.append(service.ten_dich_vu)
            
            history.append({
                'type': 'booking',
                'date': booking.ngay_hen.strftime('%d/%m/%Y'),
                'amount': float(booking.thanh_tien or 0),
                'services': services,
                'status': booking.trang_thai
            })
        
        customer_data = {
            'id': customer.id,
            'ho_ten': customer.ho_ten,
            'so_dien_thoai': customer.so_dien_thoai,
            'email': customer.email,
            'ngay_sinh': customer.ngay_sinh.strftime('%d/%m/%Y') if customer.ngay_sinh else None,
            'dia_chi': customer.dia_chi,
            'anh_dai_dien': customer.anh_dai_dien,
            'diem_tich_luy': points,
            'so_lan_cat': completed_bookings.count(),
            'tong_chi_tieu': float(total_spending),
            'hang_thanh_vien': hang_thanh_vien,
            'hang_thanh_vien_display': hang_display,
            'ngay_tao': customer.ngay_tao.strftime('%d/%m/%Y'),
            'history': history
        }
        
        return JsonResponse(customer_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
# - api_customer_detail_staff
@require_role(['nhan_vien', 'quan_ly'])
def api_customer_detail_staff(request, customer_id):
    """Get detailed customer information for staff"""
    if request.method == 'GET':
        try:
            user_id = request.session.get('user_id')
            
            # Get customer
            customer = get_object_or_404(NguoiDung, id=customer_id, da_xoa=False)
            
            # Get customer's bookings with this staff
            bookings = DatLich.objects.filter(
                khach_hang_id=customer_id,
                nhan_vien_id=user_id,
                da_xoa=False
            ).exclude(trang_thai='da_huy').select_related('dich_vu').order_by('-ngay_hen')
            
            # Calculate stats
            completed_bookings = bookings.filter(trang_thai='hoan_thanh')
            visit_count = completed_bookings.count()
            total_revenue = completed_bookings.aggregate(
                total=Sum('thanh_tien')
            )['total'] or 0
            
            # Get average rating
            avg_rating = DanhGia.objects.filter(
                khach_hang_id=customer_id,
                nhan_vien_id=user_id,
                da_xoa=False
            ).aggregate(avg_rating=Avg('so_sao'))['avg_rating'] or 0
            
            # Get booking history
            history = []
            for booking in bookings[:20]:  # Latest 20 bookings
                # Try to get rating for this booking through HoaDon
                rating = None
                try:
                    if hasattr(booking, 'hoa_don') and booking.hoa_don:
                        rating_obj = DanhGia.objects.filter(
                            hoa_don=booking.hoa_don,
                            khach_hang_id=customer_id,
                            nhan_vien_id=user_id,
                            da_xoa=False
                        ).first()
                        if rating_obj:
                            rating = rating_obj.so_sao
                except:
                    pass
                
                history.append({
                    'id': booking.id,
                    'date': booking.ngay_hen.strftime('%d/%m/%Y'),
                    'service': booking.dich_vu.ten_dich_vu if booking.dich_vu else 'Dịch vụ khác',
                    'amount': float(booking.thanh_tien),
                    'status': booking.get_trang_thai_display(),
                    'rating': rating
                })
            
            # Get favorite services (most booked services)
            favorite_services = DatLich.objects.filter(
                khach_hang_id=customer_id,
                nhan_vien_id=user_id,
                da_xoa=False,
                trang_thai='hoan_thanh',
                dich_vu__isnull=False
            ).values('dich_vu__ten_dich_vu').annotate(
                count=Count('dich_vu')
            ).order_by('-count')[:5]
            
            preferences = [service['dich_vu__ten_dich_vu'] for service in favorite_services]
            
            data = {
                'id': customer.id,
                'ho_ten': customer.ho_ten,
                'so_dien_thoai': customer.so_dien_thoai,
                'email': customer.email or '',
                'anh_dai_dien': customer.anh_dai_dien.url if customer.anh_dai_dien else '',
                'visit_count': visit_count,
                'total_revenue': float(total_revenue),
                'avg_rating': float(avg_rating),
                'history': history,
                'preferences': preferences,
                'first_visit': bookings.last().ngay_hen.strftime('%d/%m/%Y') if bookings.exists() else '',
                'last_visit': bookings.first().ngay_hen.strftime('%d/%m/%Y') if bookings.exists() else ''
            }
            
            return JsonResponse(data)
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - staff_customers_export
@require_role(['nhan_vien', 'quan_ly'])
def staff_customers_export(request):
    """Export customers list to Excel"""
    try:
        user_id = request.session.get('user_id')
        
        # Get customers data (similar to main view but without pagination)
        customer_bookings = DatLich.objects.filter(
            nhan_vien_id=user_id,
            da_xoa=False
        ).exclude(trang_thai='da_huy')
        
        customer_ids = customer_bookings.values_list('khach_hang_id', flat=True).distinct()
        
        customers = NguoiDung.objects.filter(
            id__in=customer_ids,
            da_xoa=False
        ).annotate(
            visit_count=Count('dat_lich', filter=Q(
                dat_lich__nhan_vien_id=user_id,
                dat_lich__da_xoa=False,
                dat_lich__trang_thai='hoan_thanh'
            )),
            total_revenue=Sum('dat_lich__thanh_tien', filter=Q(
                dat_lich__nhan_vien_id=user_id,
                dat_lich__da_xoa=False,
                dat_lich__trang_thai='hoan_thanh'
            )),
            last_visit=Max('dat_lich__ngay_hen', filter=Q(
                dat_lich__nhan_vien_id=user_id,
                dat_lich__da_xoa=False,
                dat_lich__trang_thai='hoan_thanh'
            )),
            avg_rating=Avg('danh_gia_khach_hang__so_sao', filter=Q(
                danh_gia_khach_hang__nhan_vien_id=user_id,
                danh_gia_khach_hang__da_xoa=False
            ))
        ).order_by('-visit_count')
        
        # Create CSV response
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="khach_hang_{timezone.now().strftime("%Y%m%d")}.csv"'
        
        # Add BOM for Excel Vietnamese support
        response.write('\ufeff')
        
        writer = csv.writer(response)
        writer.writerow([
            'Họ tên', 'Số điện thoại', 'Email', 'Số lần cắt', 
            'Tổng chi tiêu', 'Đánh giá TB', 'Lần cuối'
        ])
        
        for customer in customers:
            writer.writerow([
                customer.ho_ten,
                customer.so_dien_thoai,
                customer.email or '',
                customer.visit_count or 0,
                f"{customer.total_revenue or 0:,.0f}",
                f"{customer.avg_rating or 0:.1f}",
                customer.last_visit.strftime('%d/%m/%Y') if customer.last_visit else ''
            ])
        
        return response
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})


# ==================== CUSTOMER AUTHENTICATION VIEWS ====================

def register(request):
    """Customer registration"""
    if request.method == 'GET':
        # Show registration form
        return render(request, 'customer/register.html')
    
    elif request.method == 'POST':
        try:
            import hashlib
            import re
            
            # Get form data
            ho_ten = request.POST.get('ho_ten', '').strip()
            so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
            email = request.POST.get('email', '').strip()
            mat_khau = request.POST.get('mat_khau', '')
            xac_nhan_mat_khau = request.POST.get('xac_nhan_mat_khau', '')
            
            # Validation
            if not all([ho_ten, so_dien_thoai, mat_khau]):
                return JsonResponse({
                    'success': False,
                    'message': 'Vui lòng điền đầy đủ thông tin bắt buộc'
                })
            
            # Validate phone number format
            if not re.match(r'^(0|\+84)[0-9]{9,10}$', so_dien_thoai):
                return JsonResponse({
                    'success': False,
                    'message': 'Số điện thoại không hợp lệ'
                })
            
            # Validate email format if provided
            if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                return JsonResponse({
                    'success': False,
                    'message': 'Email không hợp lệ'
                })
            
            # Validate password
            if len(mat_khau) < 6:
                return JsonResponse({
                    'success': False,
                    'message': 'Mật khẩu phải có ít nhất 6 ký tự'
                })
            
            if mat_khau != xac_nhan_mat_khau:
                return JsonResponse({
                    'success': False,
                    'message': 'Mật khẩu xác nhận không khớp'
                })
            
            # Check if phone number already exists
            if NguoiDung.objects.filter(so_dien_thoai=so_dien_thoai, da_xoa=False).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Số điện thoại đã được đăng ký'
                })
            
            # Check if email already exists (if provided)
            if email and NguoiDung.objects.filter(email=email, da_xoa=False).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Email đã được đăng ký'
                })
            
            # Create customer account with bcrypt password
            hashed_password = bcrypt.hashpw(mat_khau.encode('utf-8'), bcrypt.gensalt())
            
            customer = NguoiDung.objects.create(
                ho_ten=ho_ten,
                so_dien_thoai=so_dien_thoai,
                email=email if email else None,
                mat_khau_hash=hashed_password.decode('utf-8'),
                vai_tro='khach_hang',
                trang_thai=True,  # Boolean, not string
                diem_tich_luy=0
            )
            
            # Award welcome points (e.g., 100 points)
            from barbershop.models import GiaoDichDiem
            welcome_points = 100
            customer.diem_tich_luy = welcome_points
            customer.save()
            
            GiaoDichDiem.objects.create(
                khach_hang=customer,
                loai_giao_dich='cong',
                so_diem=welcome_points,
                diem_truoc=0,
                diem_sau=welcome_points,
                mo_ta='Điểm thưởng chào mừng thành viên mới'
            )
            
            # Auto login
            request.session['user_id'] = customer.id
            request.session['vai_tro'] = customer.vai_tro
            request.session['ho_ten'] = customer.ho_ten
            request.session['welcome_bonus'] = welcome_points
            
            return JsonResponse({
                'success': True,
                'message': f'Đăng ký thành công! Bạn nhận được {welcome_points} điểm thưởng.',
                'redirect': '/accounts/register-success/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Có lỗi xảy ra: {str(e)}'
            })


def register_success(request):
    """Registration success page"""
    # Check if user just registered
    if not request.session.get('user_id') or request.session.get('vai_tro') != 'khach_hang':
        return redirect('accounts:customer_login')
    
    context = {
        'user_name': request.session.get('ho_ten', 'Bạn'),
        'welcome_bonus': request.session.get('welcome_bonus', 100)
    }
    
    # Clear welcome bonus from session
    if 'welcome_bonus' in request.session:
        del request.session['welcome_bonus']
    
    return render(request, 'customer/register_success.html', context)


def customer_login(request):
    """Customer login"""
    if request.method == 'GET':
        # Show login form
        return render(request, 'customer/login.html')
    
    elif request.method == 'POST':
        try:
            import hashlib
            
            so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
            mat_khau = request.POST.get('mat_khau', '')
            
            if not all([so_dien_thoai, mat_khau]):
                return JsonResponse({
                    'success': False,
                    'message': 'Vui lòng nhập đầy đủ thông tin'
                })
            
            # Find user
            try:
                user = NguoiDung.objects.get(
                    so_dien_thoai=so_dien_thoai,
                    da_xoa=False
                )
            except NguoiDung.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Số điện thoại hoặc mật khẩu không đúng'
                })
            
            # Check password (support both bcrypt and MD5)
            password_valid = False
            
            # Try bcrypt first (new format)
            if user.mat_khau_hash and user.mat_khau_hash.startswith('$2b$'):
                try:
                    password_valid = bcrypt.checkpw(mat_khau.encode('utf-8'), user.mat_khau_hash.encode('utf-8'))
                except:
                    pass
            
            # Try MD5 (legacy format)
            if not password_valid:
                hashed_password = hashlib.md5(mat_khau.encode()).hexdigest()
                password_valid = (user.mat_khau_hash == hashed_password)
            
            if not password_valid:
                return JsonResponse({
                    'success': False,
                    'message': 'Số điện thoại hoặc mật khẩu không đúng'
                })
            
            # Check status (trang_thai is Boolean, not string)
            if not user.trang_thai:
                return JsonResponse({
                    'success': False,
                    'message': 'Tài khoản đã bị khóa. Vui lòng liên hệ quản trị viên.'
                })
            
            # Check role
            if user.vai_tro != 'khach_hang':
                return JsonResponse({
                    'success': False,
                    'message': 'Tài khoản không có quyền truy cập'
                })
            
            # Create session
            request.session['user_id'] = user.id
            request.session['vai_tro'] = user.vai_tro
            request.session['ho_ten'] = user.ho_ten
            
            # Determine redirect
            next_url = request.POST.get('next', '/customer/dashboard/')
            
            return JsonResponse({
                'success': True,
                'message': f'Chào mừng {user.ho_ten}!',
                'redirect': next_url
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Có lỗi xảy ra: {str(e)}'
            })


def customer_logout(request):
    """Customer logout"""
    # Clear session
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'vai_tro' in request.session:
        del request.session['vai_tro']
    if 'ho_ten' in request.session:
        del request.session['ho_ten']
    
    return redirect('/')


def forgot_password(request):
    """Forgot password - request OTP"""
    if request.method == 'GET':
        return render(request, 'customer/forgot_password.html')
    
    elif request.method == 'POST':
        try:
            so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
            
            if not so_dien_thoai:
                return JsonResponse({
                    'success': False,
                    'message': 'Vui lòng nhập số điện thoại'
                })
            
            # Check if user exists
            try:
                user = NguoiDung.objects.get(
                    so_dien_thoai=so_dien_thoai,
                    vai_tro='khach_hang',
                    da_xoa=False
                )
            except NguoiDung.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Số điện thoại chưa được đăng ký'
                })
            
            # Generate OTP (6 digits)
            import random
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            # Store OTP in session with expiry (5 minutes)
            request.session['reset_otp'] = otp
            request.session['reset_phone'] = so_dien_thoai
            request.session['otp_expiry'] = (timezone.now() + timedelta(minutes=5)).timestamp()
            
            # In production, send OTP via SMS
            # For now, just return it in response (for testing)
            print(f"OTP for {so_dien_thoai}: {otp}")
            
            return JsonResponse({
                'success': True,
                'message': f'Mã OTP đã được gửi đến số điện thoại {so_dien_thoai}',
                'otp': otp  # Remove this in production
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Có lỗi xảy ra: {str(e)}'
            })


@csrf_exempt
def verify_otp(request):
    """Verify OTP (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})
    
    try:
        otp = request.POST.get('otp', '').strip()
        
        if not otp:
            return JsonResponse({
                'success': False,
                'message': 'Vui lòng nhập mã OTP'
            })
        
        # Check if OTP exists in session
        if 'reset_otp' not in request.session:
            return JsonResponse({
                'success': False,
                'message': 'Mã OTP không hợp lệ hoặc đã hết hạn'
            })
        
        # Check expiry
        otp_expiry = request.session.get('otp_expiry', 0)
        if timezone.now().timestamp() > otp_expiry:
            # Clear expired OTP
            del request.session['reset_otp']
            del request.session['reset_phone']
            del request.session['otp_expiry']
            
            return JsonResponse({
                'success': False,
                'message': 'Mã OTP đã hết hạn. Vui lòng yêu cầu mã mới.'
            })
        
        # Verify OTP
        if otp != request.session['reset_otp']:
            return JsonResponse({
                'success': False,
                'message': 'Mã OTP không đúng'
            })
        
        # OTP verified - mark in session
        request.session['otp_verified'] = True
        
        return JsonResponse({
            'success': True,
            'message': 'Xác thực thành công'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Có lỗi xảy ra: {str(e)}'
        })


def reset_password(request):
    """Reset password after OTP verification"""
    if request.method == 'GET':
        # Check if OTP verified
        if not request.session.get('otp_verified'):
            return redirect('/accounts/forgot-password/')
        
        return render(request, 'customer/reset_password.html')
    
    elif request.method == 'POST':
        try:
            import hashlib
            
            # Check if OTP verified
            if not request.session.get('otp_verified'):
                return JsonResponse({
                    'success': False,
                    'message': 'Phiên làm việc đã hết hạn'
                })
            
            mat_khau_moi = request.POST.get('mat_khau_moi', '')
            xac_nhan_mat_khau = request.POST.get('xac_nhan_mat_khau', '')
            
            # Validate
            if len(mat_khau_moi) < 6:
                return JsonResponse({
                    'success': False,
                    'message': 'Mật khẩu phải có ít nhất 6 ký tự'
                })
            
            if mat_khau_moi != xac_nhan_mat_khau:
                return JsonResponse({
                    'success': False,
                    'message': 'Mật khẩu xác nhận không khớp'
                })
            
            # Get user
            so_dien_thoai = request.session.get('reset_phone')
            user = NguoiDung.objects.get(
                so_dien_thoai=so_dien_thoai,
                vai_tro='khach_hang',
                da_xoa=False
            )
            
            # Update password with bcrypt
            hashed_password = bcrypt.hashpw(mat_khau_moi.encode('utf-8'), bcrypt.gensalt())
            user.mat_khau_hash = hashed_password.decode('utf-8')
            user.save()
            
            # Clear session
            del request.session['reset_otp']
            del request.session['reset_phone']
            del request.session['otp_expiry']
            del request.session['otp_verified']
            
            return JsonResponse({
                'success': True,
                'message': 'Đặt lại mật khẩu thành công. Vui lòng đăng nhập.',
                'redirect': '/accounts/login/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Có lỗi xảy ra: {str(e)}'
            })


@csrf_exempt
def send_otp(request):
    """Resend OTP (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})
    
    try:
        # Check if phone number in session
        if 'reset_phone' not in request.session:
            return JsonResponse({
                'success': False,
                'message': 'Phiên làm việc đã hết hạn'
            })
        
        so_dien_thoai = request.session['reset_phone']
        
        # Generate new OTP
        import random
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Update session
        request.session['reset_otp'] = otp
        request.session['otp_expiry'] = (timezone.now() + timedelta(minutes=5)).timestamp()
        
        # In production, send OTP via SMS
        print(f"New OTP for {so_dien_thoai}: {otp}")
        
        return JsonResponse({
            'success': True,
            'message': 'Mã OTP mới đã được gửi',
            'otp': otp  # Remove this in production
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Có lỗi xảy ra: {str(e)}'
        })
