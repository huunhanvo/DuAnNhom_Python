"""
URL configuration for attendance app (Work Schedule, Leave Requests, Check-in/out, Salary)
"""
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Admin Work Schedule
    path('admin/work-schedule/', views.admin_work_schedule, name='admin_work_schedule'),
    path('admin/schedule/export/', views.admin_export_schedule, name='admin_schedule_export'),
    
    # Admin Leave Requests
    path('admin/leave-requests/<int:leave_id>/approve/', views.admin_leave_request_approve, name='admin_leave_request_approve'),
    path('admin/leave-requests/<int:leave_id>/reject/', views.admin_leave_request_reject, name='admin_leave_request_reject'),
    
    # Dashboard action endpoints
    path('admin/leave-approve/<int:leave_id>/', views.admin_leave_approve, name='admin_leave_approve'),
    path('admin/leave-reject/<int:leave_id>/', views.admin_leave_reject, name='admin_leave_reject'),
    
    # Admin Attendance & Salary
    path('admin/attendance/', views.admin_attendance, name='admin_attendance'),
    path('admin/salary/', views.admin_salary, name='admin_salary'),
    
    # Staff Today Bookings
    path('staff/today-bookings/', views.staff_today_bookings, name='staff_today_bookings'),
    
    # Staff Schedule
    path('staff/schedule/', views.staff_schedule, name='staff_schedule'),
    path('staff/register-shift/', views.staff_register_shift, name='staff_register_shift'),
    
    # Attendance API endpoints
    path('api/attendance/check-in/', views.api_attendance_checkin, name='api_attendance_checkin'),
    path('api/attendance/check-out/', views.api_attendance_checkout, name='api_attendance_checkout'),
    
    # Leave Request API endpoints
    path('api/leave-requests/', views.api_leave_request_create, name='api_leave_request_create'),
    path('api/leave-requests/<int:leave_id>/', views.api_leave_request_cancel, name='api_leave_request_cancel'),
    
    # Schedule API endpoints
    path('api/schedule/day/<str:date_str>/', views.api_schedule_day_detail, name='api_schedule_day_detail'),
]
