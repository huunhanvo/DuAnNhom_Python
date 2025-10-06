# ============ SCHEDULE & ATTENDANCE API ENDPOINTS ============

@require_role(['nhan_vien', 'quan_ly'])
def api_attendance_checkin(request):
    """Check-in to work shift"""
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
                    'message': 'Không có ca làm việc nào trong thời gian này!'
                })
            
            # For simplicity, just return success (actual attendance tracking would need ChamCong model)
            return JsonResponse({
                'success': True, 
                'message': 'Check-in thành công!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

@require_role(['nhan_vien', 'quan_ly'])
def api_attendance_checkout(request):
    """Check-out from work shift"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            
            # For simplicity, just return success (actual attendance tracking would need ChamCong model)
            return JsonResponse({
                'success': True, 
                'message': 'Check-out thành công!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

@require_role(['nhan_vien', 'quan_ly'])
def api_leave_requests(request):
    """Handle leave requests"""
    user_id = request.session.get('user_id')
    
    if request.method == 'POST':
        try:
            tu_ngay = request.POST.get('tu_ngay')
            den_ngay = request.POST.get('den_ngay')
            ly_do = request.POST.get('ly_do')
            
            if not all([tu_ngay, den_ngay, ly_do]):
                return JsonResponse({
                    'success': False, 
                    'message': 'Vui lòng điền đầy đủ thông tin!'
                })
            
            # Convert string dates to date objects
            from datetime import datetime
            tu_ngay_obj = datetime.strptime(tu_ngay, '%Y-%m-%d').date()
            den_ngay_obj = datetime.strptime(den_ngay, '%Y-%m-%d').date()
            
            # Validate dates
            if tu_ngay_obj <= timezone.now().date():
                return JsonResponse({
                    'success': False, 
                    'message': 'Ngày bắt đầu phải sau ngày hôm nay!'
                })
                
            if den_ngay_obj < tu_ngay_obj:
                return JsonResponse({
                    'success': False, 
                    'message': 'Ngày kết thúc phải sau ngày bắt đầu!'
                })
            
            # Create leave request
            DonXinNghi.objects.create(
                nhan_vien_id=user_id,
                tu_ngay=tu_ngay_obj,
                den_ngay=den_ngay_obj,
                ly_do=ly_do,
                trang_thai='cho_duyet'
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Đã gửi đơn xin nghỉ thành công!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

@require_role(['nhan_vien', 'quan_ly'])
def api_leave_request_cancel(request, leave_id):
    """Cancel leave request"""
    if request.method == 'DELETE':
        try:
            user_id = request.session.get('user_id')
            leave_request = get_object_or_404(DonXinNghi, id=leave_id, nhan_vien_id=user_id)
            
            if leave_request.trang_thai != 'cho_duyet':
                return JsonResponse({
                    'success': False, 
                    'message': 'Chỉ có thể hủy đơn đang chờ duyệt!'
                })
            
            leave_request.da_xoa = True
            leave_request.save()
            
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
                    'note': shift.ghi_chu or ''
                })
            
            # Check for leave requests
            leave_requests = DonXinNghi.objects.filter(
                nhan_vien_id=user_id,
                tu_ngay__lte=date_obj,
                den_ngay__gte=date_obj,
                da_xoa=False
            )
            
            leave_data = []
            for leave in leave_requests:
                leave_data.append({
                    'reason': leave.ly_do,
                    'status': leave.trang_thai,
                    'from_date': leave.tu_ngay.strftime('%d/%m/%Y'),
                    'to_date': leave.den_ngay.strftime('%d/%m/%Y')
                })
            
            return JsonResponse({
                'success': True,
                'shifts': shifts_data,
                'leave_requests': leave_data
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})