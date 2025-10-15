"""
Views for attendance app (Work Schedule, Leave Requests, Check-in/out, Salary)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum, Q, F, Case, When, IntegerField
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
from decimal import Decimal
import json
import csv
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# Import decorators from core
from core.decorators import require_auth, require_role

# Import models
from barbershop.models import (
    NguoiDung,
    ThongTinNhanVien,
    LichLamViec,
    DonXinNghi,
    ChamCong,
    DatLich,
    HoaDon
)

# ============ VIEWS - Bạn sẽ copy code vào đây ============
# Các views sẽ được di chuyển vào đây:
# - admin_work_schedule
@require_role(['quan_ly'])
def admin_work_schedule(request):
    """Work Schedule Management with Approval"""
    from django.db.models import Count, Sum, Avg, Q
    from datetime import date, timedelta, datetime
    import calendar
    
    print("DEBUG Work Schedule - Request received")
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            # Approve shift
            try:
                schedule_id = request.POST.get('schedule_id')
                schedule = get_object_or_404(LichLamViec, id=schedule_id, da_xoa=False)
                schedule.trang_thai = 'da_duyet'
                schedule.save()
                return JsonResponse({'success': True, 'message': 'ÄÃ£ duyá»t ca lÃ m!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        elif action == 'reject':
            # Reject shift
            try:
                schedule_id = request.POST.get('schedule_id')
                schedule = get_object_or_404(LichLamViec, id=schedule_id, da_xoa=False)
                schedule.trang_thai = 'tu_choi'
                schedule.ghi_chu = request.POST.get('ly_do', '')
                schedule.save()
                return JsonResponse({'success': True, 'message': 'ÄÃ£ tá»« chá»i ca lÃ m!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        elif action == 'create':
            # Admin creates shift for staff
            try:
                staff_ids = request.POST.getlist('staff_ids')  # Multiple staff
                ngay_lam = request.POST.get('ngay_lam')
                ca_lam = request.POST.get('ca_lam')
                repeat_type = request.POST.get('repeat_type', 'none')
                repeat_until = request.POST.get('repeat_until')
                ghi_chu = request.POST.get('ghi_chu', '')
                
                print(f"DEBUG Create Shift - staff_ids: {staff_ids}")
                print(f"DEBUG Create Shift - ngay_lam: {ngay_lam}")
                print(f"DEBUG Create Shift - ca_lam: {ca_lam}")
                print(f"DEBUG Create Shift - POST data: {request.POST}")
                
                if not staff_ids or len(staff_ids) == 0:
                    return JsonResponse({'success': False, 'message': 'Chưa chọn nhân viên'})
                
                if not ngay_lam:
                    return JsonResponse({'success': False, 'message': 'Chưa chọn ngày'})
                
                if not ca_lam:
                    return JsonResponse({'success': False, 'message': 'Chưa chọn ca làm'})
                
                # Map English shift names to Vietnamese
                shift_map = {
                    'morning': 'sang',
                    'afternoon': 'chieu',
                    'evening': 'toi',
                    'fullday': 'ca_ngay'
                }
                ca_lam_vi = shift_map.get(ca_lam, ca_lam)
                
                # Set times based on shift type
                shift_times = {
                    'sang': ('08:00', '12:00'),
                    'chieu': ('13:00', '17:00'),
                    'toi': ('17:00', '21:00'),
                    'ca_ngay': ('08:00', '21:00')
                }
                
                gio_bat_dau, gio_ket_thuc = shift_times.get(ca_lam_vi, ('08:00', '17:00'))
                
                created_count = 0
                start_date = datetime.strptime(ngay_lam, '%Y-%m-%d').date()
                
                # Handle repeat logic
                dates_to_create = [start_date]
                
                if repeat_type != 'none' and repeat_until:
                    end_date = datetime.strptime(repeat_until, '%Y-%m-%d').date()
                    current_date = start_date
                    
                    while current_date <= end_date:
                        if repeat_type == 'daily':
                            current_date += timedelta(days=1)
                        elif repeat_type == 'weekly':
                            current_date += timedelta(weeks=1)
                        elif repeat_type == 'monthly':
                            # Add one month
                            if current_date.month == 12:
                                current_date = current_date.replace(year=current_date.year+1, month=1)
                            else:
                                current_date = current_date.replace(month=current_date.month+1)
                        
                        if current_date <= end_date:
                            dates_to_create.append(current_date)
                
                # Create shifts for all selected staff and dates
                for staff_id in staff_ids:
                    for shift_date in dates_to_create:
                        # Check if shift already exists
                        existing = LichLamViec.objects.filter(
                            nhan_vien_id=staff_id,
                            ngay_lam=shift_date,
                            ca_lam=ca_lam_vi,
                            da_xoa=False
                        ).exists()
                        
                        if not existing:
                            LichLamViec.objects.create(
                                nhan_vien_id=staff_id,
                                ngay_lam=shift_date,
                                ca_lam=ca_lam_vi,
                                gio_bat_dau=gio_bat_dau,
                                gio_ket_thuc=gio_ket_thuc,
                                trang_thai='da_duyet',
                                ghi_chu=ghi_chu,
                                da_xoa=False
                            )
                            created_count += 1
                
                return JsonResponse({
                    'success': True, 
                    'message': f'ÄÃ£ táº¡o {created_count} ca lÃ m viá»c!'
                })
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        elif action == 'delete':
            # Delete shift
            try:
                schedule_id = request.POST.get('schedule_id')
                schedule = get_object_or_404(LichLamViec, id=schedule_id, da_xoa=False)
                schedule.da_xoa = True
                schedule.ngay_xoa = timezone.now()
                schedule.save()
                return JsonResponse({'success': True, 'message': 'ÄÃ£ xÃ³a ca lÃ m!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
    
    # GET request - display schedule
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Get filter parameters
    view_type = request.GET.get('view', 'week')  # week, month, pending
    staff_id = request.GET.get('staff_id')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    print(f"DEBUG Work Schedule - Params: view={view_type}, staff={staff_id}, from={from_date}, to={to_date}")
    
    # Get all active staff
    staff = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        da_xoa=False,
        trang_thai=True
    ).order_by('ho_ten')
    
    # Calculate statistics
    total_staff = staff.count()
    
    # Working today - staff who have shifts today
    working_today = LichLamViec.objects.filter(
        da_xoa=False,
        ngay_lam=today,
        trang_thai='da_duyet'
    ).values('nhan_vien').distinct().count()
    
    # Off today - total staff minus working today
    off_today = total_staff - working_today
    
    # Total shifts this week
    total_shifts_week = LichLamViec.objects.filter(
        da_xoa=False,
        ngay_lam__gte=week_start,
        ngay_lam__lte=week_end,
        trang_thai='da_duyet'
    ).count()
    
    # Pending leave requests (assuming we have a model for this)
    try:
        from barbershop.models import DonXinNghi
        pending_leaves = DonXinNghi.objects.filter(
            da_xoa=False,
            trang_thai='cho_duyet'
        ).count()
        
        leave_requests = DonXinNghi.objects.filter(
            da_xoa=False
        ).select_related('nhan_vien').order_by('-ngay_tao')[:20]
    except:
        # If leave request model doesn't exist, use 0
        pending_leaves = 0
        leave_requests = []
    
    # Average hours per week per staff (estimate 4h per shift for sang/chieu, 4h for toi)
    week_shifts = LichLamViec.objects.filter(
        da_xoa=False,
        ngay_lam__gte=week_start,
        ngay_lam__lte=week_end,
        trang_thai='da_duyet'
    )
    
    total_hours = 0
    for shift in week_shifts:
        # Estimate hours based on shift type
        if shift.ca_lam in ['sang', 'chieu']:
            total_hours += 4
        elif shift.ca_lam == 'toi':
            total_hours += 4
        else:
            total_hours += 8  # fullday
    
    avg_hours = (total_hours / total_staff) if total_staff > 0 else 0
    
    print(f"DEBUG Work Schedule - Stats: staff={total_staff}, working_today={working_today}, shifts={total_shifts_week}")
    
    # Filter staff if specified
    if staff_id and staff_id.strip():
        staff = staff.filter(id=staff_id.strip())
        print(f"DEBUG Work Schedule - Filtered to staff ID: {staff_id}")
    
    # Date range for filtering
    if view_type == 'month':
        if from_date and to_date:
            try:
                filter_start = datetime.strptime(from_date, '%Y-%m-%d').date()
                filter_end = datetime.strptime(to_date, '%Y-%m-%d').date()
            except:
                filter_start = today.replace(day=1)
                last_day = calendar.monthrange(today.year, today.month)[1]
                filter_end = today.replace(day=last_day)
        else:
            filter_start = today.replace(day=1)
            last_day = calendar.monthrange(today.year, today.month)[1]
            filter_end = today.replace(day=last_day)
    else:
        if from_date and to_date:
            try:
                filter_start = datetime.strptime(from_date, '%Y-%m-%d').date()
                filter_end = datetime.strptime(to_date, '%Y-%m-%d').date()
            except:
                filter_start = week_start
                filter_end = week_end
        else:
            filter_start = week_start
            filter_end = week_end
    
    # Get schedules based on view type and filters
    base_schedule_query = LichLamViec.objects.filter(
        da_xoa=False,
        ngay_lam__gte=filter_start,
        ngay_lam__lte=filter_end
    ).select_related('nhan_vien')
    
    if staff_id and staff_id.strip():
        base_schedule_query = base_schedule_query.filter(nhan_vien_id=staff_id.strip())
    
    schedules = base_schedule_query.order_by('ngay_lam', 'gio_bat_dau')
    
    print(f"DEBUG Work Schedule - Found {schedules.count()} schedules for period {filter_start} to {filter_end}")
    
    # Organize schedules by staff and day for calendar view
    schedule_dict = {}
    for schedule in schedules:
        staff_id_key = schedule.nhan_vien_id
        if staff_id_key not in schedule_dict:
            schedule_dict[staff_id_key] = {}
        day = schedule.ngay_lam.strftime('%Y-%m-%d')
        if day not in schedule_dict[staff_id_key]:
            schedule_dict[staff_id_key][day] = []
        schedule_dict[staff_id_key][day].append(schedule)
    
    # Build week days for calendar view
    week_days = []
    current_date = filter_start
    while current_date <= filter_end:
        day_schedules = {
            'date': current_date,
            'morning_shifts': [],
            'afternoon_shifts': [],
            'evening_shifts': [],
            'fullday_shifts': [],
            'morning_leaves': [],
        }
        
        # Get shifts for this day
        day_str = current_date.strftime('%Y-%m-%d')
        for staff_member in staff:
            if staff_member.id in schedule_dict and day_str in schedule_dict[staff_member.id]:
                for shift in schedule_dict[staff_member.id][day_str]:
                    if shift.ca_lam == 'sang':
                        day_schedules['morning_shifts'].append(shift)
                    elif shift.ca_lam == 'chieu':
                        day_schedules['afternoon_shifts'].append(shift)
                    elif shift.ca_lam == 'toi':
                        day_schedules['evening_shifts'].append(shift)
                    else:
                        day_schedules['morning_shifts'].append(shift)  # Default to morning
        
        week_days.append(day_schedules)
        current_date += timedelta(days=1)
    
    # Build staff list with schedule for staff view
    staff_list = []
    for staff_member in staff:
        week_schedule = []
        total_hours = 0
        
        current_date = filter_start
        while current_date <= filter_end:
            day_str = current_date.strftime('%Y-%m-%d')
            day_shifts = []
            
            if staff_member.id in schedule_dict and day_str in schedule_dict[staff_member.id]:
                for shift in schedule_dict[staff_member.id][day_str]:
                    # Estimate hours based on shift type
                    hours = 4 if shift.ca_lam in ['sang', 'chieu', 'toi'] else 8
                    
                    # Map Vietnamese to English for CSS class
                    shift_type_map = {
                        'sang': 'morning',
                        'chieu': 'afternoon',
                        'toi': 'evening',
                        'ca_ngay': 'fullday'
                    }
                    shift_type = shift_type_map.get(shift.ca_lam, 'morning')
                    
                    # Map Vietnamese to display label
                    shift_label_map = {
                        'sang': 'Sáng',
                        'chieu': 'Chiều',
                        'toi': 'Tối',
                        'ca_ngay': 'Cả ngày'
                    }
                    shift_label = shift_label_map.get(shift.ca_lam, shift.ca_lam.title())
                    
                    shift_info = {
                        'type': shift_type,
                        'label': shift_label,
                        'hours': hours
                    }
                    day_shifts.append(shift_info)
                    total_hours += hours
            
            week_schedule.append({'shifts': day_shifts})
            current_date += timedelta(days=1)
        
        staff_list.append({
            'id': staff_member.id,
            'ho_ten': staff_member.ho_ten,
            'anh_dai_dien': staff_member.anh_dai_dien or '/static/img/avatar-default.png',
            'week_schedule': week_schedule,
            'total_hours': total_hours
        })
    
    context = {
        'staff': staff,
        'staff_list': staff_list,
        'schedules': schedule_dict,
        'week_days': week_days,
        'week_start': filter_start,
        'week_end': filter_end,
        'view_type': view_type,
        'from_date': from_date,
        'to_date': to_date,
        'staff_id': staff_id,
        # Stats
        'total_staff': total_staff,
        'working_today': working_today,
        'off_today': off_today,
        'total_shifts_week': total_shifts_week,
        'pending_leaves': pending_leaves,
        'avg_hours': avg_hours,
        'leave_requests': leave_requests,
    }
    
    return render(request, 'admin/work-schedule.html', context)
# - admin_leave_request_approve
@require_role(['quan_ly'])
def admin_leave_request_approve(request, leave_id):
    """Approve leave request"""
    if request.method == 'POST':
        try:
            from barbershop.models import DonXinNghi
            leave_request = get_object_or_404(DonXinNghi, id=leave_id, da_xoa=False)
            leave_request.trang_thai = 'da_duyet'
            
            # Get current user from session
            current_user_id = request.session.get('user_id')
            if current_user_id:
                try:
                    current_user = NguoiDung.objects.get(id=current_user_id)
                    leave_request.nguoi_duyet = current_user
                except NguoiDung.DoesNotExist:
                    pass  # Leave nguoi_duyet as None if user not found
            
            leave_request.save()
            
            return JsonResponse({
                'success': True,
                'message': 'ÄÃ£ duyá»t ÄÆ¡n xin nghá»!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Lá»i: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

# - admin_leave_request_reject
@require_role(['quan_ly'])
def admin_leave_request_reject(request, leave_id):
    """Reject leave request"""
    if request.method == 'POST':
        try:
            from barbershop.models import DonXinNghi
            leave_request = get_object_or_404(DonXinNghi, id=leave_id, da_xoa=False)
            leave_request.trang_thai = 'tu_choi'
            leave_request.ly_do_tu_choi = request.POST.get('reason', '')
            
            # Get current user from session
            current_user_id = request.session.get('user_id')
            if current_user_id:
                try:
                    current_user = NguoiDung.objects.get(id=current_user_id)
                    leave_request.nguoi_duyet = current_user
                except NguoiDung.DoesNotExist:
                    pass  # Leave nguoi_duyet as None if user not found
            
            leave_request.save()
            
            return JsonResponse({
                'success': True,
                'message': 'ÄÃ£ tá»« chá»i ÄÆ¡n xin nghá»!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Lá»i: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - admin_leave_approve (dashboard action)
@require_role(['quan_ly'])
def admin_leave_approve(request, leave_id):
    """Approve leave request from dashboard"""
    if request.method == 'POST':
        try:
            leave = get_object_or_404(DonXinNghi, id=leave_id, da_xoa=False)
            leave.trang_thai = 'da_duyet'
            
            # Get user instance instead of just ID
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    nguoi_duyet = NguoiDung.objects.get(id=user_id)
                    leave.nguoi_duyet = nguoi_duyet
                except NguoiDung.DoesNotExist:
                    pass
                    
            # ngay_cap_nhat will be automatically updated due to auto_now=True
            leave.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'ÄÃ£ phÃª duyá»t yÃªu cáº§u nghá» phÃ©p!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - admin_leave_reject (dashboard action)
@require_role(['quan_ly'])
def admin_leave_reject(request, leave_id):
    """Reject leave request from dashboard"""
    if request.method == 'POST':
        try:
            leave = get_object_or_404(DonXinNghi, id=leave_id, da_xoa=False)
            leave.trang_thai = 'tu_choi'
            
            # Get user instance instead of just ID
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    nguoi_duyet = NguoiDung.objects.get(id=user_id)
                    leave.nguoi_duyet = nguoi_duyet
                except NguoiDung.DoesNotExist:
                    pass
                    
            # ngay_cap_nhat will be automatically updated due to auto_now=True
            leave.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'ÄÃ£ tá»« chá»i yÃªu cáº§u nghá» phÃ©p!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - admin_attendance
@require_role(['quan_ly'])
def admin_attendance(request):
    """Attendance Management - Full Implementation"""
    from django.db.models import Q, Sum, Avg, Count
    from datetime import datetime, timedelta
    
    today = timezone.now().date()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'checkin':
            try:
                staff_id = request.POST.get('staff_id')
                checkin_time = request.POST.get('checkin_time')
                
                staff = get_object_or_404(NguoiDung, id=staff_id, vai_tro='nhan_vien')
                
                # Parse time
                if checkin_time:
                    checkin_time_obj = datetime.strptime(checkin_time, '%H:%M').time()
                else:
                    checkin_time_obj = timezone.now().time()
                
                # Create or update attendance
                attendance, created = ChamCong.objects.get_or_create(
                    nhan_vien=staff,
                    ngay_lam=today,
                    defaults={
                        'gio_vao': checkin_time_obj,
                        'trang_thai_vao': 'dung_gio' if checkin_time_obj <= time(8, 15) else 'tre'
                    }
                )
                
                if not created and not attendance.gio_vao:
                    attendance.gio_vao = checkin_time_obj
                    attendance.trang_thai_vao = 'dung_gio' if checkin_time_obj <= time(8, 15) else 'tre'
                    attendance.save()
                
                return JsonResponse({'success': True, 'message': 'Check-in thành công!'})
                
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Lỗi: {str(e)}'})
        
        elif action == 'checkout':
            try:
                staff_id = request.POST.get('staff_id')
                checkout_time = request.POST.get('checkout_time')
                
                staff = get_object_or_404(NguoiDung, id=staff_id, vai_tro='nhan_vien')
                
                # Parse time
                if checkout_time:
                    checkout_time_obj = datetime.strptime(checkout_time, '%H:%M').time()
                else:
                    checkout_time_obj = timezone.now().time()
                
                # Update attendance
                attendance = get_object_or_404(ChamCong, nhan_vien=staff, ngay_lam=today)
                attendance.gio_ra = checkout_time_obj
                attendance.trang_thai_ra = 'dung_gio' if checkout_time_obj >= time(17, 0) else 'som'
                attendance.save()  # This will trigger calculate_work_hours()
                
                return JsonResponse({'success': True, 'message': 'Check-out thành công!'})
                
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Lỗi: {str(e)}'})
        
        elif action == 'mark_absent':
            try:
                staff_id = request.POST.get('staff_id')
                reason = request.POST.get('reason', '')
                
                staff = get_object_or_404(NguoiDung, id=staff_id, vai_tro='nhan_vien')
                
                # Create absence record
                ChamCong.objects.update_or_create(
                    nhan_vien=staff,
                    ngay_lam=today,
                    defaults={
                        'trang_thai_vao': 'vang_mat',
                        'trang_thai_ra': 'vang_mat',
                        'ghi_chu': reason
                    }
                )
                
                return JsonResponse({'success': True, 'message': 'Đã ghi nhận vắng mặt!'})
                
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Lỗi: {str(e)}'})
    
    # Get filter parameters
    filter_date = request.GET.get('date', today.strftime('%Y-%m-%d'))
    filter_staff = request.GET.get('staff', '')
    
    try:
        filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
    except:
        filter_date_obj = today
    
    # Get staff list
    staff_list = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        da_xoa=False,
        trang_thai=True
    ).order_by('ho_ten')
    
    # Get today's schedules
    schedules = LichLamViec.objects.filter(
        ngay_lam=filter_date_obj,
        da_xoa=False
    ).select_related('nhan_vien')
    
    # Get attendance records for the date
    attendances = ChamCong.objects.filter(
        ngay_lam=filter_date_obj
    ).select_related('nhan_vien')
    
    if filter_staff:
        attendances = attendances.filter(nhan_vien_id=filter_staff)
    
    # Combine schedule and attendance data
    attendance_data = []
    for staff in staff_list:
        if filter_staff and str(staff.id) != filter_staff:
            continue
            
        # Find schedule
        schedule = schedules.filter(nhan_vien=staff).first()
        
        # Find attendance
        attendance = attendances.filter(nhan_vien=staff).first()
        
        attendance_data.append({
            'staff': staff,
            'schedule': schedule,
            'attendance': attendance,
            'has_checkin': attendance and attendance.gio_vao,
            'has_checkout': attendance and attendance.gio_ra,
            'is_absent': attendance and attendance.trang_thai_vao == 'vang_mat'
        })
    
    # Calculate summary stats
    total_staff = staff_list.count()
    present_count = attendances.exclude(trang_thai_vao='vang_mat').count()
    absent_count = attendances.filter(trang_thai_vao='vang_mat').count()
    late_count = attendances.filter(trang_thai_vao='tre').count()
    
    context = {
        'attendance_data': attendance_data,
        'today': today,
        'filter_date': filter_date,
        'filter_date_obj': filter_date_obj,
        'filter_staff': filter_staff,
        'staff_list': staff_list,
        'total_staff': total_staff,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'schedules': schedules,
    }
    return render(request, 'admin/attendance.html', context)
# - admin_salary
@require_role(['quan_ly'])
def admin_salary(request):
    """Salary Management - Placeholder"""
    staff = NguoiDung.objects.filter(
        vai_tro='nhan_vien',
        da_xoa=False
    ).select_related('thong_tin_nhan_vien')
    
    context = {
        'staff': staff,
    }
    return render(request, 'admin/salary.html', context)
# - admin_export_schedule
@require_role(['quan_ly'])
def admin_export_schedule(request):
    """Export Schedule"""
    schedules = LichLamViec.objects.filter(
        da_xoa=False
    ).select_related('nhan_vien').order_by('ngay_lam', 'ca_lam')
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="lich_lam_viec.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['NhÃ¢n viÃªn', 'NgÃ y', 'Ca lÃ m viá»c', 'Giá» báº¯t Äáº§u', 'Giá» káº¿t thÃºc'])
    
    for schedule in schedules:
        writer.writerow([
            schedule.nhan_vien.ho_ten,
            schedule.ngay_lam,
            schedule.ca_lam,
            schedule.gio_bat_dau,
            schedule.gio_ket_thuc
        ])
    
    return response
# - staff_today_bookings
@require_role(['nhan_vien', 'quan_ly'])
def staff_today_bookings(request):
    """Today's Bookings"""
    user_id = request.session.get('user_id')
    today = timezone.now().date()
    
    # Get all bookings for today
    bookings = DatLich.objects.filter(
        nhan_vien_id=user_id,
        ngay_hen=today,
        da_xoa=False
    ).select_related('khach_hang').prefetch_related(
        'dich_vu_dat_lich__dich_vu'
    ).order_by('gio_hen')
    
    # Calculate statistics
    total_bookings = bookings.count()
    pending_count = bookings.filter(trang_thai='cho_xac_nhan').count()
    confirmed_count = bookings.filter(trang_thai='da_xac_nhan').count()
    in_progress_count = bookings.filter(trang_thai='da_checkin').count()
    completed_count = bookings.filter(trang_thai='hoan_thanh').count()
    
    context = {
        'bookings': bookings,
        'today': today,
        'current_date': today,
        'total_bookings': total_bookings,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    }
    return render(request, 'staff/today-bookings.html', context)
