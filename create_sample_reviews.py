#!/usr/bin/env python
"""
Script to create sample review data for testing
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from django.utils import timezone
from barbershop.models import DanhGia, NguoiDung, HoaDon, DichVu

def create_sample_reviews():
    print("Tạo dữ liệu đánh giá mẫu...")
    
    # Lấy danh sách khách hàng
    khach_hangs = NguoiDung.objects.filter(vai_tro='khach_hang')[:10]
    if not khach_hangs.exists():
        print("Không tìm thấy khách hàng nào. Tạo khách hàng mẫu...")
        # Tạo một số khách hàng mẫu
        for i in range(5):
            NguoiDung.objects.create(
                ho_ten=f'Khách hàng {i+1}',
                email=f'customer{i+1}@example.com',
                so_dien_thoai=f'0123456{i+1:03d}',
                mat_khau_hash='pbkdf2_sha256$600000$dummy$hash',  # dummy password hash
                vai_tro='khach_hang'
            )
        khach_hangs = NguoiDung.objects.filter(vai_tro='khach_hang')[:5]
    
    # Lấy danh sách hóa đơn
    hoa_dons = HoaDon.objects.all()[:20]
    
    # Lấy danh sách dịch vụ  
    dich_vus = DichVu.objects.all()
    
    # Lấy danh sách nhân viên
    nhan_viens = NguoiDung.objects.filter(vai_tro__in=['nhan_vien', 'quan_ly'])
    
    # Nội dung đánh giá mẫu
    review_contents = [
        "Dịch vụ rất tốt, nhân viên thân thiện và chuyên nghiệp!",
        "Cắt tóc đẹp, giá cả hợp lý. Tôi sẽ quay lại!",
        "Không gian sạch sẽ, thoáng mát. Rất hài lòng với kết quả.",
        "Nhân viên có tay nghề cao, tư vấn tận tình.",
        "Thời gian chờ hơi lâu nhưng kết quả đáng giá.",
        "Dịch vụ ok, có thể cải thiện thêm về thái độ phục vụ.",
        "Rất tốt! Đúng như mong đợi, sẽ giới thiệu bạn bè.",
        "Giá hơi cao so với chất lượng, nhưng nhìn chung ok.",
        "Cắt tóc đẹp, gội đầu massage rất thư giãn.",
        "Lần đầu đến, được tư vấn kỹ càng. Sẽ quay lại!"
    ]
    
    # Tạo đánh giá mẫu
    created_count = 0
    for i in range(30):  # Tạo 30 đánh giá mẫu
        try:
            khach_hang = random.choice(khach_hangs)
            so_sao = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 15, 35, 35])[0]  # Bias towards higher ratings
            noi_dung = random.choice(review_contents)
            
            # Random date trong 3 tháng gần đây
            ngay_tao = timezone.now() - timedelta(days=random.randint(0, 90))
            
            # Chọn ngẫu nhiên nhân viên và hóa đơn, dịch vụ
            if not hoa_dons.exists() or not dich_vus.exists() or not nhan_viens.exists():
                print(f"Bỏ qua đánh giá {i+1}: thiếu dữ liệu cần thiết")
                continue
                
            # Tạo đánh giá
            review = DanhGia.objects.create(
                khach_hang=khach_hang,
                hoa_don=random.choice(hoa_dons),
                dich_vu=random.choice(dich_vus),
                nhan_vien=random.choice(nhan_viens),
                so_sao=so_sao,
                noi_dung=noi_dung,
                ngay_tao=ngay_tao
            )
            
            # Random thêm phản hồi cho một số đánh giá
            if random.random() < 0.3 and nhan_viens.exists():  # 30% chance có phản hồi
                phan_hoi_contents = [
                    "Cảm ơn bạn đã đánh giá! Chúng tôi rất vui khi được phục vụ bạn.",
                    "Cảm ơn phản hồi tích cực! Hẹn gặp lại bạn lần sau.",
                    "Chúng tôi sẽ cải thiện để phục vụ bạn tốt hơn. Cảm ơn!",
                    "Rất vui khi bạn hài lòng với dịch vụ của chúng tôi!",
                    "Cảm ơn bạn đã tin tưởng và sử dụng dịch vụ!"
                ]
                
                review.phan_hoi = random.choice(phan_hoi_contents)
                review.nguoi_phan_hoi = random.choice(nhan_viens)
                review.ngay_phan_hoi = ngay_tao + timedelta(days=random.randint(1, 5))
                review.save()
            
            created_count += 1
            print(f"Tạo đánh giá {created_count}: {so_sao} sao - {khach_hang.ho_ten}")
            
        except Exception as e:
            print(f"Lỗi tạo đánh giá {i+1}: {e}")
            continue
    
    print(f"\nĐã tạo thành công {created_count} đánh giá mẫu!")
    
    # Hiển thị thống kê
    total_reviews = DanhGia.objects.count()
    avg_rating = DanhGia.objects.aggregate(
        avg_rating=django.db.models.Avg('so_sao')
    )['avg_rating'] or 0
    
    print(f"Tổng số đánh giá trong hệ thống: {total_reviews}")
    print(f"Điểm đánh giá trung bình: {avg_rating:.2f}/5")
    
    # Thống kê theo sao
    for star in range(1, 6):
        count = DanhGia.objects.filter(so_sao=star).count()
        print(f"Đánh giá {star} sao: {count}")

if __name__ == '__main__':
    create_sample_reviews()