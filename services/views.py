"""
Views for services app (Services, Promotions, Vouchers)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum, Q
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
from decimal import Decimal
import json
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill

# Import decorators from core
from core.decorators import require_auth, require_role

# Import models
from barbershop.models import (
    DichVu,
    DanhMucDichVu,
    Voucher,
    DatLich,
    HoaDon
)

# ============ VIEWS - Bạn sẽ copy code vào đây ============
# Các views sẽ được di chuyển vào đây:
# - admin_services
@require_role(['quan_ly'])
def admin_services(request):
    """Service Management with CRUD"""
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            # Create new service
            try:
                # Validation
                ten_dich_vu = request.POST.get('ten_dich_vu', '').strip()
                danh_muc = request.POST.get('danh_muc', '').strip()
                gia = request.POST.get('gia', '').strip()
                thoi_luong = request.POST.get('thoi_luong', '').strip()
                
                if not ten_dich_vu:
                    return JsonResponse({'success': False, 'message': 'TÃªn dá»ch vá»¥ khÃ´ng ÄÆ°á»£c Äá» trá»ng'})
                if not danh_muc:
                    return JsonResponse({'success': False, 'message': 'Danh má»¥c khÃ´ng ÄÆ°á»£c Äá» trá»ng'})
                if not gia:
                    return JsonResponse({'success': False, 'message': 'GiÃ¡ khÃ´ng ÄÆ°á»£c Äá» trá»ng'})
                if not thoi_luong:
                    return JsonResponse({'success': False, 'message': 'Thá»i lÆ°á»£ng khÃ´ng ÄÆ°á»£c Äá» trá»ng'})
                
                # Check if service name exists
                if DichVu.objects.filter(ten_dich_vu=ten_dich_vu, da_xoa=False).exists():
                    return JsonResponse({'success': False, 'message': f'TÃªn dá»ch vá»¥ {ten_dich_vu} ÄÃ£ tá»n táº¡i!'})
                
                # Get or create category based on name
                category_mapping = {
                    'haircut': 'Cáº¯t tÃ³c',
                    'shave': 'Cáº¡o rÃ¢u', 
                    'treatment': 'ChÄm sÃ³c',
                    'combo': 'Combo'
                }
                
                category_name = category_mapping.get(danh_muc, danh_muc)
                danh_muc_obj, created = DanhMucDichVu.objects.get_or_create(
                    ten_danh_muc=category_name,
                    defaults={'mo_ta': f'Danh má»¥c {category_name}', 'da_xoa': False}
                )
                
                # Handle image upload
                anh_minh_hoa = ''
                if 'anh_minh_hoa' in request.FILES:
                    import os
                    from django.core.files.storage import default_storage
                    from django.core.files.base import ContentFile
                    
                    uploaded_file = request.FILES['anh_minh_hoa']
                    # Generate unique filename
                    file_extension = uploaded_file.name.split('.')[-1]
                    file_name = f"service_{int(timezone.now().timestamp())}_{ten_dich_vu.replace(' ', '_')}.{file_extension}"
                    file_path = f"services/{file_name}"
                    
                    # Save file
                    path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
                    anh_minh_hoa = f"/media/{path}"
                
                service = DichVu.objects.create(
                    danh_muc=danh_muc_obj,
                    ten_dich_vu=ten_dich_vu,
                    mo_ta_ngan=request.POST.get('mo_ta', ''),
                    mo_ta_chi_tiet=request.POST.get('mo_ta', ''),
                    gia=int(gia),
                    thoi_gian_thuc_hien=int(thoi_luong),
                    anh_minh_hoa=anh_minh_hoa,
                    thu_tu=int(request.POST.get('thu_tu_hien_thi', 0)),
                    trang_thai=request.POST.get('trang_thai', 'active') == 'active',
                    da_xoa=False
                )
                return JsonResponse({'success': True, 'message': 'ÄÃ£ thÃªm dá»ch vá»¥ má»i!', 'service_id': service.id})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        elif action == 'update':
            # Update existing service
            try:
                service_id = request.POST.get('service_id')
                service = get_object_or_404(DichVu, id=service_id, da_xoa=False)
                
                ten_dich_vu = request.POST.get('ten_dich_vu', '').strip()
                danh_muc = request.POST.get('danh_muc', '').strip()
                gia = request.POST.get('gia', '').strip()
                thoi_luong = request.POST.get('thoi_luong', '').strip()
                
                # Check if service name exists (excluding current service)
                if DichVu.objects.filter(ten_dich_vu=ten_dich_vu, da_xoa=False).exclude(id=service_id).exists():
                    return JsonResponse({'success': False, 'message': f'TÃªn dá»ch vá»¥ {ten_dich_vu} ÄÃ£ tá»n táº¡i!'})
                
                # Get or create category
                category_mapping = {
                    'haircut': 'Cáº¯t tÃ³c',
                    'shave': 'Cáº¡o rÃ¢u', 
                    'treatment': 'ChÄm sÃ³c',
                    'combo': 'Combo'
                }
                
                category_name = category_mapping.get(danh_muc, danh_muc)
                danh_muc_obj, created = DanhMucDichVu.objects.get_or_create(
                    ten_danh_muc=category_name,
                    defaults={'mo_ta': f'Danh má»¥c {category_name}', 'da_xoa': False}
                )
                
                # Handle image upload for update
                if 'anh_minh_hoa' in request.FILES:
                    import os
                    from django.core.files.storage import default_storage
                    from django.core.files.base import ContentFile
                    
                    # Delete old image if exists
                    if service.anh_minh_hoa and service.anh_minh_hoa.startswith('/media/'):
                        old_path = service.anh_minh_hoa.replace('/media/', '')
                        if default_storage.exists(old_path):
                            default_storage.delete(old_path)
                    
                    uploaded_file = request.FILES['anh_minh_hoa']
                    file_extension = uploaded_file.name.split('.')[-1]
                    file_name = f"service_{int(timezone.now().timestamp())}_{ten_dich_vu.replace(' ', '_')}.{file_extension}"
                    file_path = f"services/{file_name}"
                    
                    path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
                    service.anh_minh_hoa = f"/media/{path}"
                
                service.danh_muc = danh_muc_obj
                service.ten_dich_vu = ten_dich_vu
                service.mo_ta_ngan = request.POST.get('mo_ta', '')
                service.mo_ta_chi_tiet = request.POST.get('mo_ta', '')
                service.gia = int(gia)
                service.thoi_gian_thuc_hien = int(thoi_luong)
                service.thu_tu = int(request.POST.get('thu_tu_hien_thi', 0))
                service.trang_thai = request.POST.get('trang_thai', 'active') == 'active'
                service.save()
                
                return JsonResponse({'success': True, 'message': 'ÄÃ£ cáº­p nháº­t dá»ch vá»¥!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        elif action == 'toggle_status':
            # Toggle active/inactive
            try:
                service_id = request.POST.get('service_id')
                service = get_object_or_404(DichVu, id=service_id, da_xoa=False)
                service.trang_thai = not service.trang_thai
                service.save()
                
                status_text = 'kÃ­ch hoáº¡t' if service.trang_thai else 'táº¡m ngá»«ng'
                return JsonResponse({'success': True, 'message': f'ÄÃ£ {status_text} dá»ch vá»¥!', 'new_status': service.trang_thai})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        elif action == 'delete':
            # Soft delete
            try:
                service_id = request.POST.get('service_id')
                service = get_object_or_404(DichVu, id=service_id, da_xoa=False)
                service.da_xoa = True
                service.ngay_xoa = timezone.now()
                service.save()
                
                return JsonResponse({'success': True, 'message': 'ÄÃ£ xÃ³a dá»ch vá»¥!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
    
    # GET request - display services
    from django.db.models import Count, Sum, Avg
    
    # Get all services with stats
    all_services = DichVu.objects.filter(
        da_xoa=False
    ).select_related('danh_muc').annotate(
        so_luot_dat=Count('dichvudatlich'),
        doanh_thu=Sum('dichvudatlich__dat_lich__hoa_don__thanh_tien')
    ).order_by('thu_tu', 'ten_dich_vu')
    
    # Add category field for template
    for service in all_services:
        if service.danh_muc:
            category_reverse_mapping = {
                'Cáº¯t tÃ³c': 'haircut',
                'Cáº¡o rÃ¢u': 'shave',
                'ChÄm sÃ³c': 'treatment', 
                'Combo': 'combo'
            }
            service.danh_muc_key = category_reverse_mapping.get(service.danh_muc.ten_danh_muc, 'haircut')
        else:
            service.danh_muc_key = 'haircut'
    
    # Statistics
    total_services = all_services.count()
    active_services = all_services.filter(trang_thai=True).count()
    avg_price = all_services.aggregate(avg_price=Avg('gia'))['avg_price'] or 0
    popular_service = all_services.order_by('-so_luot_dat').first()
    
    # Category counts
    haircut_count = all_services.filter(danh_muc__ten_danh_muc='Cáº¯t tÃ³c').count()
    shave_count = all_services.filter(danh_muc__ten_danh_muc='Cáº¡o rÃ¢u').count()
    treatment_count = all_services.filter(danh_muc__ten_danh_muc='ChÄm sÃ³c').count()
    combo_count = all_services.filter(danh_muc__ten_danh_muc='Combo').count()
    
    context = {
        'services': all_services,
        'total_services': total_services,
        'active_services': active_services,
        'avg_price': avg_price,
        'popular_service': popular_service or {'ten_dich_vu': 'ChÆ°a cÃ³'},
        'haircut_count': haircut_count,
        'shave_count': shave_count,
        'treatment_count': treatment_count,
        'combo_count': combo_count,
    }
    return render(request, 'admin/services.html', context)
# - api_service_crud
@require_role(['quan_ly'])
def api_service_crud(request, service_id=None):
    """API endpoint for service CRUD operations"""
    if request.method == 'GET' and service_id:
        return api_service_detail(request, service_id)
    
    elif request.method == 'POST':
        # Create new service
        return admin_services(request)
    
    elif request.method == 'PUT' and service_id:
        # Update service - convert PUT to POST
        request.POST = request.POST.copy()
        request.POST['action'] = 'update'
        request.POST['service_id'] = service_id
        return admin_services(request)
    
    elif request.method == 'DELETE' and service_id:
        # Delete service
        request.POST = request.POST.copy()
        request.POST['action'] = 'delete'
        request.POST['service_id'] = service_id
        return admin_services(request)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# - api_service_toggle_status
@require_role(['quan_ly'])
def api_service_toggle_status(request, service_id):
    """API endpoint to toggle service status"""
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['action'] = 'toggle_status'
        request.POST['service_id'] = service_id
        return admin_services(request)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
# - api_service_update_order
@require_role(['quan_ly'])
def api_service_update_order(request):
    """API endpoint to update service display order"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            order_list = data.get('order', [])
            
            for item in order_list:
                service_id = item.get('id')
                new_order = item.get('order')
                if service_id and new_order is not None:
                    DichVu.objects.filter(id=service_id, da_xoa=False).update(thu_tu=new_order)
            
            return JsonResponse({'success': True, 'message': 'ÄÃ£ cáº­p nháº­t thá»© tá»±!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
# - admin_promotions
@require_role(['quan_ly'])
def admin_promotions(request):
    """Promotion Management with Enhanced Stats, Filtering and CRUD"""
    from django.db.models import Count, Sum, Q, F
    from datetime import datetime, date
    from django.contrib import messages
    
    # Handle POST requests for CRUD operations
    if request.method == 'POST':
        try:
            voucher_id = request.POST.get('voucher_id')
            
            # Validation
            ma_voucher = request.POST.get('ma_voucher', '').strip()
            ten_voucher = request.POST.get('ten_voucher', '').strip()
            loai_giam = request.POST.get('loai_giam', '').strip()
            gia_tri_giam = request.POST.get('gia_tri_giam', '').strip()
            ngay_bat_dau = request.POST.get('ngay_bat_dau', '').strip()
            ngay_ket_thuc = request.POST.get('ngay_ket_thuc', '').strip()
            
            if not all([ma_voucher, ten_voucher, loai_giam, gia_tri_giam, ngay_bat_dau, ngay_ket_thuc]):
                messages.error(request, 'Vui lÃ²ng Äiá»n Äáº§y Äá»§ thÃ´ng tin báº¯t buá»c!')
                return redirect('services:admin_promotions')
            
            # Check for duplicate voucher code (exclude current when editing)
            existing_voucher = Voucher.objects.filter(ma_voucher=ma_voucher, da_xoa=False)
            if voucher_id:
                existing_voucher = existing_voucher.exclude(id=voucher_id)
            if existing_voucher.exists():
                messages.error(request, f'MÃ£ voucher "{ma_voucher}" ÄÃ£ tá»n táº¡i!')
                return redirect('services:admin_promotions')
            
            # Parse dates
            try:
                ngay_bat_dau_dt = datetime.strptime(ngay_bat_dau, '%Y-%m-%dT%H:%M')
                ngay_ket_thuc_dt = datetime.strptime(ngay_ket_thuc, '%Y-%m-%dT%H:%M')
                
                if ngay_bat_dau_dt >= ngay_ket_thuc_dt:
                    messages.error(request, 'NgÃ y káº¿t thÃºc pháº£i sau ngÃ y báº¯t Äáº§u!')
                    return redirect('services:admin_promotions')
                    
            except ValueError:
                messages.error(request, 'Äá»nh dáº¡ng ngÃ y giá» khÃ´ng há»£p lá»!')
                return redirect('services:admin_promotions')
            
            # Validate discount value
            try:
                gia_tri_giam_float = float(gia_tri_giam)
                if gia_tri_giam_float <= 0:
                    messages.error(request, 'GiÃ¡ trá» giáº£m pháº£i lá»n hÆ¡n 0!')
                    return redirect('services:admin_promotions')
                if loai_giam == 'phan_tram' and gia_tri_giam_float > 100:
                    messages.error(request, 'Giáº£m theo pháº§n trÄm khÃ´ng ÄÆ°á»£c vÆ°á»£t quÃ¡ 100%!')
                    return redirect('services:admin_promotions')
            except ValueError:
                messages.error(request, 'GiÃ¡ trá» giáº£m khÃ´ng há»£p lá»!')
                return redirect('services:admin_promotions')
            
            # Prepare data with correct field names from model
            voucher_data = {
                'ma_voucher': ma_voucher,
                'ten_voucher': ten_voucher,
                'mo_ta': request.POST.get('mo_ta', '').strip(),
                'loai_giam': loai_giam,
                'gia_tri_giam': gia_tri_giam_float,
                'gia_tri_don_toi_thieu': float(request.POST.get('gia_tri_don_hang_toi_thieu') or 0),  # Model field name
                'giam_toi_da': float(request.POST.get('gia_tri_giam_toi_da') or 0) or None,  # Model field name
                'ngay_bat_dau': ngay_bat_dau_dt.date(),  # Convert to date for DateField
                'ngay_ket_thuc': ngay_ket_thuc_dt.date(),  # Convert to date for DateField
                'so_luong_tong': int(request.POST.get('so_luong_toi_da') or 0) or None,  # Model field name
                'trang_thai': request.POST.get('trang_thai') == 'active',
            }
            
            if voucher_id:
                # Update existing voucher
                voucher = Voucher.objects.get(id=voucher_id, da_xoa=False)
                for key, value in voucher_data.items():
                    setattr(voucher, key, value)
                voucher.save()
                messages.success(request, f'ÄÃ£ cáº­p nháº­t voucher "{ma_voucher}" thÃ nh cÃ´ng!')
            else:
                # Create new voucher - Remove nguoi_tao field as it doesn't exist in Voucher model
                voucher = Voucher.objects.create(**voucher_data)
                messages.success(request, f'ÄÃ£ táº¡o voucher "{ma_voucher}" thÃ nh cÃ´ng!')
                
        except Exception as e:
            messages.error(request, f'CÃ³ lá»i xáº£y ra: {str(e)}')
        
        return redirect('services:admin_promotions')
    
    # Handle GET requests for listing and filtering
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    type_filter = request.GET.get('type', 'all')
    search = request.GET.get('search', '').strip()
    
    # Base query
    promotions_query = Voucher.objects.filter(da_xoa=False)
    
    # Apply filters
    if status_filter == 'active':
        promotions_query = promotions_query.filter(
            trang_thai=True,
            ngay_bat_dau__lte=timezone.now(),
            ngay_ket_thuc__gte=timezone.now()
        )
    elif status_filter == 'inactive':
        promotions_query = promotions_query.filter(trang_thai=False)
    elif status_filter == 'expired':
        promotions_query = promotions_query.filter(ngay_ket_thuc__lt=timezone.now())
    elif status_filter == 'upcoming':
        promotions_query = promotions_query.filter(ngay_bat_dau__gt=timezone.now())
    
    if type_filter != 'all':
        promotions_query = promotions_query.filter(loai_giam=type_filter)
    
    if search:
        promotions_query = promotions_query.filter(
            Q(ma_voucher__icontains=search) |
            Q(ten_voucher__icontains=search) |
            Q(mo_ta__icontains=search)
        )
    
    promotions = promotions_query.order_by('-ngay_tao')
    
    # Add usage percentage to each promotion
    for promo in promotions:
        if promo.so_luong_tong and promo.so_luong_tong > 0:
            promo.usage_percentage = (promo.so_luong_da_dung / promo.so_luong_tong) * 100
        else:
            promo.usage_percentage = 0
    
    # Statistics
    today = timezone.now()
    total_promotions = Voucher.objects.filter(da_xoa=False).count()
    
    active_promotions = Voucher.objects.filter(
        da_xoa=False,
        trang_thai=True,
        ngay_bat_dau__lte=today,
        ngay_ket_thuc__gte=today
    ).count()
    
    expired_promotions = Voucher.objects.filter(
        da_xoa=False,
        ngay_ket_thuc__lt=today
    ).count()
    
    upcoming_promotions = Voucher.objects.filter(
        da_xoa=False,
        ngay_bat_dau__gt=today
    ).count()
    
    # Usage statistics  
    total_usage = Voucher.objects.filter(da_xoa=False).aggregate(
        total_used=Sum('so_luong_da_dung')
    )['total_used'] or 0
    
    context = {
        'promotions': promotions,
        'total_promotions': total_promotions,
        'active_promotions': active_promotions,
        'expired_promotions': expired_promotions,
        'upcoming_promotions': upcoming_promotions,
        'total_usage': total_usage,
        'filtered_count': promotions.count(),
        # Filter values for form
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search': search,
        # Choices for dropdowns
        'status_choices': [
            ('all', 'Táº¥t cáº£'),
            ('active', 'Äang hoáº¡t Äá»ng'),
            ('inactive', 'Táº¡m ngÆ°ng'),
            ('expired', 'ÄÃ£ háº¿t háº¡n'),
            ('upcoming', 'Sáº¯p diá»n ra')
        ],
        'type_choices': [
            ('all', 'Táº¥t cáº£ loáº¡i'),
            ('phan_tram', 'Pháº§n trÄm'),
            ('tien_mat', 'Tiá»n máº·t')
        ]
    }
    
    return render(request, 'admin/promotions.html', context)
# - admin_delete_promotion
@require_role(['quan_ly'])
def admin_delete_promotion(request, voucher_id):
    """Delete promotion (soft delete)"""
    from django.contrib import messages
    from django.http import JsonResponse
    
    try:
        voucher = Voucher.objects.get(id=voucher_id, da_xoa=False)
        voucher.da_xoa = True
        voucher.save()
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True, 'message': f'ÄÃ£ xÃ³a voucher "{voucher.ma_voucher}" thÃ nh cÃ´ng!'})
        else:
            messages.success(request, f'ÄÃ£ xÃ³a voucher "{voucher.ma_voucher}" thÃ nh cÃ´ng!')
            
    except Voucher.DoesNotExist:
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'message': 'Voucher khÃ´ng tá»n táº¡i!'})
        else:
            messages.error(request, 'Voucher khÃ´ng tá»n táº¡i!')
    except Exception as e:
        print(f"DEBUG Delete Promotion - Error: {e}")
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
        else:
            messages.error(request, f'CÃ³ lá»i xáº£y ra: {str(e)}')
    
    return redirect('services:admin_promotions')
