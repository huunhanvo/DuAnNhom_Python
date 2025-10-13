"""
Views for core app (Dashboard, Settings, Content)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum, Q, Avg, F
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
from decimal import Decimal
import json

# Import decorators
from .decorators import require_auth, require_role

# Import models (bạn sẽ import từ barbershop.models hoặc từ các app khác nếu cần)
from barbershop.models import (
    NguoiDung,
    DatLich,
    HoaDon,
    DichVu,
    CaiDatHeThong,
    DonXinNghi,
    ThongTinNhanVien,
    LichLamViec,
    Voucher,
    DanhMucDichVu,
)

# ============================================
# PUBLIC PAGES - CUSTOMER VIEWS
# ============================================

def home(request):
    """Trang chủ công khai"""
    from django.db.models import Avg
    
    # Get featured services
    featured_services = DichVu.objects.filter(
        trang_thai=True,
        da_xoa=False
    ).order_by('thu_tu')[:6]
    
    # Get top rated stylists
    top_stylists = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        trang_thai=True,
        da_xoa=False
    ).select_related('thong_tin_nhan_vien').order_by('-thong_tin_nhan_vien__danh_gia_trung_binh')[:4]
    
    # Get active promotions
    today = timezone.now().date()
    active_vouchers = Voucher.objects.filter(
        trang_thai=True,
        hien_thi_cong_khai=True,
        ngay_bat_dau__lte=today,
        ngay_ket_thuc__gte=today,
        da_xoa=False
    ).order_by('-gia_tri_giam')[:3]
    
    # Get recent reviews
    from barbershop.models import DanhGia
    recent_reviews = DanhGia.objects.filter(
        da_duyet=True,
        da_xoa=False
    ).select_related('khach_hang', 'nhan_vien').order_by('-ngay_tao')[:6]
    
    # Statistics
    total_customers = NguoiDung.objects.filter(vai_tro='khach_hang', da_xoa=False).count()
    total_services = DatLich.objects.filter(trang_thai='hoan_thanh', da_xoa=False).count()
    
    context = {
        'featured_services': featured_services,
        'top_stylists': top_stylists,
        'active_vouchers': active_vouchers,
        'recent_reviews': recent_reviews,
        'total_customers': total_customers,
        'total_services': total_services,
    }
    return render(request, 'customer/home.html', context)


def about(request):
    """Trang giới thiệu"""
    # Get team members (staff)
    team_members = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        trang_thai=True,
        da_xoa=False
    ).select_related('thong_tin_nhan_vien').order_by('-thong_tin_nhan_vien__kinh_nghiem_nam')
    
    # Get statistics
    total_customers = NguoiDung.objects.filter(vai_tro='khach_hang', da_xoa=False).count()
    total_services_completed = DatLich.objects.filter(trang_thai='hoan_thanh', da_xoa=False).count()
    years_experience = 10  # Mock data
    
    context = {
        'team_members': team_members,
        'total_customers': total_customers,
        'total_services_completed': total_services_completed,
        'years_experience': years_experience,
    }
    return render(request, 'customer/about.html', context)


def services(request):
    """Trang danh sách dịch vụ"""
    from barbershop.models import DanhMucDichVu
    
    # Get category filter
    category_id = request.GET.get('category')
    search = request.GET.get('search', '').strip()
    
    # Base query
    services_query = DichVu.objects.filter(
        trang_thai=True,
        da_xoa=False
    ).select_related('danh_muc')
    
    # Apply filters
    if category_id:
        services_query = services_query.filter(danh_muc_id=category_id)
    
    if search:
        services_query = services_query.filter(
            Q(ten_dich_vu__icontains=search) |
            Q(mo_ta_ngan__icontains=search) |
            Q(mo_ta_chi_tiet__icontains=search)
        )
    
    services_list = services_query.order_by('danh_muc__thu_tu', 'thu_tu')
    
    # Get all categories
    categories = DanhMucDichVu.objects.filter(
        trang_thai=True,
        da_xoa=False
    ).order_by('thu_tu')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(services_list, 12)
    page_number = request.GET.get('page', 1)
    services_page = paginator.get_page(page_number)
    
    context = {
        'services': services_page,
        'categories': categories,
        'selected_category': category_id,
        'search': search,
    }
    return render(request, 'customer/services.html', context)


def stylists(request):
    """Trang danh sách thợ cắt"""
    # Get filters
    specialty = request.GET.get('specialty', '').strip()
    sort_by = request.GET.get('sort', 'rating')
    
    # Base query
    stylists_query = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        trang_thai=True,
        da_xoa=False
    ).select_related('thong_tin_nhan_vien')
    
    # Apply specialty filter
    if specialty:
        stylists_query = stylists_query.filter(
            thong_tin_nhan_vien__chuyen_mon__icontains=specialty
        )
    
    # Apply sorting
    if sort_by == 'rating':
        stylists_query = stylists_query.order_by('-thong_tin_nhan_vien__danh_gia_trung_binh')
    elif sort_by == 'experience':
        stylists_query = stylists_query.order_by('-thong_tin_nhan_vien__kinh_nghiem_nam')
    elif sort_by == 'name':
        stylists_query = stylists_query.order_by('ho_ten')
    else:
        stylists_query = stylists_query.order_by('-thong_tin_nhan_vien__tong_luot_phuc_vu')
    
    # Add booking count annotation
    stylists_list = stylists_query.annotate(
        total_bookings=Count('dat_lich_nhan_vien', filter=Q(dat_lich_nhan_vien__trang_thai='hoan_thanh', dat_lich_nhan_vien__da_xoa=False))
    )
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(stylists_list, 12)
    page_number = request.GET.get('page', 1)
    stylists_page = paginator.get_page(page_number)
    
    context = {
        'stylists': stylists_page,
        'specialty': specialty,
        'sort_by': sort_by,
    }
    return render(request, 'customer/stylists.html', context)


def stylist_detail(request, stylist_id):
    """Trang chi tiết thợ cắt"""
    stylist = get_object_or_404(
        NguoiDung,
        id=stylist_id,
        vai_tro='nhan_vien',
        trang_thai=True,
        da_xoa=False
    )
    
    # Get stylist info
    staff_info = None
    try:
        staff_info = stylist.thong_tin_nhan_vien
    except:
        pass
    
    # Get statistics
    total_services = DatLich.objects.filter(
        nhan_vien=stylist,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).count()
    
    total_customers = DatLich.objects.filter(
        nhan_vien=stylist,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).values('khach_hang').distinct().count()
    
    # Get reviews
    from barbershop.models import DanhGia
    reviews = DanhGia.objects.filter(
        nhan_vien=stylist,
        da_duyet=True,
        da_xoa=False
    ).select_related('khach_hang').order_by('-ngay_tao')[:10]
    
    # Rating distribution
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for review in DanhGia.objects.filter(nhan_vien=stylist, da_xoa=False):
        rating_counts[review.so_sao] = rating_counts.get(review.so_sao, 0) + 1
    
    # Skills and certificates
    skills = []
    certificates = []
    if staff_info:
        if staff_info.chuyen_mon:
            skills = [s.strip() for s in staff_info.chuyen_mon.split(',') if s.strip()]
        if staff_info.chung_chi:
            certificates = [c.strip() for c in staff_info.chung_chi.split(',') if c.strip()]
    
    # Check if current user has favorited this stylist
    is_favorite = False
    if request.session.get('user_id'):
        from barbershop.models import StylistYeuThich
        is_favorite = StylistYeuThich.objects.filter(
            khach_hang_id=request.session['user_id'],
            stylist=stylist
        ).exists()
    
    context = {
        'stylist': stylist,
        'staff_info': staff_info,
        'total_services': total_services,
        'total_customers': total_customers,
        'reviews': reviews,
        'rating_counts': rating_counts,
        'skills': skills,
        'certificates': certificates,
        'is_favorite': is_favorite,
    }
    return render(request, 'customer/stylist_detail.html', context)


def promotions(request):
    """Trang khuyến mãi"""
    today = timezone.now().date()
    
    # Get active vouchers
    vouchers = Voucher.objects.filter(
        trang_thai=True,
        ngay_bat_dau__lte=today,
        ngay_ket_thuc__gte=today,
        da_xoa=False
    ).order_by('-gia_tri_giam')
    
    # Separate public and VIP vouchers
    public_vouchers = vouchers.filter(hien_thi_cong_khai=True)
    
    # Get rewards (if user is logged in)
    rewards = []
    user_points = 0
    if request.session.get('user_id'):
        from barbershop.models import QuaTangDiem
        user = NguoiDung.objects.get(id=request.session['user_id'])
        user_points = user.diem_tich_luy or 0
        
        rewards = QuaTangDiem.objects.filter(
            trang_thai=True,
            da_xoa=False,
            so_luong_con_lai__gt=0
        ).order_by('diem_yeu_cau')[:6]
    
    context = {
        'vouchers': public_vouchers,
        'rewards': rewards,
        'user_points': user_points,
    }
    return render(request, 'customer/promotions.html', context)


# ============ VIEWS - Bạn sẽ copy code vào đây ============
# Các views sẽ được di chuyển vào đây:
# - login_view, logout_view, page_not_found (GIỮ LẠI trong barbershop/views.py)
# - admin_dashboard
@require_role(['quan_ly'])
def admin_dashboard(request):
    """Admin Dashboard"""
    today = timezone.now().date()
    
    # Today's bookings
    today_bookings = DatLich.objects.filter(
        ngay_hen=today,
        da_xoa=False
    ).exclude(trang_thai='da_huy')
    
    # Today's revenue from invoices
    today_invoices = HoaDon.objects.filter(
        ngay_tao__date=today,
        da_xoa=False
    )
    today_revenue = today_invoices.aggregate(total=Sum('thanh_tien'))['total'] or 0
    
    # Total customers
    total_customers = NguoiDung.objects.filter(
        vai_tro='khach_hang',
        da_xoa=False
    ).count()
    
    # Pending bookings
    pending_bookings = DatLich.objects.filter(
        trang_thai='cho_xac_nhan',
        da_xoa=False
    ).count()
    
    # Revenue chart (last 7 days)
    revenue_chart_data = []
    revenue_chart_labels = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        daily_revenue = HoaDon.objects.filter(
            ngay_tao__date=date,
            da_xoa=False
        ).aggregate(total=Sum('thanh_tien'))['total'] or 0
        revenue_chart_data.append(float(daily_revenue))
        revenue_chart_labels.append(date.strftime('%d/%m'))
    
    # Top services
    top_services = DichVu.objects.filter(da_xoa=False).annotate(
        booking_count=Count('dichvudatlich', filter=Q(dichvudatlich__dat_lich__da_xoa=False))
    ).order_by('-booking_count')[:5]
    
    # Pending bookings for dashboard table
    pending_bookings_list = DatLich.objects.filter(
        trang_thai='cho_xac_nhan',
        da_xoa=False
    ).select_related('khach_hang', 'nhan_vien').order_by('ngay_hen', 'gio_hen')[:10]
    
    # Pending leave requests
    pending_leave_requests = DonXinNghi.objects.filter(
        trang_thai='cho_duyet',
        da_xoa=False
    ).select_related('nhan_vien').order_by('ngay_tao')[:10]
    
    # Upcoming bookings today
    upcoming_bookings = DatLich.objects.filter(
        ngay_hen=today,
        da_xoa=False
    ).exclude(trang_thai='da_huy').select_related(
        'khach_hang', 'nhan_vien'
    ).order_by('gio_hen')[:5]
    
    context = {
        'today_bookings': today_bookings.count(),
        'today_revenue': today_revenue,
        'total_customers': total_customers,
        'pending_bookings': pending_bookings,
        'pending_bookings_list': pending_bookings_list,
        'pending_leave_requests': pending_leave_requests,
        'revenue_chart_labels': revenue_chart_labels,
        'revenue_chart_data': revenue_chart_data,
        'top_services': top_services,
        'upcoming_bookings': upcoming_bookings,
    }
    return render(request, 'admin/dashboard.html', context)
# - staff_dashboard
@require_role(['nhan_vien', 'quan_ly'])
def staff_dashboard(request):
    """Staff Dashboard"""
    user_id = request.session.get('user_id')
    today = timezone.now().date()
    
    # Get staff info
    staff = NguoiDung.objects.get(id=user_id)
    staff_info = ThongTinNhanVien.objects.filter(nguoi_dung_id=user_id).first()
    
    # Today's bookings for this staff
    today_bookings = DatLich.objects.filter(
        nhan_vien_id=user_id,
        ngay_hen=today,
        da_xoa=False
    ).exclude(trang_thai='da_huy').select_related('khach_hang').order_by('gio_hen')
    
    # Count today's bookings by status
    waiting_checkin = today_bookings.filter(trang_thai='da_xac_nhan').count()
    
    # Today's schedule
    today_schedule = LichLamViec.objects.filter(
        nhan_vien_id=user_id,
        ngay_lam=today,
        da_xoa=False
    ).first()
    
    # This month statistics
    from django.db.models import Sum
    month_start = today.replace(day=1)
    
    month_completed_bookings = DatLich.objects.filter(
        nhan_vien_id=user_id,
        ngay_hen__gte=month_start,
        ngay_hen__lte=today,
        da_xoa=False,
        trang_thai='hoan_thanh'
    )
    
    month_bookings_count = month_completed_bookings.count()
    month_revenue = month_completed_bookings.aggregate(
        total=Sum('thanh_tien')
    )['total'] or 0
    
    # Average revenue per booking
    avg_revenue = month_revenue / month_bookings_count if month_bookings_count > 0 else 0
    
    # Next booking
    next_booking = today_bookings.filter(
        trang_thai__in=['da_xac_nhan', 'da_checkin']
    ).first()
    
    # Staff rating
    staff_rating = staff_info.danh_gia_trung_binh if staff_info else 0
    total_services = staff_info.tong_luot_phuc_vu if staff_info else 0
    
    context = {
        'staff': staff,
        'today_bookings': today_bookings,
        'today_schedule': today_schedule,
        'booking_count': today_bookings.count(),
        'waiting_checkin': waiting_checkin,
        'month_bookings_count': month_bookings_count,
        'month_revenue': month_revenue,
        'avg_revenue': avg_revenue,
        'next_booking': next_booking,
        'staff_rating': staff_rating,
        'total_services': total_services,
    }
    return render(request, 'staff/dashboard.html', context)

# - admin_settings
@require_role(['quan_ly'])
def admin_settings(request):
    """System Settings"""
    settings = CaiDatHeThong.get_settings()
    
    # Prepare days of week data for template
    days_of_week = [
        {'name': 'Thá»© 2', 'key': 'monday'},
        {'name': 'Thá»© 3', 'key': 'tuesday'},
        {'name': 'Thá»© 4', 'key': 'wednesday'},
        {'name': 'Thá»© 5', 'key': 'thursday'},
        {'name': 'Thá»© 6', 'key': 'friday'},
        {'name': 'Thá»© 7', 'key': 'saturday'},
        {'name': 'Chá»§ nháº­t', 'key': 'sunday'},
    ]
    
    for day in days_of_week:
        day['is_open'] = settings.ngay_lam_viec.get(day['key'], True)
        day['open_time'] = settings.gio_mo_cua
        day['close_time'] = settings.gio_dong_cua
    
    context = {
        'settings': settings,
        'days_of_week': days_of_week,
        'last_backup': settings.lan_sao_luu_cuoi,
    }
    return render(request, 'admin/settings.html', context)
# - admin_settings_api_general
@require_role(['quan_ly'])  
def admin_settings_api_general(request):
    """API endpoint for general settings"""
    if request.method == 'POST':
        try:
            settings = CaiDatHeThong.get_settings()
            
            # Update general fields
            settings.ten_tiem = request.POST.get('ten_tiem', settings.ten_tiem)
            settings.hotline = request.POST.get('hotline', settings.hotline)
            settings.dia_chi = request.POST.get('dia_chi', settings.dia_chi)
            settings.email = request.POST.get('email', settings.email)
            settings.website = request.POST.get('website', settings.website)
            settings.mo_ta = request.POST.get('mo_ta', settings.mo_ta)
            
            # Handle logo upload
            if 'logo' in request.FILES:
                logo_file = request.FILES['logo']
                # Simple file handling - in production, use proper storage
                logo_path = f'uploads/logos/{logo_file.name}'
                settings.logo = logo_path
            
            settings.save()
            
            return JsonResponse({'success': True, 'message': 'ÄÃ£ lÆ°u thÃ´ng tin chung thÃ nh cÃ´ng!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

# - admin_settings_api_business_hours
@require_role(['quan_ly'])
def admin_settings_api_business_hours(request):
    """API endpoint for business hours settings"""
    if request.method == 'POST':
        try:
            settings = CaiDatHeThong.get_settings()
            
            # Update working days
            ngay_lam_viec = {}
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            for day in days:
                ngay_lam_viec[day] = request.POST.get(f'{day}_open') == 'on'
            
            settings.ngay_lam_viec = ngay_lam_viec
            settings.gio_mo_cua = request.POST.get('gio_mo_cua', settings.gio_mo_cua)
            settings.gio_dong_cua = request.POST.get('gio_dong_cua', settings.gio_dong_cua)
            settings.thoi_gian_slot = int(request.POST.get('slot_duration', 30))
            
            settings.save()
            
            return JsonResponse({'success': True, 'message': 'ÄÃ£ cáº­p nháº­t giá» lÃ m viá»c thÃ nh cÃ´ng!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - admin_settings_api_services
@require_role(['quan_ly'])
def admin_settings_api_services(request):
    """API endpoint for service settings"""
    if request.method == 'POST':
        try:
            settings = CaiDatHeThong.get_settings()
            
            settings.tu_dong_xac_nhan = request.POST.get('auto_confirm') == 'on'
            settings.cho_phep_chon_nhan_vien = request.POST.get('allow_staff_select') == 'on'
            settings.yeu_cau_dat_coc = request.POST.get('require_deposit') == 'on'
            
            if settings.yeu_cau_dat_coc:
                settings.so_tien_dat_coc = float(request.POST.get('deposit_amount', 50000))
                settings.loai_dat_coc = request.POST.get('deposit_type', 'VND')
            
            settings.save()
            
            return JsonResponse({'success': True, 'message': 'ÄÃ£ cáº­p nháº­t cÃ i Äáº·t dá»ch vá»¥ thÃ nh cÃ´ng!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - admin_settings_api_payments
@require_role(['quan_ly'])
def admin_settings_api_payments(request):
    """API endpoint for payment settings"""
    if request.method == 'POST':
        try:
            settings = CaiDatHeThong.get_settings()
            
            settings.thanh_toan_tien_mat = request.POST.get('cash_enabled') == 'on'
            settings.thanh_toan_the = request.POST.get('card_enabled') == 'on'
            settings.thanh_toan_chuyen_khoan = request.POST.get('bank_enabled') == 'on'
            settings.so_tai_khoan = request.POST.get('bank_account', settings.so_tai_khoan)
            settings.ten_ngan_hang = request.POST.get('bank_name', settings.ten_ngan_hang)
            
            settings.thanh_toan_momo = request.POST.get('momo_enabled') == 'on'
            settings.so_dien_thoai_momo = request.POST.get('momo_phone', settings.so_dien_thoai_momo)
            
            settings.thanh_toan_vnpay = request.POST.get('vnpay_enabled') == 'on'
            settings.vnpay_api_key = request.POST.get('vnpay_key', settings.vnpay_api_key)
            
            settings.save()
            
            return JsonResponse({'success': True, 'message': 'ÄÃ£ cáº­p nháº­t cÃ i Äáº·t thanh toÃ¡n thÃ nh cÃ´ng!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - admin_content
@require_role(['quan_ly'])
def admin_content(request):
    """Content Management - Placeholder"""
    context = {}
    return render(request, 'admin/content.html', context)


# ============================================
# CUSTOMER DASHBOARD VIEWS
# ============================================

@require_role(['khach_hang'])
def customer_dashboard(request):
    """Customer Dashboard"""
    user_id = request.session.get('user_id')
    customer = NguoiDung.objects.get(id=user_id)
    
    # Get statistics
    today = timezone.now().date()
    
    # Upcoming bookings
    upcoming_bookings = DatLich.objects.filter(
        khach_hang=customer,
        ngay_hen__gte=today,
        trang_thai__in=['cho_xac_nhan', 'da_xac_nhan'],
        da_xoa=False
    ).order_by('ngay_hen', 'gio_hen')[:5]
    
    # Completed bookings count
    completed_count = DatLich.objects.filter(
        khach_hang=customer,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).count()
    
    # Points and vouchers
    from barbershop.models import VoucherKhachHang
    points = customer.diem_tich_luy or 0
    available_vouchers = VoucherKhachHang.objects.filter(
        khach_hang=customer,
        trang_thai='chua_su_dung',
        voucher__ngay_ket_thuc__gte=today
    ).count()
    
    # Recent activity
    from barbershop.models import GiaoDichDiem
    recent_activity = []
    
    # Add booking activities
    recent_bookings = DatLich.objects.filter(
        khach_hang=customer,
        da_xoa=False
    ).order_by('-ngay_tao')[:5]
    
    for booking in recent_bookings:
        recent_activity.append({
            'type': 'booking',
            'icon': 'calendar-check',
            'title': f'Đặt lịch {booking.ma_dat_lich}',
            'description': f'Ngày {booking.ngay_hen.strftime("%d/%m/%Y")} lúc {booking.gio_hen.strftime("%H:%M")}',
            'date': booking.ngay_tao,
            'status': booking.trang_thai
        })
    
    # Add point transactions
    point_transactions = GiaoDichDiem.objects.filter(
        khach_hang=customer
    ).order_by('-ngay_giao_dich')[:5]
    
    for trans in point_transactions:
        recent_activity.append({
            'type': 'points',
            'icon': 'star',
            'title': trans.mo_ta,
            'description': f'{trans.so_diem} điểm',
            'date': trans.ngay_giao_dich,
            'points': trans.so_diem
        })
    
    # Sort by date
    recent_activity.sort(key=lambda x: x['date'], reverse=True)
    recent_activity = recent_activity[:10]
    
    # Favorite stylists count
    from barbershop.models import StylistYeuThich
    favorite_count = StylistYeuThich.objects.filter(khach_hang=customer).count()
    
    context = {
        'customer': customer,
        'upcoming_count': upcoming_bookings.count(),
        'completed_count': completed_count,
        'points': points,
        'vouchers_count': available_vouchers,
        'upcoming_bookings': upcoming_bookings,
        'recent_activity': recent_activity,
        'favorite_count': favorite_count,
    }
    return render(request, 'customer/customer_dashboard.html', context)


@require_role(['khach_hang'])
def customer_bookings(request):
    """Customer Bookings List"""
    user_id = request.session.get('user_id')
    customer = NguoiDung.objects.get(id=user_id)
    
    # Get filter
    status = request.GET.get('status', 'upcoming')
    
    # Base query
    bookings_query = DatLich.objects.filter(
        khach_hang=customer,
        da_xoa=False
    ).select_related('nhan_vien').prefetch_related('dich_vu_dat_lich__dich_vu')
    
    # Apply status filter
    today = timezone.now().date()
    if status == 'upcoming':
        bookings_query = bookings_query.filter(
            ngay_hen__gte=today,
            trang_thai__in=['cho_xac_nhan', 'da_xac_nhan']
        )
    elif status == 'pending':
        bookings_query = bookings_query.filter(trang_thai='cho_xac_nhan')
    elif status == 'completed':
        bookings_query = bookings_query.filter(trang_thai='hoan_thanh')
    elif status == 'cancelled':
        bookings_query = bookings_query.filter(trang_thai='da_huy')
    
    bookings_list = bookings_query.order_by('-ngay_hen', '-gio_hen')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(bookings_list, 10)
    page_number = request.GET.get('page', 1)
    bookings_page = paginator.get_page(page_number)
    
    # Count by status
    upcoming_count = DatLich.objects.filter(
        khach_hang=customer,
        ngay_hen__gte=today,
        trang_thai__in=['cho_xac_nhan', 'da_xac_nhan'],
        da_xoa=False
    ).count()
    
    pending_count = DatLich.objects.filter(
        khach_hang=customer,
        trang_thai='cho_xac_nhan',
        da_xoa=False
    ).count()
    
    completed_count = DatLich.objects.filter(
        khach_hang=customer,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).count()
    
    cancelled_count = DatLich.objects.filter(
        khach_hang=customer,
        trang_thai='da_huy',
        da_xoa=False
    ).count()
    
    context = {
        'bookings': bookings_page,
        'status': status,
        'upcoming_count': upcoming_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
    }
    return render(request, 'customer/customer_bookings.html', context)


@require_role(['khach_hang'])
def customer_booking_detail(request, booking_id):
    """Customer Booking Detail"""
    user_id = request.session.get('user_id')
    customer = NguoiDung.objects.get(id=user_id)
    
    booking = get_object_or_404(
        DatLich,
        id=booking_id,
        khach_hang=customer,
        da_xoa=False
    )
    
    # Get services
    services = booking.dich_vu_dat_lich.all().select_related('dich_vu')
    
    # Check if can cancel (at least 1 hour before)
    can_cancel = False
    if booking.trang_thai in ['cho_xac_nhan', 'da_xac_nhan']:
        booking_datetime = datetime.combine(booking.ngay_hen, booking.gio_hen)
        time_diff = booking_datetime - timezone.now()
        if time_diff.total_seconds() > 3600:  # 1 hour
            can_cancel = True
    
    # Check if can review
    can_review = False
    has_review = False
    if booking.trang_thai == 'hoan_thanh':
        from barbershop.models import DanhGia
        has_review = DanhGia.objects.filter(
            khach_hang=customer,
            dat_lich=booking,
            da_xoa=False
        ).exists()
        can_review = not has_review
    
    context = {
        'booking': booking,
        'services': services,
        'can_cancel': can_cancel,
        'can_review': can_review,
        'has_review': has_review,
    }
    return render(request, 'customer/customer_booking_detail.html', context)


@require_role(['khach_hang'])
def customer_history(request):
    """Customer Service History"""
    user_id = request.session.get('user_id')
    customer = NguoiDung.objects.get(id=user_id)
    
    # Get date range filter
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    # Base query - completed bookings
    history_query = DatLich.objects.filter(
        khach_hang=customer,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).select_related('nhan_vien').prefetch_related('dich_vu_dat_lich__dich_vu')
    
    # Apply date filter
    if from_date:
        history_query = history_query.filter(ngay_hen__gte=from_date)
    if to_date:
        history_query = history_query.filter(ngay_hen__lte=to_date)
    
    history_list = history_query.order_by('-ngay_hen', '-gio_hen')
    
    # Statistics
    total_completed = history_list.count()
    total_spent = sum(booking.thanh_tien for booking in history_list)
    
    # Average rating
    from barbershop.models import DanhGia
    avg_rating = DanhGia.objects.filter(
        khach_hang=customer,
        da_xoa=False
    ).aggregate(avg=Avg('so_sao'))['avg'] or 0
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(history_list, 10)
    page_number = request.GET.get('page', 1)
    history_page = paginator.get_page(page_number)
    
    context = {
        'history': history_page,
        'total_completed': total_completed,
        'total_spent': total_spent,
        'avg_rating': avg_rating,
        'from_date': from_date,
        'to_date': to_date,
    }
    return render(request, 'customer/customer_history.html', context)


@csrf_exempt
@require_role(['khach_hang'])
def cancel_booking(request, booking_id):
    """Cancel booking (AJAX)"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            customer = NguoiDung.objects.get(id=user_id)
            
            booking = get_object_or_404(
                DatLich,
                id=booking_id,
                khach_hang=customer,
                da_xoa=False
            )
            
            # Check if can cancel
            if booking.trang_thai not in ['cho_xac_nhan', 'da_xac_nhan']:
                return JsonResponse({
                    'success': False,
                    'message': 'Không thể hủy lịch hẹn này'
                })
            
            # Check time
            booking_datetime = datetime.combine(booking.ngay_hen, booking.gio_hen)
            time_diff = booking_datetime - timezone.now()
            if time_diff.total_seconds() <= 3600:
                return JsonResponse({
                    'success': False,
                    'message': 'Chỉ có thể hủy lịch trước 1 giờ'
                })
            
            # Cancel booking
            booking.trang_thai = 'da_huy'
            booking.ly_do_huy = request.POST.get('reason', 'Khách hàng hủy')
            booking.ngay_huy = timezone.now()
            booking.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Đã hủy lịch hẹn thành công'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Có lỗi xảy ra: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})


