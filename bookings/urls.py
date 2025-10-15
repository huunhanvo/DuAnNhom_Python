"""
URL configuration for bookings app (Bookings, Invoices, POS)
"""
from django.urls import path
from . import views
# Import customer booking views
from .customer_booking_views import (
    booking_step1, booking_step2, booking_step3, booking_step4,
    create_booking, booking_success, get_time_slots, validate_voucher
)

app_name = 'bookings'

urlpatterns = [
    # Admin Bookings
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/bookings/create/', views.admin_bookings_create, name='admin_bookings_create'),
    path('admin/bookings/<int:booking_id>/', views.admin_booking_detail, name='admin_booking_detail'),
    path('admin/bookings/<int:booking_id>/cancel/', views.admin_booking_cancel, name='admin_booking_cancel'),
    path('admin/bookings/<int:booking_id>/checkin/', views.admin_booking_checkin, name='admin_booking_checkin'),
    path('admin/bookings/<int:booking_id>/complete/', views.admin_booking_complete, name='admin_booking_complete'),
    path('admin/bookings/export/', views.admin_bookings_export, name='admin_bookings_export'),
    
    # Dashboard action endpoints
    path('admin/booking-approve/<int:booking_id>/', views.admin_booking_approve, name='admin_booking_approve'),
    path('admin/booking-reject/<int:booking_id>/', views.admin_booking_reject, name='admin_booking_reject'),
    
    # Admin Invoices
    path('admin/invoices/', views.admin_invoices, name='admin_invoices'),
    path('admin/invoices/export/excel/', views.admin_invoices_export_excel, name='admin_invoices_export_excel'),
    path('admin/invoices/export/pdf/', views.admin_invoices_export_pdf, name='admin_invoices_export_pdf'),
    
    # Staff POS
    path('staff/pos/', views.staff_pos, name='staff_pos'),
    
    # Staff Bookings
    path('staff/bookings/create/', views.staff_bookings_create, name='staff_bookings_create'),
    
    # Staff action endpoints
    path('staff/booking-checkin/<int:booking_id>/', views.staff_booking_checkin, name='staff_booking_checkin'),
    path('staff/booking-complete/<int:booking_id>/', views.staff_booking_complete, name='staff_booking_complete'),
    
    # API URLs
    path('api/search-customer/', views.api_search_customer, name='api_search_customer'),
    path('api/load-booking/', views.api_load_booking, name='api_load_booking'),
    
    # Booking API endpoints
    path('api/bookings/<int:booking_id>/confirm/', views.api_booking_confirm, name='api_booking_confirm'),
    path('api/bookings/<int:booking_id>/check-in/', views.api_booking_checkin, name='api_booking_checkin'),
    path('api/bookings/<int:booking_id>/complete/', views.api_booking_complete_today, name='api_booking_complete_today'),
    path('api/bookings/<int:booking_id>/cancel/', views.api_booking_cancel, name='api_booking_cancel'),
    path('api/bookings/<int:booking_id>/', views.api_booking_detail, name='api_booking_detail'),
    
    # ==================== CUSTOMER BOOKING FLOW ====================
    path('bookings/step1/', booking_step1, name='booking_step1'),
    path('bookings/step2/', booking_step2, name='booking_step2'),
    path('bookings/step3/', booking_step3, name='booking_step3'),
    path('bookings/step4/', booking_step4, name='booking_step4'),
    path('bookings/create/', create_booking, name='create_booking'),
    path('bookings/success/', booking_success, name='booking_success'),
    
    # AJAX endpoints
    path('bookings/api/time-slots/', get_time_slots, name='get_time_slots'),
    path('bookings/api/validate-voucher/', validate_voucher, name='validate_voucher'),
    
    # Debug endpoint (development only)
    path('bookings/debug-session/', lambda request: __import__('bookings.debug_views', fromlist=['debug_booking_session']).debug_booking_session(request), name='debug_booking_session'),
    path('bookings/test/', lambda request: __import__('django.shortcuts', fromlist=['render']).render(request, 'test_booking.html'), name='test_booking'),
    path('bookings/debug/', lambda request: __import__('django.shortcuts', fromlist=['render']).render(request, 'debug_booking.html'), name='debug_booking'),
]