# - admin_promotion_stats
@require_role(['quan_ly'])
def admin_promotion_stats(request, voucher_id):
    """Get detailed statistics for a specific voucher"""
    from django.http import JsonResponse
    from datetime import datetime, date
    
    try:
        voucher = Voucher.objects.get(id=voucher_id, da_xoa=False)
        
        # Calculate remaining days - DateField objects don't have .date() method
        today = timezone.now().date()
        if voucher.ngay_ket_thuc > today:
            so_ngay_con_lai = (voucher.ngay_ket_thuc - today).days
        else:
            so_ngay_con_lai = 0
        
        # Calculate total savings from this voucher usage
        tong_tiet_kiem = 0
        if voucher.so_luong_da_dung > 0:
            # Use correct field name from model: gia_tri_don_toi_thieu
            avg_order_value = voucher.gia_tri_don_toi_thieu or 100000  # fallback
            if voucher.loai_giam == 'phan_tram':
                tong_tiet_kiem = (avg_order_value * voucher.gia_tri_giam / 100) * voucher.so_luong_da_dung
            else:
                tong_tiet_kiem = voucher.gia_tri_giam * voucher.so_luong_da_dung
        
        stats = {
            'ma_voucher': voucher.ma_voucher,
            'ten_voucher': voucher.ten_voucher,
            'mo_ta': voucher.mo_ta or '',
            'loai_giam': voucher.loai_giam,
            'gia_tri_giam': float(voucher.gia_tri_giam),
            'gia_tri_don_hang_toi_thieu': float(voucher.gia_tri_don_toi_thieu or 0),  # Fixed field name
            'gia_tri_giam_toi_da': float(voucher.giam_toi_da or 0),  # Fixed field name
            'ngay_bat_dau': str(voucher.ngay_bat_dau),  # DateField can be converted to string directly
            'ngay_ket_thuc': str(voucher.ngay_ket_thuc),  # DateField can be converted to string directly
            'so_luong_toi_da': voucher.so_luong_tong or 0,  # Fixed field name
            'so_luong_da_dung': voucher.so_luong_da_dung or 0,
            'trang_thai': voucher.trang_thai,
            'so_ngay_con_lai': so_ngay_con_lai,
            'tong_tiet_kiem': float(tong_tiet_kiem),
        }
        
        return JsonResponse({
            'success': True,
            'stats': stats
        })
        
    except Voucher.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Voucher khÃ´ng tá»n táº¡i!'
        })
    except Exception as e:
        print(f"DEBUG Promotion Stats - Error: {e}")
        return JsonResponse({
            'success': False,
            'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'
        })
