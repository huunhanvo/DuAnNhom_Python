"""
Script để thêm comment đánh dấu vị trí di chuyển code trong barbershop/views.py
"""

# Mapping: function_name -> (app_name, description)
VIEW_MAPPING = {
    # CORE APP - Dashboard, Settings
    'admin_dashboard': ('core', 'Admin Dashboard'),
    'staff_dashboard': ('core', 'Staff Dashboard'),
    'admin_settings': ('core', 'Admin Settings'),
    'admin_settings_api_general': ('core', 'Settings API - General'),
    'admin_settings_api_business_hours': ('core', 'Settings API - Business Hours'),
    'admin_settings_api_services': ('core', 'Settings API - Services'),
    'admin_settings_api_payments': ('core', 'Settings API - Payments'),
    'admin_content': ('core', 'Admin Content Management'),
    
    # ACCOUNTS APP - Staff, Customers, Profile
    'admin_staff': ('accounts', 'Admin Staff Management'),
    'admin_staff_detail': ('accounts', 'Admin Staff Detail'),
    'admin_staff_edit': ('accounts', 'Admin Staff Edit'),
    'admin_customers': ('accounts', 'Admin Customers Management'),
    'staff_profile': ('accounts', 'Staff Profile Page'),
    'api_staff_update_profile': ('accounts', 'API Staff Update Profile'),
    'api_staff_change_password': ('accounts', 'API Staff Change Password'),
    'api_staff_upload_avatar': ('accounts', 'API Staff Upload Avatar'),
    'api_staff_update_notifications': ('accounts', 'API Staff Update Notifications'),
    'staff_my_customers': ('accounts', 'Staff My Customers'),
    'api_customer_detail': ('accounts', 'API Customer Detail'),
    'api_customer_detail_staff': ('accounts', 'API Customer Detail for Staff'),
    'staff_customers_export': ('accounts', 'Staff Customers Export'),
    
    # SERVICES APP - Services, Promotions, Vouchers
    'admin_services': ('services', 'Admin Services Management'),
    'api_service_crud': ('services', 'API Service CRUD'),
    'api_service_toggle_status': ('services', 'API Service Toggle Status'),
    'api_service_update_order': ('services', 'API Service Update Order'),
    'admin_promotions': ('services', 'Admin Promotions Management'),
    'admin_delete_promotion': ('services', 'Admin Delete Promotion'),
    'admin_promotion_stats': ('services', 'Admin Promotion Stats'),
    'admin_export_promotions': ('services', 'Admin Export Promotions'),
    'test_promotions': ('services', 'Test Promotions'),
    
    # BOOKINGS APP - Bookings, Invoices, POS
    'admin_bookings': ('bookings', 'Admin Bookings Management'),
    'admin_bookings_create': ('bookings', 'Admin Bookings Create'),
    'admin_booking_detail': ('bookings', 'Admin Booking Detail'),
    'admin_booking_cancel': ('bookings', 'Admin Booking Cancel'),
    'admin_booking_checkin': ('bookings', 'Admin Booking Check-in'),
    'admin_booking_complete': ('bookings', 'Admin Booking Complete'),
    'admin_bookings_export': ('bookings', 'Admin Bookings Export'),
    'admin_booking_approve': ('bookings', 'Admin Booking Approve (Dashboard Action)'),
    'admin_booking_reject': ('bookings', 'Admin Booking Reject (Dashboard Action)'),
    'admin_invoices': ('bookings', 'Admin Invoices Management'),
    'admin_invoices_export_excel': ('bookings', 'Admin Invoices Export Excel'),
    'admin_invoices_export_pdf': ('bookings', 'Admin Invoices Export PDF'),
    'staff_pos': ('bookings', 'Staff POS System'),
    'staff_bookings_create': ('bookings', 'Staff Bookings Create'),
    'api_search_customer': ('bookings', 'API Search Customer'),
    'api_load_booking': ('bookings', 'API Load Booking'),
    'api_booking_confirm': ('bookings', 'API Booking Confirm'),
    'api_booking_checkin': ('bookings', 'API Booking Check-in'),
    'api_booking_complete_today': ('bookings', 'API Booking Complete Today'),
    'api_booking_cancel': ('bookings', 'API Booking Cancel'),
    'api_booking_detail': ('bookings', 'API Booking Detail'),
    'staff_booking_checkin': ('bookings', 'Staff Booking Check-in (Staff Action)'),
    'staff_booking_complete': ('bookings', 'Staff Booking Complete (Staff Action)'),
    
    # ATTENDANCE APP - Work Schedule, Leave, Salary
    'admin_work_schedule': ('attendance', 'Admin Work Schedule'),
    'admin_leave_request_approve': ('attendance', 'Admin Leave Request Approve'),
    'admin_leave_request_reject': ('attendance', 'Admin Leave Request Reject'),
    'admin_leave_approve': ('attendance', 'Admin Leave Approve (Dashboard Action)'),
    'admin_leave_reject': ('attendance', 'Admin Leave Reject (Dashboard Action)'),
    'admin_attendance': ('attendance', 'Admin Attendance Management'),
    'admin_salary': ('attendance', 'Admin Salary Management'),
    'admin_export_schedule': ('attendance', 'Admin Export Schedule'),
    'staff_today_bookings': ('attendance', 'Staff Today Bookings'),
    'staff_schedule': ('attendance', 'Staff Schedule'),
    'staff_register_shift': ('attendance', 'Staff Register Shift'),
    'api_attendance_checkin': ('attendance', 'API Attendance Check-in'),
    'api_attendance_checkout': ('attendance', 'API Attendance Check-out'),
    'api_leave_request_create': ('attendance', 'API Leave Request Create'),
    'api_leave_request_cancel': ('attendance', 'API Leave Request Cancel'),
    'api_schedule_day_detail': ('attendance', 'API Schedule Day Detail'),
    
    # REPORTS APP - Analytics, Exports
    'admin_reports': ('reports', 'Admin Reports & Analytics'),
    'admin_reports_export_excel': ('reports', 'Admin Reports Export Excel'),
    'admin_reports_export_pdf': ('reports', 'Admin Reports Export PDF'),
    'admin_pos_report': ('reports', 'Admin POS Report'),
    
    # REVIEWS APP - Reviews, Loyalty
    'admin_reviews': ('reviews', 'Admin Reviews Management'),
    'admin_loyalty': ('reviews', 'Admin Loyalty Program'),
    'admin_review_reply': ('reviews', 'Admin Review Reply'),
    'admin_review_detail': ('reviews', 'Admin Review Detail'),
    'admin_review_delete': ('reviews', 'Admin Review Delete'),
    'admin_reviews_export': ('reviews', 'Admin Reviews Export'),
}

