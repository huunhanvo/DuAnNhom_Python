"""
URL configuration for accounts app (Staff, Customers, Profile)
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Admin Staff
    path('admin/staff/', views.admin_staff, name='admin_staff'),
    path('admin/staff/<int:staff_id>/', views.admin_staff_detail, name='admin_staff_detail'),
    path('admin/staff/edit/<int:staff_id>/', views.admin_staff_edit, name='admin_staff_edit'),
    
    # Admin Customers
    path('admin/customers/', views.admin_customers, name='admin_customers'),
    
    # API Customer
    path('api/customers/<int:customer_id>/', views.api_customer_detail, name='api_customer_detail'),
    path('api/customers/<int:customer_id>/detail/', views.api_customer_detail_staff, name='api_customer_detail_staff'),
    
    # Staff Profile
    path('staff/profile/', views.staff_profile, name='staff_profile'),
    path('api/staff/update-profile/', views.api_staff_update_profile, name='api_staff_update_profile'),
    path('api/staff/change-password/', views.api_staff_change_password, name='api_staff_change_password'),
    path('api/staff/upload-avatar/', views.api_staff_upload_avatar, name='api_staff_upload_avatar'),
    path('api/staff/update-notifications/', views.api_staff_update_notifications, name='api_staff_update_notifications'),
    
    # Staff My Customers
    path('staff/my-customers/', views.staff_my_customers, name='staff_my_customers'),
    path('staff/my-customers/export/', views.staff_customers_export, name='staff_customers_export'),
    
    # ==================== CUSTOMER AUTHENTICATION ====================
    path('accounts/register/', views.register, name='register'),
    path('accounts/register-success/', views.register_success, name='register_success'),
    path('accounts/login/', views.customer_login, name='customer_login'),
    path('accounts/logout/', views.customer_logout, name='customer_logout'),
    path('accounts/forgot-password/', views.forgot_password, name='forgot_password'),
    path('accounts/verify-otp/', views.verify_otp, name='verify_otp'),
    path('accounts/reset-password/', views.reset_password, name='reset_password'),
    path('accounts/send-otp/', views.send_otp, name='send_otp'),
]
