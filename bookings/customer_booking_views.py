"""
Customer Booking Flow Views
Thêm các views này vào bookings/views.py
"""

# ==================== CUSTOMER BOOKING FLOW ====================

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q, Avg, F
from django.views.decorators.csrf import csrf_exempt
from core.decorators import require_role
from barbershop.models import (
    NguoiDung, DatLich, DichVu, DichVuDatLich, DanhGia
)


def booking_step1(request):
    """Step 1: Select Services"""
    # Get categories and services
    from barbershop.models import DanhMucDichVu
    
    categories = DanhMucDichVu.objects.filter(da_xoa=False).order_by('thu_tu')
    
    # Get featured/popular services (top 6 by order)
    # Note: DichVu model doesn't have 'noi_bat' field, so we use 'thu_tu' (order) instead
    featured_services = DichVu.objects.filter(
        trang_thai=True,
        da_xoa=False
    ).order_by('thu_tu')[:6]
    
    # Get all services grouped by category
    services = DichVu.objects.filter(
        trang_thai=True,
        da_xoa=False
    ).select_related('danh_muc').order_by('danh_muc__thu_tu', 'thu_tu')
    
    # Check if voucher code in URL
    voucher_code = request.GET.get('voucher', '')
    
    context = {
        'categories': categories,
        'featured_services': featured_services,
        'services': services,  # Changed from 'all_services' to 'services'
        'voucher_code': voucher_code,
    }
    return render(request, 'customer/booking_step1.html', context)


def booking_step2(request):
    """Step 2: Select Stylist & Time"""
    import logging
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        # Get selected services from step 1
        import json
        services_data = request.POST.get('services', '[]')
        selected_services = json.loads(services_data)
        
        logger.info(f"=== BOOKING STEP 2 ===")
        logger.info(f"Received services data: {services_data[:100]}...")  # First 100 chars
        logger.info(f"Parsed services count: {len(selected_services)}")
        
        if not selected_services:
            return redirect('/bookings/step1/')
        
        # Store in session
        request.session['booking_services'] = selected_services
        request.session.modified = True  # Force session save
        request.session.save()  # Explicitly save session
        
        logger.info(f"Saved to session: {len(selected_services)} services")
        logger.info(f"Session after save: {request.session.get('booking_services')}")
        logger.info(f"Session key: {request.session.session_key}")
        
        # Get available stylists
        stylists = NguoiDung.objects.filter(
            vai_tro='nhan_vien',
            trang_thai=True,  # BooleanField, not CharField
            da_xoa=False
        ).annotate(
            total_bookings=Count('dat_lich_nhan_vien', filter=Q(dat_lich_nhan_vien__trang_thai='hoan_thanh'))
        ).select_related('thong_tin_nhan_vien').order_by('-total_bookings')
        
        # Get stylist ratings
        for stylist in stylists:
            avg_rating = DanhGia.objects.filter(
                nhan_vien=stylist,
                da_duyet=True,
                da_xoa=False
            ).aggregate(avg=Avg('danh_gia_stylist'))['avg']
            stylist.avg_rating = round(avg_rating, 1) if avg_rating else 0
        
        context = {
            'selected_services': selected_services,
            'stylists': stylists,
        }
        return render(request, 'customer/booking_step2.html', context)
    
    return redirect('/bookings/step1/')


