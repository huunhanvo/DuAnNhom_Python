from django.shortcuts import render, get_object_or_404
from barbershop.models import NguoiDung, ThongTinNhanVien

def test_avatar(request):
    """Test avatar display"""
    user_id = request.session.get('user_id', 2)  # Default to test user
    user = get_object_or_404(NguoiDung, id=user_id, da_xoa=False)
    
    staff_info = None
    try:
        staff_info = ThongTinNhanVien.objects.get(nguoi_dung=user, da_xoa=False)
    except ThongTinNhanVien.DoesNotExist:
        pass
    
    # Staff context for template
    staff_context = {
        'ho_ten': user.ho_ten,
        'so_dien_thoai': user.so_dien_thoai,
        'email': user.email,
        'anh_dai_dien': user.anh_dai_dien if user.anh_dai_dien else None,
    }
    
    context = {
        'user': user,
        'staff_info': staff_info,
        'staff': staff_context,
    }
    return render(request, 'test_avatar.html', context)