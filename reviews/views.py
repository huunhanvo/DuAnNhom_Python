"""
Views for reviews app (Reviews, Loyalty program)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum, Q, Avg
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from decimal import Decimal
import json
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# Import decorators from core
from core.decorators import require_auth, require_role

# Import models
from barbershop.models import (
    DanhGia,
    NguoiDung,
    DatLich,
    DichVu,
    HoaDon
)

# ============ VIEWS - Bạn sẽ copy code vào đây ============
# Các views sẽ được di chuyển vào đây:
# - admin_reviews
@require_role(['quan_ly'])
def admin_reviews(request):
    """Review Management with comprehensive features"""
    from django.db.models import Count, Avg, Q
    from django.core.paginator import Paginator
    from datetime import datetime, timedelta
    
    # Get filter parameters
    rating_filter = request.GET.get('rating', 'all')
    status_filter = request.GET.get('status', 'all')
    service_filter = request.GET.get('service', '')
    search = request.GET.get('search', '').strip()
    sort = request.GET.get('sort', '-ngay_tao')
    
    # Base query for reviews
    reviews_query = DanhGia.objects.filter(da_xoa=False).select_related(
        'khach_hang', 'hoa_don', 'dich_vu', 'nhan_vien', 'nguoi_phan_hoi'
    )
    
    # Apply filters
    if rating_filter != 'all' and rating_filter.isdigit():
        reviews_query = reviews_query.filter(so_sao=int(rating_filter))
    
    if status_filter == 'pending':
        reviews_query = reviews_query.filter(phan_hoi__isnull=True)
    elif status_filter == 'replied':
        reviews_query = reviews_query.filter(phan_hoi__isnull=False)
    
    if service_filter and service_filter.isdigit():
        reviews_query = reviews_query.filter(dich_vu_id=service_filter)
    
    if search:
        reviews_query = reviews_query.filter(
            Q(khach_hang__ho_ten__icontains=search) |
            Q(noi_dung__icontains=search) |
            Q(dich_vu__ten_dich_vu__icontains=search) |
            Q(nhan_vien__ho_ten__icontains=search)
        )
    
    # Apply sorting
    reviews_query = reviews_query.order_by(sort)
    
    # Calculate statistics
    total_reviews = DanhGia.objects.filter(da_xoa=False).count()
    avg_rating = DanhGia.objects.filter(da_xoa=False).aggregate(
        avg=Avg('so_sao')
    )['avg'] or 0
    
    pending_replies = DanhGia.objects.filter(
        da_xoa=False, 
        phan_hoi__isnull=True
    ).count()
    
    # Calculate satisfaction rate (4-5 stars)
    satisfied = DanhGia.objects.filter(da_xoa=False, so_sao__gte=4).count()
    satisfaction_rate = round((satisfied / total_reviews * 100) if total_reviews > 0 else 0, 1)
    
    # Rating breakdown
    rating_breakdown = []
    for stars in range(5, 0, -1):
        count = DanhGia.objects.filter(da_xoa=False, so_sao=stars).count()
        percent = round((count / total_reviews * 100) if total_reviews > 0 else 0, 1)
        rating_breakdown.append({
            'stars': stars,
            'count': count,
            'percent': percent
        })
    
    # Rating counts for tabs
    star_counts = {}
    for i in range(1, 6):
        star_counts[f'{i}_star_count'] = DanhGia.objects.filter(
            da_xoa=False, so_sao=i
        ).count()
    
    # Trend data for chart - find date range with actual data
    trend_labels = []
    trend_data = []
    trend_counts = []
    
    # Get the date range with reviews (last 30 days or actual review dates)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    reviews_in_period = DanhGia.objects.filter(
        da_xoa=False,
        ngay_tao__date__gte=thirty_days_ago
    ).dates('ngay_tao', 'day').order_by('ngay_tao')
    
    if reviews_in_period:
        # Use actual review dates for more meaningful chart
        review_dates = list(reviews_in_period)[-7:]  # Last 7 dates with reviews
        
        for date in review_dates:
            trend_labels.append(date.strftime('%d/%m'))
            
            daily_reviews = DanhGia.objects.filter(
                da_xoa=False,
                ngay_tao__date=date
            )
            
            daily_avg = daily_reviews.aggregate(avg=Avg('so_sao'))['avg'] or 0
            daily_count = daily_reviews.count()
            
            trend_data.append(round(daily_avg, 1))
            trend_counts.append(daily_count)
    else:
        # Fallback to last 7 days even if empty
        for i in range(6, -1, -1):
            date = timezone.now().date() - timedelta(days=i)
            trend_labels.append(date.strftime('%d/%m'))
            
            daily_reviews = DanhGia.objects.filter(
                da_xoa=False,
                ngay_tao__date=date
            )
            
            daily_avg = daily_reviews.aggregate(avg=Avg('so_sao'))['avg'] or 0
            daily_count = daily_reviews.count()
            
            trend_data.append(round(daily_avg, 1))
            trend_counts.append(daily_count)
    
    # Pagination
    paginator = Paginator(reviews_query, 10)
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    
    # Get all services for filter
    services = DichVu.objects.filter(da_xoa=False).order_by('ten_dich_vu')
    
    # Convert data to JSON format for Chart.js
    import json
    
    context = {
        'reviews': reviews,
        'services': services,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 1),
        'pending_replies': pending_replies,
        'satisfaction_rate': satisfaction_rate,
        'rating_breakdown': rating_breakdown,
        'trend_labels': json.dumps(trend_labels),
        'trend_data': json.dumps(trend_data),
        'trend_counts': json.dumps(trend_counts),
        'current_filters': {
            'rating': rating_filter,
            'status': status_filter,
            'service': service_filter,
            'search': search,
            'sort': sort
        },
        **star_counts
    }
    
    return render(request, 'admin/reviews.html', context)
# - admin_loyalty
@require_role(['quan_ly'])
def admin_loyalty(request):
    """Loyalty Program"""
    from django.db.models import Sum, Count, Avg
    
    # Get top customers based on points and spending
    top_customers = []
    customers = NguoiDung.objects.filter(
        vai_tro='khach_hang',
        da_xoa=False
    ).annotate(
        total_spent=Sum('hoadon__tong_tien'),
        total_visits=Count('hoadon', distinct=True),
        avg_rating=Avg('danh_gia_khach_hang__so_sao')
    ).order_by('-diem_tich_luy')[:10]
    
    for customer in customers:
        # Calculate tier based on spending
        total_spent = customer.total_spent or 0
        if total_spent >= 10000000:  # 10M+
            tier_name = "VIP Platinum"
            tier_color = "#E5E4E2"
            tier_bg = "linear-gradient(135deg, #E5E4E2, #BCC6CC)"
            tier_icon = "ð"
            next_tier = "Max Level"
            points_to_next = 0
        elif total_spent >= 5000000:  # 5M+
            tier_name = "VIP Gold"
            tier_color = "#FFD700"
            tier_bg = "linear-gradient(135deg, #FFD700, #FFA500)"
            tier_icon = "â­"
            next_tier = "VIP Platinum"
            points_to_next = 10000000 - total_spent
        elif total_spent >= 2000000:  # 2M+
            tier_name = "VIP Silver"
            tier_color = "#C0C0C0"
            tier_bg = "linear-gradient(135deg, #C0C0C0, #A9A9A9)"
            tier_icon = "ð¥"
            next_tier = "VIP Gold"
            points_to_next = 5000000 - total_spent
        else:
            tier_name = "ThÃ nh viÃªn"
            tier_color = "#6c757d"
            tier_bg = "linear-gradient(135deg, #6c757d, #5a6268)"
            tier_icon = "ð¤"
            next_tier = "VIP Silver"
            points_to_next = 2000000 - total_spent
        
        next_tier_progress = min(100, (total_spent / (total_spent + points_to_next)) * 100) if points_to_next > 0 else 100
        
        top_customers.append({
            'id': customer.id,
            'name': customer.ho_ten,
            'phone': customer.so_dien_thoai,
            'avatar': customer.anh_dai_dien,
            'points': customer.diem_tich_luy,
            'total_spent': total_spent,
            'total_visits': customer.total_visits or 0,
            'avg_rating': round(customer.avg_rating or 0, 1),
            'last_visit': customer.ngay_cap_nhat.strftime('%d/%m'),
            'tier_name': tier_name,
            'tier_color': tier_color,
            'tier_bg': tier_bg,
            'tier_icon': tier_icon,
            'next_tier': next_tier,
            'points_to_next_tier': points_to_next,
            'next_tier_progress': next_tier_progress
        })
    
    context = {
        'loyalty_tiers': [],
        'top_customers': top_customers,
        'total_loyalty_members': NguoiDung.objects.filter(vai_tro='khach_hang', da_xoa=False).count(),
        'total_points_issued': NguoiDung.objects.filter(vai_tro='khach_hang', da_xoa=False).aggregate(
            total=Sum('diem_tich_luy'))['total'] or 0,
    }
    return render(request, 'admin/loyalty.html', context)
# - admin_review_reply
@require_role(['quan_ly'])
def admin_review_reply(request, review_id):
    """API endpoint for replying to reviews"""
    if request.method == 'POST':
        try:
            review = get_object_or_404(DanhGia, id=review_id, da_xoa=False)
            reply_content = request.POST.get('phan_hoi', '').strip()
            
            if not reply_content:
                return JsonResponse({'success': False, 'message': 'Ná»i dung pháº£n há»i khÃ´ng ÄÆ°á»£c Äá» trá»ng'})
            
            # Get NguoiDung from session
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    nguoi_dung = NguoiDung.objects.get(id=user_id)
                    review.nguoi_phan_hoi = nguoi_dung
                except NguoiDung.DoesNotExist:
                    pass
                    
            review.phan_hoi = reply_content
            review.ngay_phan_hoi = timezone.now()
            review.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'ÄÃ£ gá»­i pháº£n há»i thÃ nh cÃ´ng!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

# - admin_review_detail
@require_role(['quan_ly'])
def admin_review_detail(request, review_id):
    """API endpoint for getting review details"""
    try:
        review = get_object_or_404(DanhGia, id=review_id, da_xoa=False)
        
        data = {
            'id': review.id,
            'khach_hang': review.khach_hang.ho_ten,
            'so_sao': review.so_sao,
            'noi_dung': review.noi_dung,
            'phan_hoi': review.phan_hoi,
            'ngay_tao': review.ngay_tao.strftime('%d/%m/%Y %H:%M'),
            'dich_vu': review.dich_vu.ten_dich_vu,
            'nhan_vien': review.nhan_vien.ho_ten,
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
# - admin_review_delete
@require_role(['quan_ly'])
def admin_review_delete(request, review_id):
    """API endpoint for deleting reviews (soft delete)"""
    if request.method == 'DELETE':
        try:
            review = get_object_or_404(DanhGia, id=review_id, da_xoa=False)
            review.da_xoa = True
            review.ngay_xoa = timezone.now()
            review.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'ÄÃ£ xÃ³a ÄÃ¡nh giÃ¡ thÃ nh cÃ´ng!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'CÃ³ lá»i xáº£y ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
# - admin_reviews_export
@require_role(['quan_ly'])
def admin_reviews_export(request):
    """Export reviews to CSV"""
    import csv
    from django.http import HttpResponse
    
    reviews = DanhGia.objects.filter(da_xoa=False).select_related(
        'khach_hang', 'dich_vu', 'nhan_vien'
    ).order_by('-ngay_tao')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="danh_gia_khach_hang.csv"'
    response.write('\ufeff')  # UTF-8 BOM for Excel
    
    writer = csv.writer(response)
    writer.writerow([
        'NgÃ y táº¡o', 'KhÃ¡ch hÃ ng', 'Äiá»n thoáº¡i', 'Dá»ch vá»¥', 'NhÃ¢n viÃªn', 
        'Sá» sao', 'Ná»i dung', 'Pháº£n há»i', 'NgÃ y pháº£n há»i'
    ])
    
    for review in reviews:
        writer.writerow([
            review.ngay_tao.strftime('%d/%m/%Y %H:%M'),
            review.khach_hang.ho_ten,
            review.khach_hang.so_dien_thoai,
            review.dich_vu.ten_dich_vu,
            review.nhan_vien.ho_ten,
            review.so_sao,
            review.noi_dung,
            review.phan_hoi or '',
            review.ngay_phan_hoi.strftime('%d/%m/%Y %H:%M') if review.ngay_phan_hoi else ''
        ])
    
    return response

