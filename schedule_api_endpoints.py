# ============ SCHEDULE & ATTENDANCE API ENDPOINTS ============

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
            
            # Create or update attendance record (assuming you have ChamCong model)
            # For now, we'll just return success
            return JsonResponse({
                'success': True, 
                'message': 'Check-in thành công!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

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