# ==================== REWARDS & PROFILE VIEWS ====================

@require_role(['khach_hang'])
def customer_rewards(request):
    """Customer rewards and points page"""
    customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
    
    # Get available rewards
    from barbershop.models import QuaTangDiem
    rewards = QuaTangDiem.objects.filter(
        da_xoa=False,
        so_luong_con_lai__gt=0
    ).order_by('diem_yeu_cau')
    
    # Get customer's vouchers
    from barbershop.models import VoucherKhachHang
    customer_vouchers = VoucherKhachHang.objects.filter(
        khach_hang=customer
    ).select_related('voucher').order_by('-ngay_nhan')
    
    # Update expired vouchers
    for cv in customer_vouchers:
        cv.check_het_han()
    
    # Get point transaction history
    from barbershop.models import GiaoDichDiem
    transactions = GiaoDichDiem.objects.filter(
        khach_hang=customer
    ).order_by('-ngay_giao_dich')[:20]
    
    # Get redemption history
    from barbershop.models import LichSuDoiQua
    redemptions = LichSuDoiQua.objects.filter(
        khach_hang=customer
    ).select_related('qua_tang').order_by('-ngay_doi')[:10]
    
    # Calculate membership tier
    points = customer.diem_tich_luy or 0
    if points >= 1000:
        tier = {'name': 'Platinum', 'color': '#E5E4E2', 'next': None}
    elif points >= 500:
        tier = {'name': 'Gold', 'color': '#FFD700', 'next': 1000 - points}
    elif points >= 200:
        tier = {'name': 'Silver', 'color': '#C0C0C0', 'next': 500 - points}
    else:
        tier = {'name': 'Bronze', 'color': '#CD7F32', 'next': 200 - points}
    
    context = {
        'customer': customer,
        'rewards': rewards,
        'customer_vouchers': customer_vouchers,
        'transactions': transactions,
        'redemptions': redemptions,
        'tier': tier,
    }
    return render(request, 'customer/customer_rewards.html', context)


