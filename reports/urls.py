"""
URL configuration for reports app (Analytics, Exports - Excel/PDF)
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Admin Reports
    path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('admin/reports/export/excel/', views.admin_reports_export_excel, name='admin_reports_export_excel'),
    path('admin/reports/export/pdf/', views.admin_reports_export_pdf, name='admin_reports_export_pdf'),
    
    # Admin POS Report
    path('admin/pos-report/', views.admin_pos_report, name='admin_pos_report'),
    
]