def booking_step3(request):
    """Step 3: Confirm & Complete Booking"""
    # Debug logging
    import logging
    import json
    logger = logging.getLogger(__name__)
    
    logger.info(f"=== BOOKING STEP 3 ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"User ID in session: {request.session.get('user_id')}")
    logger.info(f"Booking services in session: {request.session.get('booking_services')}")
    
    # Check if user is logged in, if not redirect to login with next parameter
    if 'user_id' not in request.session:
        # Save current booking data to session first
        if request.method == 'POST':
            request.session['pending_booking_step2'] = {
                'stylist_id': request.POST.get('stylist_id'),
                'ngay_hen': request.POST.get('ngay_hen'),
                'gio_hen': request.POST.get('gio_hen'),
                'ghi_chu': request.POST.get('ghi_chu', '')
            }
        return redirect(f"/accounts/customer/login/?next=/bookings/step3/")
    
    # Check if there's pending booking data after login
    pending_data = request.session.get('pending_booking_step2')
    
    if request.method == 'POST':
        # Get data from step 2
        stylist_id = request.POST.get('stylist_id')
        ngay_hen = request.POST.get('ngay_hen')
        gio_hen = request.POST.get('gio_hen')
        ghi_chu = request.POST.get('ghi_chu', '')
        
        logger.info(f"POST Data - stylist_id: {stylist_id}, ngay_hen: {ngay_hen}, gio_hen: {gio_hen}")
    elif pending_data:
        # User just logged in, use pending data
        stylist_id = pending_data.get('stylist_id')
        ngay_hen = pending_data.get('ngay_hen')
        gio_hen = pending_data.get('gio_hen')
        ghi_chu = pending_data.get('ghi_chu', '')
        # Clear pending data
        del request.session['pending_booking_step2']
    else:
        # No POST data and no pending data
        return redirect('bookings:booking_step2')
    
    if not all([stylist_id, ngay_hen, gio_hen]):
        return redirect('bookings:booking_step2')
    
    # Update session
    request.session['booking_stylist_id'] = stylist_id
    request.session['booking_date'] = ngay_hen
    request.session['booking_time'] = gio_hen
    request.session['booking_note'] = ghi_chu
    request.session.modified = True  # Force session save
    
    # Get customer info
    customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
    
    # Get stylist info (if specific stylist selected)
    stylist = None
    if stylist_id and stylist_id != 'any':
        stylist = get_object_or_404(NguoiDung, id=stylist_id, vai_tro='nhan_vien')
    
    # Calculate totals
    services = request.session.get('booking_services', [])
    
    # DEBUG: Log session data
    logger.info(f"Services from session: {services}")
    logger.info(f"Services count: {len(services) if services else 0}")
    logger.info(f"All session keys: {list(request.session.keys())}")
    
    # Validate that services exist
    if not services:
        # No services selected, redirect back to step 1
        logger.warning(f"No booking_services in session! Redirecting to step1")
        logger.warning(f"All session keys: {list(request.session.keys())}")
        return redirect('bookings:booking_step1')
    
    tam_tinh = sum(service.get('price', 0) * service.get('quantity', 1) for service in services)
    
    # Get customer's available vouchers
    from barbershop.models import VoucherKhachHang, Voucher
    today = timezone.now().date()
    
    # Customer's personal vouchers
    customer_vouchers = VoucherKhachHang.objects.filter(
        khach_hang=customer,
        trang_thai='chua_su_dung'
    ).select_related('voucher')
    
    # Public vouchers that customer can use
    public_vouchers = Voucher.objects.filter(
        trang_thai=True,
        ngay_bat_dau__lte=today,
        ngay_ket_thuc__gte=today,
        gia_tri_don_toi_thieu__lte=tam_tinh,  # Only show vouchers applicable to this order
        da_xoa=False
    ).exclude(
        so_luong_da_dung__gte=F('so_luong_tong')  # Exclude fully used vouchers
    )
    
    context = {
        'customer': customer,
        'stylist': stylist,
        'services': services,
        'services_json': json.dumps(services),  # JSON serialized for JavaScript
        'ngay_hen': ngay_hen,
        'gio_hen': gio_hen,
        'ghi_chu': ghi_chu,
        'tam_tinh': tam_tinh,
        'customer_vouchers': customer_vouchers,
        'public_vouchers': public_vouchers,
        'max_points': min(customer.diem_tich_luy, int(tam_tinh / 100)),  # 100 points = 10,000 VND
    }
    return render(request, 'customer/booking_step3.html', context)


def booking_step4(request):
    """Step 4: Review & Confirm"""
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect(f"/accounts/customer/login/?next=/bookings/step3/")
    
    if request.method == 'POST':
        # Get payment info
        voucher_code = request.POST.get('voucher_code', '')
        points_to_use = int(request.POST.get('points_to_use', 0) or 0)
        
        # Update session
        request.session['booking_voucher'] = voucher_code
        request.session['booking_points'] = points_to_use
        
        # Get all booking info from session
        services = request.session.get('booking_services', [])
        stylist_id = request.session.get('booking_stylist_id')
        ngay_hen = request.session.get('booking_date')
        gio_hen = request.session.get('booking_time')
        ghi_chu = request.session.get('booking_note', '')
        
        if not all([services, stylist_id, ngay_hen, gio_hen]):
            return redirect('/bookings/step1/')
        
        # Get customer and stylist
        customer = get_object_or_404(NguoiDung, id=request.session['user_id'])
        stylist = get_object_or_404(NguoiDung, id=stylist_id)
        
        # Calculate totals
        tam_tinh = sum(service.get('price', 0) * service.get('quantity', 1) for service in services)
        tien_giam_gia = 0
        
        # Apply voucher
        voucher = None
        if voucher_code:
            from barbershop.models import Voucher
            voucher = Voucher.objects.filter(
                ma_voucher=voucher_code,
                trang_thai=True,  # BooleanField, not CharField
                da_xoa=False
            ).first()
            
            if voucher:
                if voucher.loai_giam == 'phan_tram':
                    discount = tam_tinh * voucher.gia_tri_giam / 100
                    if voucher.giam_toi_da:
                        discount = min(discount, voucher.giam_toi_da)
                    tien_giam_gia += discount
                else:  # tien
                    tien_giam_gia += voucher.gia_tri_giam
        
        # Apply points (100 points = 10,000 VND)
        if points_to_use > 0:
            tien_giam_gia += points_to_use * 100
        
        thanh_tien = max(0, tam_tinh - tien_giam_gia)
        
        context = {
            'customer': customer,
            'stylist': stylist,
            'services': services,
            'ngay_hen': ngay_hen,
            'gio_hen': gio_hen,
            'ghi_chu': ghi_chu,
            'tam_tinh': tam_tinh,
            'voucher': voucher,
            'points_to_use': points_to_use,
            'tien_giam_gia': tien_giam_gia,
            'thanh_tien': thanh_tien,
        }
        return render(request, 'customer/booking_step4.html', context)
    
    return redirect('/bookings/step3/')


@csrf_exempt
def create_booking(request):
    """Create booking (AJAX) - Called from step 3"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})
    
    # Check if user is logged in
    if 'user_id' not in request.session:
        return JsonResponse({
            'success': False,
            'message': 'Vui lòng đăng nhập để hoàn tất đặt lịch',
            'require_login': True,
            'redirect_url': '/accounts/customer/login/?next=/bookings/step3/'
        })
    
    try:
        from barbershop.models import Voucher, GiaoDichDiem
        import random
        import string
        import json
        
        # Get all booking info from session
        customer_id = request.session['user_id']
        customer = get_object_or_404(NguoiDung, id=customer_id)
        
        services = request.session.get('booking_services', [])
        stylist_id = request.session.get('booking_stylist_id')
        ngay_hen = request.session.get('booking_date')
        gio_hen = request.session.get('booking_time')
        ghi_chu = request.session.get('booking_note', '')
        
        # Get voucher and points from POST (from step 3 form)
        voucher_code = request.POST.get('voucher_code', '').strip().upper()
        points_to_use = int(request.POST.get('points_to_use', 0) or 0)
        
        if not all([services, stylist_id, ngay_hen, gio_hen]):
            return JsonResponse({
                'success': False,
                'message': 'Thiếu thông tin đặt lịch. Vui lòng bắt đầu lại từ bước 1.'
            })
        
        # Parse date and time
        from datetime import datetime
        ngay_hen_date = datetime.strptime(ngay_hen, '%Y-%m-%d').date()
        gio_hen_time = datetime.strptime(gio_hen, '%H:%M').time()
        
        # Calculate totals
        tam_tinh = sum(service.get('price', 0) * service.get('quantity', 1) for service in services)
        tien_giam_gia = 0
        voucher = None
        
        # Apply voucher
        if voucher_code:
            voucher = Voucher.objects.filter(
                ma_voucher=voucher_code,
                trang_thai=True,
                da_xoa=False
            ).first()
            
            if voucher:
                # Validate voucher
                today = timezone.now().date()
                if voucher.ngay_bat_dau and today < voucher.ngay_bat_dau:
                    return JsonResponse({'success': False, 'message': 'Voucher chưa có hiệu lực'})
                if voucher.ngay_ket_thuc and today > voucher.ngay_ket_thuc:
                    return JsonResponse({'success': False, 'message': 'Voucher đã hết hạn'})
                if voucher.gia_tri_don_toi_thieu and tam_tinh < voucher.gia_tri_don_toi_thieu:
                    return JsonResponse({'success': False, 'message': f'Đơn hàng tối thiểu {voucher.gia_tri_don_toi_thieu:,.0f}đ'})
                if voucher.so_luong_tong and voucher.so_luong_da_dung >= voucher.so_luong_tong:
                    return JsonResponse({'success': False, 'message': 'Voucher đã hết lượt sử dụng'})
                
                # Calculate discount
                if voucher.loai_giam == 'phan_tram':
                    discount = tam_tinh * voucher.gia_tri_giam / 100
                    if voucher.giam_toi_da:
                        discount = min(discount, voucher.giam_toi_da)
                    tien_giam_gia += discount
                else:
                    tien_giam_gia += voucher.gia_tri_giam
                
                # Update voucher usage
                voucher.so_luong_da_dung += 1
                voucher.save()
        
        # Apply points (100 points = 10,000 VND)
        if points_to_use > 0:
            if customer.diem_tich_luy < points_to_use:
                return JsonResponse({
                    'success': False,
                    'message': 'Không đủ điểm thưởng'
                })
            tien_giam_gia += points_to_use * 100
        
        thanh_tien = max(0, tam_tinh - tien_giam_gia)
        
        # Generate booking code
        ma_dat_lich = 'BK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Create booking
        booking = DatLich.objects.create(
            ma_dat_lich=ma_dat_lich,
            khach_hang=customer,
            ten_khach_hang=customer.ho_ten,
            so_dien_thoai_khach=customer.so_dien_thoai,
            nhan_vien_id=stylist_id,
            ngay_hen=ngay_hen_date,
            gio_hen=gio_hen_time,
            loai_dat_lich='online',
            trang_thai='cho_xac_nhan',
            ghi_chu=ghi_chu,
            tong_tien=tam_tinh,
            tien_giam_gia=tien_giam_gia,
            thanh_tien=thanh_tien,
            da_xoa=False
        )
        
        # Add services
        for service in services:
            quantity = service.get('quantity', 1)
            price = service.get('price', 0)
            DichVuDatLich.objects.create(
                dat_lich=booking,
                dich_vu_id=service['id'],
                ten_dich_vu=service.get('name', 'Dịch vụ'),  # Thêm tên dịch vụ
                gia=price,  # Đổi từ gia_tai_thoi_diem -> gia
                so_luong=quantity,
                thanh_tien=price * quantity
                # Bỏ da_xoa vì model không có field này
            )
        
        # Deduct points if used
        if points_to_use > 0:
            points_before = customer.diem_tich_luy
            customer.diem_tich_luy -= points_to_use
            customer.save()
            
            GiaoDichDiem.objects.create(
                khach_hang=customer,
                loai_giao_dich='tru',
                so_diem=points_to_use,
                diem_truoc=points_before,
                diem_sau=customer.diem_tich_luy,
                mo_ta=f'Sử dụng điểm cho đặt lịch {ma_dat_lich}'
            )
        
        # Clear booking session data
        for key in ['booking_services', 'booking_stylist_id', 'booking_date', 
                    'booking_time', 'booking_note']:
            if key in request.session:
                del request.session[key]
        
        return JsonResponse({
            'success': True,
            'message': 'Đặt lịch thành công!',
            'booking_id': booking.id,
            'booking_code': ma_dat_lich,
            'redirect_url': f'/bookings/success/?id={booking.id}'
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Có lỗi xảy ra: {str(e)}'
        })


def booking_success(request):
    """Booking success page"""
    booking_id = request.GET.get('id')
    if not booking_id:
        return redirect('/customer/bookings/')
    
    booking = get_object_or_404(DatLich, id=booking_id, da_xoa=False)
    services = booking.dich_vu_dat_lich.all().select_related('dich_vu')
    
    context = {
        'booking': booking,
        'services': services,
    }
    return render(request, 'customer/booking_success.html', context)


@csrf_exempt
def get_time_slots(request):
    """Get available time slots for a date and stylist (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})
    
    try:
        from datetime import datetime, timedelta
        from barbershop.models import LichLamViec
        
        stylist_id = request.POST.get('stylist_id')
        date_str = request.POST.get('date')
        
        if not date_str:
            return JsonResponse({
                'success': False,
                'message': 'Thiếu thông tin ngày'
            })
        
        # Parse date
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # If stylist selected (not "any")
        if stylist_id and stylist_id != 'any':
            # Get stylist's work schedule for this date
            work_schedules = LichLamViec.objects.filter(
                nhan_vien_id=stylist_id,
                ngay_lam=selected_date,
                trang_thai='da_duyet',
                da_xoa=False
            )
            
            if not work_schedules.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Stylist không có lịch làm việc trong ngày này'
                })
            
            # Generate time slots based on work schedule
            time_slots = []
            for schedule in work_schedules:
                from datetime import time
                
                # Handle both string and time object formats
                if isinstance(schedule.gio_bat_dau, time):
                    start_time = schedule.gio_bat_dau
                else:
                    start_time = datetime.strptime(schedule.gio_bat_dau, '%H:%M').time()
                
                if isinstance(schedule.gio_ket_thuc, time):
                    end_time = schedule.gio_ket_thuc
                else:
                    end_time = datetime.strptime(schedule.gio_ket_thuc, '%H:%M').time()
                
                current_time = datetime.combine(selected_date, start_time)
                end_datetime = datetime.combine(selected_date, end_time)
                
                while current_time < end_datetime:
                    slot_time = current_time.time()
                    
                    # Check if slot is already booked
                    existing_booking = DatLich.objects.filter(
                        nhan_vien_id=stylist_id,
                        ngay_hen=selected_date,
                        gio_hen=slot_time,
                        trang_thai__in=['cho_xac_nhan', 'da_xac_nhan', 'da_checkin'],
                        da_xoa=False
                    ).exists()
                    
                    time_slots.append({
                        'time': slot_time.strftime('%H:%M'),
                        'available': not existing_booking
                    })
                    
                    current_time += timedelta(minutes=30)
        else:
            # "Any stylist" - use default business hours
            from barbershop.models import CaiDatHeThong
            settings = CaiDatHeThong.get_settings()
            
            from datetime import time
            
            # Handle both string and time object formats
            if isinstance(settings.gio_mo_cua, time):
                start_time = settings.gio_mo_cua
            else:
                start_time = datetime.strptime(settings.gio_mo_cua or '08:00', '%H:%M').time()
            
            if isinstance(settings.gio_dong_cua, time):
                end_time = settings.gio_dong_cua
            else:
                end_time = datetime.strptime(settings.gio_dong_cua or '20:00', '%H:%M').time()
            
            current_time = datetime.combine(selected_date, start_time)
            end_datetime = datetime.combine(selected_date, end_time)
            
            time_slots = []
            while current_time < end_datetime:
                slot_time = current_time.time()
                
                # For "any stylist", just show all slots as available
                time_slots.append({
                    'time': slot_time.strftime('%H:%M'),
                    'available': True
                })
                
                current_time += timedelta(minutes=30)
        
        return JsonResponse({
            'success': True,
            'time_slots': time_slots
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Có lỗi xảy ra: {str(e)}'
        })


