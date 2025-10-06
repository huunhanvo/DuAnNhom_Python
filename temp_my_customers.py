@require_role(['nhan_vien', 'quan_ly'])
def staff_my_customers(request):
    """My Customers - Simple version"""
    user_id = request.session.get('user_id')
    
    # Get customers who booked with this staff
    customer_bookings = DatLich.objects.filter(
        nhan_vien_id=user_id,
        da_xoa=False
    ).exclude(trang_thai='da_huy')
    
    customer_ids = customer_bookings.values_list('khach_hang_id', flat=True).distinct()
    
    customers_list = []
    for customer_id in customer_ids:
        try:
            customer = NguoiDung.objects.get(id=customer_id, da_xoa=False)
            
            # Add basic attributes
            customer.visit_count = 0
            customer.total_revenue = 0
            customer.last_visit = None
            customer.loyalty_score = 50
            customer.hang_thanh_vien = 'bronze'
            customer.recent_visits = []
            customer.preferences = []
            
            customers_list.append(customer)
        except:
            continue
    
    context = {
        'customers': customers_list,
        'total_customers': len(customers_list),
        'regular_customers': 0,
        'this_month_customers': 0,
        'avg_rating': 0,
        'search_query': '',
        'sort_by': '',
        'tier_filter': '',
        'loyalty_filter': '',
    }
    return render(request, 'staff/my-customers.html', context)