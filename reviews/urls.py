"""
URL configuration for reviews app (Reviews, Loyalty program)
"""
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Admin Reviews
    path('admin/reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin/reviews/export/', views.admin_reviews_export, name='admin_reviews_export'),
    path('api/reviews/<int:review_id>/', views.admin_review_detail, name='admin_review_detail'),
    path('api/reviews/<int:review_id>/reply/', views.admin_review_reply, name='admin_review_reply'),
    path('api/reviews/<int:review_id>/delete/', views.admin_review_delete, name='admin_review_delete'),
    
    # Admin Loyalty
    path('admin/loyalty/', views.admin_loyalty, name='admin_loyalty'),
]