def add_comments_to_views():
    """Thêm comments vào barbershop/views.py"""
    
    with open('barbershop/views.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Kiểm tra xem dòng này có phải là khai báo function không
        if line.startswith('def ') or line.startswith('@'):
            # Tìm tên function
            if line.startswith('def '):
                func_name = line.split('def ')[1].split('(')[0].strip()
                
                # Kiểm tra xem function này có trong mapping không
                if func_name in VIEW_MAPPING:
                    app_name, description = VIEW_MAPPING[func_name]
                    
                    # Thêm comment TRƯỚC khai báo function
                    comment_start = f"\n# ========== BẮT ĐẦU - Di chuyển tới {app_name}/views.py ==========\n"
                    comment_start += f"# Function: {func_name} - {description}\n"
                    comment_start += f"# Hướng dẫn: Copy toàn bộ code của function '{func_name}' vào file {app_name}/views.py\n"
                    new_lines.append(comment_start)
                    
                    # Thêm decorator nếu có
                    # Lùi lại để tìm decorator
                    decorator_start = i - 1
                    while decorator_start >= 0 and lines[decorator_start].startswith('@'):
                        decorator_start -= 1
                    decorator_start += 1
                    
                    # Thêm tất cả decorators và function
                    for j in range(decorator_start, i + 1):
                        new_lines.append(lines[j])
                    
                    # Tìm toàn bộ nội dung function (cho tới function tiếp theo hoặc comment section)
                    i += 1
                    function_body = []
                    indent_level = None
                    
                    while i < len(lines):
                        current_line = lines[i]
                        
                        # Xác định indent level từ dòng đầu tiên của function body
                        if indent_level is None and current_line.strip() and not current_line.strip().startswith('#'):
                            indent_level = len(current_line) - len(current_line.lstrip())
                        
                        # Nếu gặp function mới hoặc decorator mới, dừng lại
                        if (current_line.startswith('def ') or 
                            (current_line.startswith('@') and not current_line.strip().startswith('#')) or
                            current_line.startswith('# ============')):
                            break
                        
                        # Nếu gặp dòng không indent (cùng cấp với def), dừng lại
                        if indent_level is not None and current_line.strip() and not current_line.strip().startswith('#'):
                            current_indent = len(current_line) - len(current_line.lstrip())
                            if current_indent < indent_level:
                                break
                        
                        function_body.append(current_line)
                        i += 1
                    
                    # Thêm toàn bộ function body
                    new_lines.extend(function_body)
                    
                    # Thêm comment KẾT THÚC
                    comment_end = f"# ========== KẾT THÚC - {func_name} ==========\n\n"
                    new_lines.append(comment_end)
                    
                    continue
        
        new_lines.append(line)
        i += 1
    
    # Ghi lại file
    with open('barbershop/views.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ Đã thêm comments vào barbershop/views.py thành công!")
    print(f"✅ Đã đánh dấu {len(VIEW_MAPPING)} functions cần di chuyển")

if __name__ == '__main__':
    add_comments_to_views()
