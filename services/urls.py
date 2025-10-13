"""
URL configuration for services app (Services, Promotions, Vouchers)
"""
from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Admin Services
    path('admin/services/', views.admin_services, name='admin_services'),
    
    # Services API URLs
    path('api/services/', views.api_service_crud, name='api_services_create'),
    path('api/services/<int:service_id>/', views.api_service_crud, name='api_services_detail'),
    path('api/services/<int:service_id>/toggle-status/', views.api_service_toggle_status, name='api_service_toggle_status'),
    path('api/services/update-order/', views.api_service_update_order, name='api_service_update_order'),
    
    # Admin Promotions
    path('admin/promotions/', views.admin_promotions, name='admin_promotions'),
    path('admin/promotions/stats/<int:voucher_id>/', views.admin_promotion_stats, name='admin_promotion_stats'),
    path('admin/promotions/delete/<int:voucher_id>/', views.admin_delete_promotion, name='admin_delete_promotion'),
    path('admin/promotions/export/', views.admin_export_promotions, name='admin_promotions_export'),
    
    # Test Promotions
    path('test/promotions/', views.test_promotions, name='test_promotions'),
    
]