# - staff_schedule
@require_role(['nhan_vien', 'quan_ly'])
def staff_schedule(request):
    """My Schedule"""
    user_id = request.session.get('user_id')
    today = timezone.now().date()
    current_time = timezone.now().time()
    
    # Get current month data
    month_start = today.replace(day=1)
    next_month = month_start.replace(month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1)
    
    # Get current shift if working now
    current_shift = LichLamViec.objects.filter(
        nhan_vien_id=user_id,
        ngay_lam=today,
        gio_bat_dau__lte=current_time,
        gio_ket_thuc__gte=current_time,
        da_xoa=False
    ).first()
    
    # Get month schedules
    month_schedules = LichLamViec.objects.filter(
        nhan_vien_id=user_id,
        ngay_lam__gte=month_start,
        ngay_lam__lt=next_month,
        da_xoa=False
    ).order_by('ngay_lam')
    
    # Calculate month statistics
    total_shifts_month = month_schedules.count()
    total_hours_month = 0
    for schedule in month_schedules:
        # Calculate hours (simple estimation: afternoon=8h, morning/evening=4h)
        if schedule.ca_lam == 'ca_day':
            total_hours_month += 8
        else:
            total_hours_month += 4
    
    # Get upcoming shifts (next 7 days)
    upcoming_shifts_list = LichLamViec.objects.filter(
        nhan_vien_id=user_id,
        ngay_lam__gte=today,
        ngay_lam__lte=today + timedelta(days=7),
        da_xoa=False
    ).order_by('ngay_lam')[:10]
    
    # Get leave requests for display (recent 5 requests)
    my_leave_requests = DonXinNghi.objects.filter(
        nhan_vien_id=user_id,
        da_xoa=False
    ).order_by('-ngay_tao')[:5]
    
    # Get all approved leaves for calendar (not sliced)
    approved_leaves = DonXinNghi.objects.filter(
        nhan_vien_id=user_id,
        trang_thai='da_duyet',
        da_xoa=False
    )
    
    # Create calendar data for current month
    calendar_days = []
    
    # Get first day of month and calculate calendar start
    first_day = month_start
    first_weekday = first_day.weekday()  # 0=Monday, 6=Sunday
    
    # Add days from previous month to fill the first week
    calendar_start = first_day - timedelta(days=first_weekday)
    
    # Generate 42 days (6 weeks) for calendar
    for i in range(42):
        day_date = calendar_start + timedelta(days=i)
        
        # Get shifts for this day
        day_shifts = month_schedules.filter(ngay_lam=day_date)
        shifts_data = []
        for shift in day_shifts:
            shifts_data.append({
                'type': shift.ca_lam,
                'label': shift.get_ca_lam_display(),
                'time': f"{shift.gio_bat_dau.strftime('%H:%M')}-{shift.gio_ket_thuc.strftime('%H:%M')}"
            })
        
        # Check if has leave request
        has_leave = approved_leaves.filter(
            tu_ngay__lte=day_date,
            den_ngay__gte=day_date
        ).exists()
        
        calendar_days.append({
            'date': day_date.strftime('%Y-%m-%d'),
            'day': day_date.day,
            'is_today': day_date == today,
            'is_current_month': day_date.month == today.month,
            'has_shift': len(shifts_data) > 0,
            'is_off': day_date.weekday() == 6,  # Sunday
            'shifts': shifts_data,
            'leave': has_leave
        })
    
    context = {
        'current_shift': current_shift,
        'current_date': today,
        'current_month': today.strftime('%B %Y'),
        'total_shifts_month': total_shifts_month,
        'total_hours_month': total_hours_month,
        'days_off_month': 4,  # Assume 4 Sundays per month
        'upcoming_shifts': upcoming_shifts_list.count(),
        'upcoming_shifts_list': upcoming_shifts_list,
        'my_leave_requests': my_leave_requests,
        'calendar_days': calendar_days,
    }
    return render(request, 'staff/schedule.html', context)

