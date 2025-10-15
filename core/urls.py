"""
URL configuration for core app (Dashboard, Settings, Decorators)
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Staff Dashboard
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Admin Settings
    path('admin/settings/', views.admin_settings, name='admin_settings'),
    
    # Settings API endpoints
    path('api/settings/general/', views.admin_settings_api_general, name='admin_settings_api_general'),
    path('api/settings/business-hours/', views.admin_settings_api_business_hours, name='admin_settings_api_business_hours'),
    path('api/settings/services/', views.admin_settings_api_services, name='admin_settings_api_services'),
    path('api/settings/payments/', views.admin_settings_api_payments, name='admin_settings_api_payments'),
    
    # Admin Content
    path('admin/content/', views.admin_content, name='admin_content'),
    
    # ==================== PUBLIC PAGES ====================
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('stylists/', views.stylists, name='stylists'),
    path('stylists/<int:stylist_id>/', views.stylist_detail, name='stylist_detail'),
    path('promotions/', views.promotions, name='promotions'),
    
    # ==================== CUSTOMER DASHBOARD ====================
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/bookings/', views.customer_bookings, name='customer_bookings'),
    path('customer/bookings/<int:booking_id>/', views.customer_booking_detail, name='customer_booking_detail'),
    path('customer/history/', views.customer_history, name='customer_history'),
    path('customer/bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # ==================== REWARDS & PROFILE ====================
    path('customer/rewards/', views.customer_rewards, name='customer_rewards'),
    path('customer/rewards/<int:reward_id>/redeem/', views.redeem_reward, name='redeem_reward'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),
    path('customer/profile/update/', views.update_profile, name='update_profile'),
    path('customer/profile/change-password/', views.change_password, name='change_password'),
    path('customer/favorites/', views.customer_favorite_stylists, name='customer_favorite_stylists'),
    path('customer/favorites/<int:stylist_id>/toggle/', views.toggle_favorite, name='toggle_favorite'),
    
    # ==================== REVIEW SYSTEM ====================
    path('customer/bookings/<int:booking_id>/review/', views.customer_review, name='customer_review'),
]