@csrf_exempt
@require_role(['khach_hang'])
def redeem_reward(request, reward_id):
    """AJAX endpoint to redeem a reward with points"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})
    
    try:
        from barbershop.models import QuaTangDiem, GiaoDichDiem, LichSuDoiQua, VoucherKhachHang
        
        customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
        reward = get_object_or_404(QuaTangDiem, id=reward_id, da_xoa=False)
        
        # Check if reward is available
        if reward.so_luong_con_lai <= 0:
            return JsonResponse({'success': False, 'message': 'Phần thưởng đã hết'})
        
        # Check if customer has enough points
        customer_points = customer.diem_tich_luy or 0
        if customer_points < reward.diem_yeu_cau:
            return JsonResponse({
                'success': False, 
                'message': f'Bạn cần thêm {reward.diem_yeu_cau - customer_points} điểm'
            })
        
        # Deduct points
        points_before = customer_points
        customer.diem_tich_luy = customer_points - reward.diem_yeu_cau
        customer.save()
        
        # Record point transaction
        GiaoDichDiem.objects.create(
            khach_hang=customer,
            loai_giao_dich='tru',
            so_diem=reward.diem_yeu_cau,
            diem_truoc=points_before,
            diem_sau=customer.diem_tich_luy,
            mo_ta=f'Đổi quà: {reward.ten_qua}'
        )
        
        # Create redemption record
        redemption = LichSuDoiQua.objects.create(
            khach_hang=customer,
            qua_tang=reward,
            diem_da_dung=reward.diem_yeu_cau,
            trang_thai='cho_xu_ly'
        )
        
        # Decrease reward quantity
        reward.so_luong_con_lai -= 1
        reward.save()
        
        # If reward is a voucher, create customer voucher
        if reward.loai_giam:
            voucher_code = f'REWARD{customer.id}{reward.id}{timezone.now().strftime("%Y%m%d%H%M%S")}'
            ngay_het_han = timezone.now() + timezone.timedelta(days=reward.thoi_han_su_dung)
            
            VoucherKhachHang.objects.create(
                khach_hang=customer,
                voucher=None,  # This is a reward-based voucher
                ma_voucher=voucher_code,
                loai_giam=reward.loai_giam,
                gia_tri_giam=reward.gia_tri_giam,
                ngay_het_han=ngay_het_han,
                trang_thai='chua_su_dung',
                ghi_chu=f'Đổi từ quà tặng: {reward.ten_qua}'
            )
            
            message = f'Đổi quà thành công! Mã voucher: {voucher_code}'
        else:
            message = 'Đổi quà thành công! Chúng tôi sẽ liên hệ bạn sớm'
        
        return JsonResponse({
            'success': True, 
            'message': message,
            'new_points': customer.diem_tich_luy
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_role(['khach_hang'])
def customer_profile(request):
    """Customer profile view"""
    customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
    
    # Get customer statistics
    total_bookings = DatLich.objects.filter(
        khach_hang=customer,
        da_xoa=False
    ).count()
    
    completed_bookings = DatLich.objects.filter(
        khach_hang=customer,
        trang_thai='hoan_thanh',
        da_xoa=False
    ).count()
    
    total_spent = HoaDon.objects.filter(
        khach_hang=customer,
        da_xoa=False
    ).aggregate(total=Sum('thanh_tien'))['total'] or 0
    
    # Get favorite stylists
    from barbershop.models import StylistYeuThich
    favorite_stylists = StylistYeuThich.objects.filter(
        khach_hang=customer
    ).select_related('stylist__thong_tin_nhan_vien')
    
    # Calculate membership info
    points = customer.diem_tich_luy or 0
    if points >= 1000:
        tier = {'name': 'Platinum', 'color': '#E5E4E2', 'benefits': ['Ưu tiên đặt lịch', 'Giảm 15%', 'Quà tặng đặc biệt']}
    elif points >= 500:
        tier = {'name': 'Gold', 'color': '#FFD700', 'benefits': ['Ưu tiên đặt lịch', 'Giảm 10%', 'Voucher sinh nhật']}
    elif points >= 200:
        tier = {'name': 'Silver', 'color': '#C0C0C0', 'benefits': ['Giảm 5%', 'Voucher sinh nhật']}
    else:
        tier = {'name': 'Bronze', 'color': '#CD7F32', 'benefits': ['Tích điểm thưởng']}
    
    # Generate referral code
    referral_code = f'REF{customer.id:05d}'
    
    context = {
        'customer': customer,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'total_spent': total_spent,
        'favorite_stylists': favorite_stylists,
        'tier': tier,
        'referral_code': referral_code,
    }
    return render(request, 'customer/customer_profile.html', context)


@csrf_exempt
@require_role(['khach_hang'])
def update_profile(request):
    """AJAX endpoint to update customer profile"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})
    
    try:
        customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
        
        # Update basic info
        customer.ho_ten = request.POST.get('ho_ten', customer.ho_ten)
        customer.so_dien_thoai = request.POST.get('so_dien_thoai', customer.so_dien_thoai)
        customer.email = request.POST.get('email', customer.email)
        customer.dia_chi = request.POST.get('dia_chi', customer.dia_chi)
        
        # Update birthday if provided
        ngay_sinh = request.POST.get('ngay_sinh')
        if ngay_sinh:
            from datetime import datetime
            customer.ngay_sinh = datetime.strptime(ngay_sinh, '%Y-%m-%d').date()
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            avatar_file = request.FILES['avatar']
            # Save to media/avatars/
            import os
            from django.conf import settings
            
            # Create directory if not exists
            avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
            os.makedirs(avatar_dir, exist_ok=True)
            
            # Generate unique filename
            ext = avatar_file.name.split('.')[-1]
            filename = f'customer_{customer.id}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{ext}'
            filepath = os.path.join(avatar_dir, filename)
            
            # Save file
            with open(filepath, 'wb+') as destination:
                for chunk in avatar_file.chunks():
                    destination.write(chunk)
            
            customer.anh_dai_dien = f'avatars/{filename}'
        
        customer.save()
        
        # Update session
        request.session['ho_ten'] = customer.ho_ten
        
        return JsonResponse({
            'success': True, 
            'message': 'Cập nhật thông tin thành công',
            'avatar_url': customer.anh_dai_dien if customer.anh_dai_dien else None
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@require_role(['khach_hang'])
def change_password(request):
    """AJAX endpoint to change password"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})
    
    try:
        customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
        
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate current password
        import hashlib
        hashed_current = hashlib.md5(current_password.encode()).hexdigest()
        if customer.mat_khau != hashed_current:
            return JsonResponse({'success': False, 'message': 'Mật khẩu hiện tại không đúng'})
        
        # Validate new password
        if len(new_password) < 6:
            return JsonResponse({'success': False, 'message': 'Mật khẩu mới phải có ít nhất 6 ký tự'})
        
        if new_password != confirm_password:
            return JsonResponse({'success': False, 'message': 'Mật khẩu xác nhận không khớp'})
        
        # Update password
        customer.mat_khau = hashlib.md5(new_password.encode()).hexdigest()
        customer.save()
        
        return JsonResponse({'success': True, 'message': 'Đổi mật khẩu thành công'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_role(['khach_hang'])
def customer_favorite_stylists(request):
    """Customer favorite stylists management page"""
    customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
    
    # Get all stylists
    all_stylists = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        trang_thai=True,  # BooleanField, not CharField
        da_xoa=False
    ).annotate(
        total_bookings=Count('dat_lich_nhan_vien', filter=Q(dat_lich_nhan_vien__trang_thai='hoan_thanh'))
    ).select_related('thong_tin_nhan_vien').order_by('-total_bookings')
    
    # Get customer's favorites
    from barbershop.models import StylistYeuThich
    favorite_ids = StylistYeuThich.objects.filter(
        khach_hang=customer
    ).values_list('stylist_id', flat=True)
    
    # Mark favorites
    from barbershop.models import DanhGia
    for stylist in all_stylists:
        stylist.is_favorite = stylist.id in favorite_ids
        
        # Get average rating
        avg_rating = DanhGia.objects.filter(
            nhan_vien=stylist,
            da_duyet=True,
            da_xoa=False
        ).aggregate(avg=Avg('danh_gia_stylist'))['avg']
        stylist.avg_rating = round(avg_rating, 1) if avg_rating else 0
    
    context = {
        'all_stylists': all_stylists,
    }
    return render(request, 'customer/customer_favorite_stylists.html', context)


@csrf_exempt
@require_role(['khach_hang'])
def toggle_favorite(request, stylist_id):
    """AJAX endpoint to add/remove favorite stylist"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})
    
    try:
        from barbershop.models import StylistYeuThich
        
        customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
        stylist = get_object_or_404(NguoiDung, id=stylist_id, vai_tro='nhan_vien')
        
        # Check if already favorite
        favorite = StylistYeuThich.objects.filter(
            khach_hang=customer,
            stylist=stylist
        ).first()
        
        if favorite:
            # Remove from favorites (hard delete since no da_xoa field)
            favorite.delete()
            is_favorite = False
            message = 'Đã xóa khỏi danh sách yêu thích'
        else:
            # Add to favorites
            StylistYeuThich.objects.create(
                khach_hang=customer,
                stylist=stylist
            )
            is_favorite = True
            message = 'Đã thêm vào danh sách yêu thích'
        
        # Get new count
        favorite_count = StylistYeuThich.objects.filter(
            khach_hang=customer
        ).count()
        
        return JsonResponse({
            'success': True, 
            'message': message,
            'is_favorite': is_favorite,
            'favorite_count': favorite_count
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# ==================== REVIEW SYSTEM ====================

@csrf_exempt
@require_role(['khach_hang'])
def customer_review(request, booking_id):
    """Submit customer review with images"""
    if request.method == 'GET':
        # Show review form
        customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
        booking = get_object_or_404(
            DatLich,
            id=booking_id,
            khach_hang=customer,
            trang_thai='hoan_thanh',
            da_xoa=False
        )
        
        # Check if already reviewed
        from barbershop.models import DanhGia
        existing_review = DanhGia.objects.filter(
            khach_hang=customer,
            dat_lich=booking,
            da_xoa=False
        ).first()
        
        if existing_review:
            return render(request, 'customer/review_submitted.html', {
                'review': existing_review,
                'booking': booking
            })
        
        # Get services from booking
        services = booking.dich_vu_dat_lich.all().select_related('dich_vu')
        
        context = {
            'booking': booking,
            'services': services,
        }
        return render(request, 'customer/customer_review.html', context)
    
    elif request.method == 'POST':
        # Submit review
        try:
            from barbershop.models import DanhGia
            import os
            import json
            from django.conf import settings
            
            customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
            booking = get_object_or_404(
                DatLich,
                id=booking_id,
                khach_hang=customer,
                trang_thai='hoan_thanh',
                da_xoa=False
            )
            
            # Check if already reviewed
            existing_review = DanhGia.objects.filter(
                khach_hang=customer,
                dat_lich=booking,
                da_xoa=False
            ).first()
            
            if existing_review:
                return JsonResponse({
                    'success': False,
                    'message': 'Bạn đã đánh giá lịch hẹn này rồi'
                })
            
            # Get review data
            so_sao = int(request.POST.get('so_sao', 5))
            danh_gia_stylist = int(request.POST.get('danh_gia_stylist', 5))
            noi_dung = request.POST.get('noi_dung', '').strip()
            
            # Validate
            if not noi_dung or len(noi_dung) < 10:
                return JsonResponse({
                    'success': False,
                    'message': 'Nội dung đánh giá phải có ít nhất 10 ký tự'
                })
            
            # Get quality checkboxes
            chuyen_nghiep = request.POST.get('chuyen_nghiep') == 'on'
            than_thien = request.POST.get('than_thien') == 'on'
            sach_se = request.POST.get('sach_se') == 'on'
            dung_gio = request.POST.get('dung_gio') == 'on'
            
            # Handle image uploads
            image_paths = []
            if 'images' in request.FILES:
                files = request.FILES.getlist('images')
                
                # Limit to 5 images
                if len(files) > 5:
                    return JsonResponse({
                        'success': False,
                        'message': 'Chỉ được upload tối đa 5 ảnh'
                    })
                
                # Create directory
                review_dir = os.path.join(settings.MEDIA_ROOT, 'reviews')
                os.makedirs(review_dir, exist_ok=True)
                
                # Save each image
                for idx, img_file in enumerate(files):
                    # Validate file type
                    ext = img_file.name.split('.')[-1].lower()
                    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                        continue
                    
                    # Generate unique filename
                    filename = f'review_{customer.id}_{booking.id}_{idx}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{ext}'
                    filepath = os.path.join(review_dir, filename)
                    
                    # Save file
                    with open(filepath, 'wb+') as destination:
                        for chunk in img_file.chunks():
                            destination.write(chunk)
                    
                    image_paths.append(f'reviews/{filename}')
            
            # Create review
            review = DanhGia.objects.create(
                khach_hang=customer,
                dat_lich=booking,
                nhan_vien=booking.nhan_vien,
                so_sao=so_sao,
                danh_gia_stylist=danh_gia_stylist,
                noi_dung=noi_dung,
                hinh_anh=json.dumps(image_paths) if image_paths else None,
                chuyen_nghiep=chuyen_nghiep,
                than_thien=than_thien,
                sach_se=sach_se,
                dung_gio=dung_gio,
                da_duyet=False  # Wait for approval
            )
            
            # Award points for review (e.g., 50 points)
            from barbershop.models import GiaoDichDiem
            points_reward = 50
            points_before = customer.diem_tich_luy or 0
            customer.diem_tich_luy = points_before + points_reward
            customer.save()
            
            GiaoDichDiem.objects.create(
                khach_hang=customer,
                loai_giao_dich='cong',
                so_diem=points_reward,
                diem_truoc=points_before,
                diem_sau=customer.diem_tich_luy,
                mo_ta=f'Thưởng đánh giá lịch hẹn {booking.ma_dat_lich}'
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Cảm ơn bạn đã đánh giá! Bạn nhận được {points_reward} điểm thưởng.',
                'points_earned': points_reward
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Có lỗi xảy ra: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