# - staff_register_shift
@require_role(['nhan_vien', 'quan_ly'])
def staff_register_shift(request):
    """Register for work shift"""
    user_id = request.session.get('user_id')
    
    if request.method == 'POST':
        ngay_lam = request.POST.get('ngay_lam')
        ca_lam = request.POST.get('ca_lam')
        ghi_chu = request.POST.get('ghi_chu', '')
        
        # Set default times based on shift
        if ca_lam == 'sang':
            gio_bat_dau = '08:00'
            gio_ket_thuc = '12:00'
        elif ca_lam == 'chieu':
            gio_bat_dau = '13:00'
            gio_ket_thuc = '17:00'
        else:  # toi
            gio_bat_dau = '18:00'
            gio_ket_thuc = '22:00'
        
        LichLamViec.objects.create(
            nhan_vien_id=user_id,
            ngay_lam=ngay_lam,
            ca_lam=ca_lam,
            gio_bat_dau=gio_bat_dau,
            gio_ket_thuc=gio_ket_thuc,
            trang_thai='cho_duyet',
            ghi_chu=ghi_chu,
            da_xoa=False
        )
        
        return redirect('attendance:staff_schedule')
    
    # Get existing shifts
    today = timezone.now().date()
    existing_shifts = LichLamViec.objects.filter(
        nhan_vien_id=user_id,
        ngay_lam__gte=today,
        da_xoa=False
    ).order_by('ngay_lam')
    
    context = {
        'existing_shifts': existing_shifts,
        'today': today,
    }
    return render(request, 'staff/register-shift.html', context)