@csrf_exempt
def validate_voucher(request):
    """Validate voucher code (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'})
    
    try:
        from barbershop.models import Voucher
        
        voucher_code = request.POST.get('voucher_code', '').strip().upper()
        total_amount = float(request.POST.get('total_amount', 0))
        
        if not voucher_code:
            return JsonResponse({
                'success': False,
                'message': 'Vui lòng nhập mã voucher'
            })
        
        # Find voucher
        voucher = Voucher.objects.filter(
            ma_voucher=voucher_code,
            trang_thai=True,  # BooleanField, not CharField
            da_xoa=False
        ).first()
        
        if not voucher:
            return JsonResponse({
                'success': False,
                'message': 'Mã voucher không tồn tại'
            })
        
        # Check date range
        today = timezone.now().date()
        if voucher.ngay_bat_dau and today < voucher.ngay_bat_dau:
            return JsonResponse({
                'success': False,
                'message': 'Voucher chưa có hiệu lực'
            })
        
        if voucher.ngay_ket_thuc and today > voucher.ngay_ket_thuc:
            return JsonResponse({
                'success': False,
                'message': 'Voucher đã hết hạn'
            })
        
        # Check minimum order value
        if voucher.gia_tri_don_toi_thieu and total_amount < voucher.gia_tri_don_toi_thieu:
            return JsonResponse({
                'success': False,
                'message': f'Đơn hàng tối thiểu {voucher.gia_tri_don_toi_thieu:,.0f}đ'
            })
        
        # Check usage limit
        if voucher.so_luong_tong:
            if voucher.so_luong_da_dung >= voucher.so_luong_tong:
                return JsonResponse({
                    'success': False,
                    'message': 'Voucher đã hết lượt sử dụng'
                })
        
        # Calculate discount
        if voucher.loai_giam == 'phan_tram':
            discount = total_amount * voucher.gia_tri_giam / 100
            if voucher.giam_toi_da:
                discount = min(discount, voucher.giam_toi_da)
        else:  # tien
            discount = voucher.gia_tri_giam
        
        return JsonResponse({
            'success': True,
            'message': 'Áp dụng voucher thành công',
            'voucher': {
                'code': voucher.ma_voucher,
                'name': voucher.ten_voucher,
                'discount': discount,
                'type': voucher.loai_giam,
                'value': voucher.gia_tri_giam
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Có lỗi xảy ra: {str(e)}'
        })
