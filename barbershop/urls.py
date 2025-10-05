"""
URL configuration for barbershop project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from barbershop import views

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    
    # Auth URLs
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin URLs
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/staff/', views.admin_staff, name='admin_staff'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/invoices/', views.admin_invoices, name='admin_invoices'),
    path('admin/customers/', views.admin_customers, name='admin_customers'),
    path('admin/services/', views.admin_services, name='admin_services'),
    path('admin/work-schedule/', views.admin_work_schedule, name='admin_work_schedule'),
    path('admin/promotions/', views.admin_promotions, name='admin_promotions'),
    path('admin/promotions/stats/<int:voucher_id>/', views.admin_promotion_stats, name='admin_promotion_stats'),
    path('admin/promotions/delete/<int:voucher_id>/', views.admin_delete_promotion, name='admin_delete_promotion'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('admin/reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin/reviews/export/', views.admin_reviews_export, name='admin_reviews_export'),
    path('api/reviews/<int:review_id>/', views.admin_review_detail, name='admin_review_detail'),
    path('api/reviews/<int:review_id>/reply/', views.admin_review_reply, name='admin_review_reply'),
    path('api/reviews/<int:review_id>/delete/', views.admin_review_delete, name='admin_review_delete'),
    path('admin/pos-report/', views.admin_pos_report, name='admin_pos_report'),
    path('admin/settings/', views.admin_settings, name='admin_settings'),
    # Settings API endpoints
    path('api/settings/general/', views.admin_settings_api_general, name='admin_settings_api_general'),
    path('api/settings/business-hours/', views.admin_settings_api_business_hours, name='admin_settings_api_business_hours'),
    path('api/settings/services/', views.admin_settings_api_services, name='admin_settings_api_services'),
    path('api/settings/payments/', views.admin_settings_api_payments, name='admin_settings_api_payments'),
    # path('admin/inventory/', views.admin_inventory, name='admin_inventory'),  # Tạm ẩn trang kho hàng
    path('admin/salary/', views.admin_salary, name='admin_salary'),
    path('admin/attendance/', views.admin_attendance, name='admin_attendance'),
    path('admin/loyalty/', views.admin_loyalty, name='admin_loyalty'),
    path('admin/staff/<int:staff_id>/', views.admin_staff_detail, name='admin_staff_detail'),
    path('admin/staff/edit/<int:staff_id>/', views.admin_staff_edit, name='admin_staff_edit'),
    path('admin/bookings/create/', views.admin_bookings_create, name='admin_bookings_create'),
    path('test/promotions/', views.test_promotions, name='test_promotions'),
    path('admin/bookings/<int:booking_id>/', views.admin_booking_detail, name='admin_booking_detail'),
    path('admin/bookings/<int:booking_id>/cancel/', views.admin_booking_cancel, name='admin_booking_cancel'),
    path('admin/bookings/<int:booking_id>/checkin/', views.admin_booking_checkin, name='admin_booking_checkin'),
    path('admin/bookings/<int:booking_id>/complete/', views.admin_booking_complete, name='admin_booking_complete'),
    path('admin/bookings/export/', views.admin_bookings_export, name='admin_bookings_export'),
    path('admin/invoices/export/excel/', views.admin_invoices_export_excel, name='admin_invoices_export_excel'),
    path('admin/invoices/export/pdf/', views.admin_invoices_export_pdf, name='admin_invoices_export_pdf'),
    path('admin/reports/export/excel/', views.admin_reports_export_excel, name='admin_reports_export_excel'),
    path('admin/reports/export/pdf/', views.admin_reports_export_pdf, name='admin_reports_export_pdf'),
    path('admin/leave-requests/<int:leave_id>/approve/', views.admin_leave_request_approve, name='admin_leave_request_approve'),
    path('admin/leave-requests/<int:leave_id>/reject/', views.admin_leave_request_reject, name='admin_leave_request_reject'),
    path('admin/promotions/export/', views.admin_export_promotions, name='admin_promotions_export'),
    path('admin/schedule/export/', views.admin_export_schedule, name='admin_schedule_export'),
    path('admin/content/', views.admin_content, name='admin_content'),
    
    # Staff URLs
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/pos/', views.staff_pos, name='staff_pos'),
    path('staff/today-bookings/', views.staff_today_bookings, name='staff_today_bookings'),
    path('staff/schedule/', views.staff_schedule, name='staff_schedule'),
    path('staff/register-shift/', views.staff_register_shift, name='staff_register_shift'),
    path('staff/my-customers/', views.staff_my_customers, name='staff_my_customers'),
    path('staff/revenue/', views.staff_revenue, name='staff_revenue'),
    path('staff/profile/', views.staff_profile, name='staff_profile'),
    path('staff/commission/', views.staff_commission, name='staff_commission'),
    path('staff/bookings/create/', views.staff_bookings_create, name='staff_bookings_create'),
    
    # API URLs
    path('api/search-customer/', views.api_search_customer, name='api_search_customer'),
    path('api/customers/<int:customer_id>/', views.api_customer_detail, name='api_customer_detail'),
    path('api/load-booking/', views.api_load_booking, name='api_load_booking'),
    
    # Services API URLs
    path('api/services/', views.api_service_crud, name='api_services_create'),
    path('api/services/<int:service_id>/', views.api_service_crud, name='api_services_detail'),
    path('api/services/<int:service_id>/toggle-status/', views.api_service_toggle_status, name='api_service_toggle_status'),
    path('api/services/update-order/', views.api_service_update_order, name='api_service_update_order'),
    
    # Dashboard action endpoints
    path('admin/booking-approve/<int:booking_id>/', views.admin_booking_approve, name='admin_booking_approve'),
    path('admin/booking-reject/<int:booking_id>/', views.admin_booking_reject, name='admin_booking_reject'),
    path('admin/leave-approve/<int:leave_id>/', views.admin_leave_approve, name='admin_leave_approve'),
    path('admin/leave-reject/<int:leave_id>/', views.admin_leave_reject, name='admin_leave_reject'),
    
    # Staff action endpoints
    path('staff/booking-checkin/<int:booking_id>/', views.staff_booking_checkin, name='staff_booking_checkin'),
    path('staff/booking-complete/<int:booking_id>/', views.staff_booking_complete, name='staff_booking_complete'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