# - api_attendance_checkin
@require_role(['nhan_vien', 'quan_ly'])
def api_attendance_checkin(request):
    """Check-in attendance via API"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            today = timezone.now().date()
            current_time = timezone.now().time()
            
            # Find current shift
            current_shift = LichLamViec.objects.filter(
                nhan_vien_id=user_id,
                ngay_lam=today,
                gio_bat_dau__lte=current_time,
                gio_ket_thuc__gte=current_time,
                da_xoa=False
            ).first()
            
            if not current_shift:
                return JsonResponse({
                    'success': False, 
                    'message': 'Không tìm thấy ca làm việc hiện tại!'
                })
            
            # For now, we'll just return success
            return JsonResponse({
                'success': True, 
                'message': 'Check-in thành công!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - api_attendance_checkout
@require_role(['nhan_vien', 'quan_ly'])
def api_attendance_checkout(request):
    """Check-out attendance via API"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            today = timezone.now().date()
            
            # For now, we'll just return success
            return JsonResponse({
                'success': True, 
                'message': 'Check-out thành công!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

# - api_leave_request_create
@require_role(['nhan_vien', 'quan_ly'])
def api_leave_request_create(request):
    """Create leave request via API"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            tu_ngay = request.POST.get('tu_ngay')
            den_ngay = request.POST.get('den_ngay')
            ly_do = request.POST.get('ly_do')
            
            if not all([tu_ngay, den_ngay, ly_do]):
                return JsonResponse({
                    'success': False, 
                    'message': 'Vui lòng điền đầy đủ thông tin!'
                })
            
            # Parse dates
            from datetime import datetime
            tu_ngay_date = datetime.strptime(tu_ngay, '%Y-%m-%d').date()
            den_ngay_date = datetime.strptime(den_ngay, '%Y-%m-%d').date()
            
            # Validate dates
            if tu_ngay_date < timezone.now().date():
                return JsonResponse({
                    'success': False, 
                    'message': 'Không thể đăng ký nghỉ cho ngày trong quá khứ!'
                })
            
            if den_ngay_date < tu_ngay_date:
                return JsonResponse({
                    'success': False, 
                    'message': 'Ngày kết thúc phải sau ngày bắt đầu!'
                })
            
            # Create leave request
            leave = DonXinNghi.objects.create(
                nhan_vien_id=user_id,
                tu_ngay=tu_ngay_date,
                den_ngay=den_ngay_date,
                ly_do=ly_do,
                trang_thai='cho_duyet',
                da_xoa=False
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Đã gửi đơn xin nghỉ phép!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - api_leave_request_cancel
@require_role(['nhan_vien', 'quan_ly'])
def api_leave_request_cancel(request, leave_id):
    """Cancel leave request via API"""
    if request.method == 'DELETE':
        try:
            user_id = request.session.get('user_id')
            leave = get_object_or_404(DonXinNghi, id=leave_id, nhan_vien_id=user_id, da_xoa=False)
            
            if leave.trang_thai != 'cho_duyet':
                return JsonResponse({
                    'success': False, 
                    'message': 'Chỉ có thể hủy đơn đang chờ duyệt!'
                })
            
            leave.da_xoa = True
            leave.ngay_xoa = timezone.now()
            leave.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Đã hủy đơn xin nghỉ!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - api_schedule_day_detail
@require_role(['nhan_vien', 'quan_ly'])
def api_schedule_day_detail(request, date_str):
    """Get schedule details for a specific day"""
    if request.method == 'GET':
        try:
            user_id = request.session.get('user_id')
            
            # Parse date
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Get shifts for this day
            shifts = LichLamViec.objects.filter(
                nhan_vien_id=user_id,
                ngay_lam=date_obj,
                da_xoa=False
            )
            
            shifts_data = []
            for shift in shifts:
                shifts_data.append({
                    'label': shift.get_ca_lam_display(),
                    'time': f"{shift.gio_bat_dau.strftime('%H:%M')} - {shift.gio_ket_thuc.strftime('%H:%M')}",
                    'status': shift.trang_thai
                })
            
            # Get leave status
            leave = DonXinNghi.objects.filter(
                nhan_vien_id=user_id,
                tu_ngay__lte=date_obj,
                den_ngay__gte=date_obj,
                trang_thai='da_duyet',
                da_xoa=False
            ).first()
            
            data = {
                'date': date_str,
                'shifts': shifts_data,
                'leave': {
                    'ly_do': leave.ly_do,
                    'trang_thai': leave.get_trang_thai_display()
                } if leave else None
            }
            
            return JsonResponse(data)
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