# - admin_export_promotions
@require_role(['quan_ly'])
def admin_export_promotions(request):
    """Export Promotions"""
    promotions = Voucher.objects.filter(da_xoa=False).order_by('-ngay_tao')
    
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="khuyen_mai.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['MÃ£ voucher', 'TÃªn voucher', 'MÃ´ táº£', 'Loáº¡i giáº£m', 'GiÃ¡ trá»', 'NgÃ y báº¯t Äáº§u', 'NgÃ y káº¿t thÃºc', 'Tráº¡ng thÃ¡i'])
    
    for promo in promotions:
        status_text = 'Hoáº¡t Äá»ng' if promo.trang_thai else 'Táº¡m ngÆ°ng'
        loai_giam_text = dict(promo.LOAI_GIAM_CHOICES).get(promo.loai_giam, promo.loai_giam)
        
        writer.writerow([
            promo.ma_voucher,
            promo.ten_voucher,
            promo.mo_ta or '',
            loai_giam_text,
            promo.gia_tri_giam,
            promo.ngay_bat_dau,
            promo.ngay_ket_thuc,
            status_text
        ])
    
    return response
# - test_promotions
def test_promotions(request):
    """Test view without authentication"""
    from datetime import datetime, date
    from django.contrib import messages
    
    # Handle POST requests for CRUD operations (same as main view)
    if request.method == 'POST':
        try:
            voucher_id = request.POST.get('voucher_id')
            
            # Validation
            ma_voucher = request.POST.get('ma_voucher', '').strip()
            ten_voucher = request.POST.get('ten_voucher', '').strip()
            loai_giam = request.POST.get('loai_giam', '').strip()
            gia_tri_giam = request.POST.get('gia_tri_giam', '').strip()
            ngay_bat_dau = request.POST.get('ngay_bat_dau', '').strip()
            ngay_ket_thuc = request.POST.get('ngay_ket_thuc', '').strip()
            
            if not all([ma_voucher, ten_voucher, loai_giam, gia_tri_giam, ngay_bat_dau, ngay_ket_thuc]):
                messages.error(request, 'Vui lÃ²ng Äiá»n Äáº§y Äá»§ thÃ´ng tin báº¯t buá»c!')
                return redirect('test_promotions')
            
            # Check for duplicate voucher code (exclude current when editing)
            existing_voucher = Voucher.objects.filter(ma_voucher=ma_voucher, da_xoa=False)
            if voucher_id:
                existing_voucher = existing_voucher.exclude(id=voucher_id)
            if existing_voucher.exists():
                messages.error(request, f'MÃ£ voucher "{ma_voucher}" ÄÃ£ tá»n táº¡i!')
                return redirect('test_promotions')
            
            # Parse dates
            try:
                ngay_bat_dau_dt = datetime.strptime(ngay_bat_dau, '%Y-%m-%dT%H:%M')
                ngay_ket_thuc_dt = datetime.strptime(ngay_ket_thuc, '%Y-%m-%dT%H:%M')
                
                if ngay_bat_dau_dt >= ngay_ket_thuc_dt:
                    messages.error(request, 'NgÃ y káº¿t thÃºc pháº£i sau ngÃ y báº¯t Äáº§u!')
                    return redirect('test_promotions')
                    
            except ValueError as e:
                messages.error(request, f'Äá»nh dáº¡ng ngÃ y giá» khÃ´ng há»£p lá»: {e}!')
                return redirect('test_promotions')
            
            # Validate discount value
            try:
                gia_tri_giam_float = float(gia_tri_giam)
                if gia_tri_giam_float <= 0:
                    messages.error(request, 'GiÃ¡ trá» giáº£m pháº£i lá»n hÆ¡n 0!')
                    return redirect('test_promotions')
                if loai_giam == 'phan_tram' and gia_tri_giam_float > 100:
                    messages.error(request, 'Giáº£m theo pháº§n trÄm khÃ´ng ÄÆ°á»£c vÆ°á»£t quÃ¡ 100%!')
                    return redirect('test_promotions')
            except ValueError:
                messages.error(request, 'GiÃ¡ trá» giáº£m khÃ´ng há»£p lá»!')
                return redirect('test_promotions')
            
            # Prepare data with correct field names from model
            voucher_data = {
                'ma_voucher': ma_voucher,
                'ten_voucher': ten_voucher,
                'mo_ta': request.POST.get('mo_ta', '').strip(),
                'loai_giam': loai_giam,
                'gia_tri_giam': gia_tri_giam_float,
                'gia_tri_don_toi_thieu': float(request.POST.get('gia_tri_don_hang_toi_thieu') or 0),
                'giam_toi_da': float(request.POST.get('gia_tri_giam_toi_da') or 0) or None,
                'ngay_bat_dau': ngay_bat_dau_dt.date(),
                'ngay_ket_thuc': ngay_ket_thuc_dt.date(),
                'so_luong_tong': int(request.POST.get('so_luong_toi_da') or 0) or None,
                'trang_thai': request.POST.get('trang_thai') == 'active',
            }
            
            if voucher_id:
                # Update existing voucher
                voucher = Voucher.objects.get(id=voucher_id, da_xoa=False)
                for key, value in voucher_data.items():
                    setattr(voucher, key, value)
                voucher.save()
                messages.success(request, f'ÄÃ£ cáº­p nháº­t voucher "{ma_voucher}" thÃ nh cÃ´ng!')
            else:
                # Create new voucher - Use first user as default
                from .models import NguoiDung
                first_user = NguoiDung.objects.first()
                if not first_user:
                    messages.error(request, 'KhÃ´ng tÃ¬m tháº¥y user Äá» táº¡o voucher!')
                    return redirect('test_promotions')
                    
                voucher_data['nguoi_tao'] = first_user
                voucher = Voucher.objects.create(**voucher_data)
                messages.success(request, f'ÄÃ£ táº¡o voucher "{ma_voucher}" thÃ nh cÃ´ng!')
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            messages.error(request, f'CÃ³ lá»i xáº£y ra: {str(e)}')
        
        return redirect('test_promotions')
    
    # GET request - Create a test object with attributes
    class TestVoucher:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    # Get actual vouchers from database for display
    actual_vouchers = Voucher.objects.filter(da_xoa=False).order_by('-id')
    
    context = {
        'promotions': actual_vouchers,
        'total_promotions': actual_vouchers.count(),
        'active_promotions': actual_vouchers.filter(trang_thai=True).count(),
        'inactive_promotions': actual_vouchers.filter(trang_thai=False).count(),
        'expired_promotions': 0,
    }
    
    return render(request, 'admin/promotions.html', context)
