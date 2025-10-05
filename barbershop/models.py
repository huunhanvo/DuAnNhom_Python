"""
Django Models cho Hệ thống Quản lý Barbershop
Tương ứng với PostgreSQL database: quan_ly_barbershop
"""

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


# =============================================
# 1. NGƯỜI DÙNG
# =============================================
class NguoiDung(models.Model):
    VAI_TRO_CHOICES = [
        ('khach_hang', 'Khách hàng'),
        ('nhan_vien', 'Nhân viên'),
        ('quan_ly', 'Quản lý'),
    ]
    
    GIOI_TINH_CHOICES = [
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác'),
    ]
    
    ho_ten = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    mat_khau_hash = models.CharField(max_length=255)
    vai_tro = models.CharField(max_length=20, choices=VAI_TRO_CHOICES)
    ngay_sinh = models.DateField(null=True, blank=True)
    gioi_tinh = models.CharField(max_length=10, choices=GIOI_TINH_CHOICES, null=True, blank=True)
    dia_chi = models.TextField(null=True, blank=True)
    anh_dai_dien = models.CharField(max_length=255, null=True, blank=True)
    diem_tich_luy = models.IntegerField(default=0)
    trang_thai = models.BooleanField(default=True)
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'nguoi_dung'
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'
    
    def __str__(self):
        return f"{self.ho_ten} ({self.get_vai_tro_display()})"
    
    def set_password(self, raw_password):
        self.mat_khau_hash = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.mat_khau_hash)


# =============================================
# 2. THÔNG TIN NHÂN VIÊN
# =============================================
class ThongTinNhanVien(models.Model):
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, related_name='thong_tin_nhan_vien')
    cccd = models.CharField(max_length=12, null=True, blank=True, verbose_name='CCCD/CMND')
    mo_ta = models.TextField(null=True, blank=True)
    chuyen_mon = models.TextField(null=True, blank=True)
    kinh_nghiem_nam = models.IntegerField(null=True, blank=True)
    chung_chi = models.TextField(null=True, blank=True)  # Store as JSON string or comma-separated
    danh_gia_trung_binh = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    tong_luot_phuc_vu = models.IntegerField(default=0)
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'thong_tin_nhan_vien'
        verbose_name = 'Thông tin nhân viên'
        verbose_name_plural = 'Thông tin nhân viên'
    
    def __str__(self):
        return f"Thông tin NV: {self.nguoi_dung.ho_ten}"


# =============================================
# 3. DANH MỤC DỊCH VỤ
# =============================================
class DanhMucDichVu(models.Model):
    ten_danh_muc = models.CharField(max_length=100)
    mo_ta = models.TextField(null=True, blank=True)
    thu_tu = models.IntegerField(default=0)
    trang_thai = models.BooleanField(default=True)
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'danh_muc_dich_vu'
        verbose_name = 'Danh mục dịch vụ'
        verbose_name_plural = 'Danh mục dịch vụ'
        ordering = ['thu_tu', 'ten_danh_muc']
    
    def __str__(self):
        return self.ten_danh_muc


# =============================================
# 4. DỊCH VỤ
# =============================================
class DichVu(models.Model):
    danh_muc = models.ForeignKey(DanhMucDichVu, on_delete=models.SET_NULL, null=True, related_name='dich_vu')
    ten_dich_vu = models.CharField(max_length=100)
    mo_ta_ngan = models.TextField(null=True, blank=True)
    mo_ta_chi_tiet = models.TextField(null=True, blank=True)
    gia = models.DecimalField(max_digits=10, decimal_places=2)
    thoi_gian_thuc_hien = models.IntegerField(help_text='Thời gian tính bằng phút')
    anh_minh_hoa = models.CharField(max_length=255, null=True, blank=True)
    thu_tu = models.IntegerField(default=0)
    trang_thai = models.BooleanField(default=True)
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'dich_vu'
        verbose_name = 'Dịch vụ'
        verbose_name_plural = 'Dịch vụ'
        ordering = ['thu_tu', 'ten_dich_vu']
    
    def __str__(self):
        return f"{self.ten_dich_vu} - {self.gia}đ"


# =============================================
# 5. LỊCH LÀM VIỆC
# =============================================
class LichLamViec(models.Model):
    CA_LAM_CHOICES = [
        ('sang', 'Sáng'),
        ('chieu', 'Chiều'),
        ('toi', 'Tối'),
    ]
    
    TRANG_THAI_CHOICES = [
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối'),
    ]
    
    nhan_vien = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='lich_lam_viec')
    ngay_lam = models.DateField()
    ca_lam = models.CharField(max_length=20, choices=CA_LAM_CHOICES)
    gio_bat_dau = models.TimeField()
    gio_ket_thuc = models.TimeField()
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='da_duyet')
    ghi_chu = models.TextField(null=True, blank=True)
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'lich_lam_viec'
        verbose_name = 'Lịch làm việc'
        verbose_name_plural = 'Lịch làm việc'
        unique_together = ['nhan_vien', 'ngay_lam', 'ca_lam']
        ordering = ['ngay_lam', 'gio_bat_dau']
    
    def __str__(self):
        return f"{self.nhan_vien.ho_ten} - {self.ngay_lam} ({self.get_ca_lam_display()})"


# =============================================
# 6. YÊU CẦU NGHỈ PHÉP
# =============================================
class YeuCauNghiPhep(models.Model):
    TRANG_THAI_CHOICES = [
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối'),
    ]
    
    nhan_vien = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='yeu_cau_nghi_phep')
    ngay_bat_dau = models.DateField()
    ngay_ket_thuc = models.DateField()
    ly_do = models.TextField(null=True, blank=True)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='cho_duyet')
    nguoi_duyet = models.ForeignKey(NguoiDung, on_delete=models.SET_NULL, null=True, blank=True, related_name='yeu_cau_duyet')
    ghi_chu_duyet = models.TextField(null=True, blank=True)
    ngay_duyet = models.DateTimeField(null=True, blank=True)
    ngay_tao = models.DateTimeField(default=timezone.now)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'yeu_cau_nghi_phep'
        verbose_name = 'Yêu cầu nghỉ phép'
        verbose_name_plural = 'Yêu cầu nghỉ phép'
        ordering = ['-ngay_tao']
    
    def __str__(self):
        return f"{self.nhan_vien.ho_ten} - {self.ngay_bat_dau} đến {self.ngay_ket_thuc}"


# =============================================
# 7. ĐẶT LỊCH (BOOKING)
# =============================================
class DatLich(models.Model):
    LOAI_DAT_LICH_CHOICES = [
        ('online', 'Online'),
        ('walk_in', 'Walk-in'),
    ]
    
    TRANG_THAI_CHOICES = [
        ('cho_xac_nhan', 'Chờ xác nhận'),
        ('da_xac_nhan', 'Đã xác nhận'),
        ('da_checkin', 'Đã check-in'),
        ('hoan_thanh', 'Hoàn thành'),
        ('da_huy', 'Đã hủy'),
        ('khong_den', 'Không đến'),
    ]
    
    ma_dat_lich = models.CharField(max_length=20, unique=True)
    khach_hang = models.ForeignKey(NguoiDung, on_delete=models.SET_NULL, null=True, blank=True, related_name='dat_lich')
    ten_khach_hang = models.CharField(max_length=100, null=True, blank=True)
    so_dien_thoai_khach = models.CharField(max_length=15)
    email_khach = models.EmailField(max_length=100, null=True, blank=True)
    nhan_vien = models.ForeignKey(NguoiDung, on_delete=models.SET_NULL, null=True, related_name='dat_lich_nhan_vien')
    ngay_hen = models.DateField()
    gio_hen = models.TimeField()
    loai_dat_lich = models.CharField(max_length=20, choices=LOAI_DAT_LICH_CHOICES, default='online')
    tong_tien = models.DecimalField(max_digits=10, decimal_places=2)
    tien_giam_gia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    thanh_tien = models.DecimalField(max_digits=10, decimal_places=2)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='da_xac_nhan')
    ghi_chu = models.TextField(null=True, blank=True)
    ly_do_huy = models.TextField(null=True, blank=True)
    ngay_check_in = models.DateTimeField(null=True, blank=True)
    ngay_hoan_thanh = models.DateTimeField(null=True, blank=True)
    ngay_huy = models.DateTimeField(null=True, blank=True)
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'dat_lich'
        verbose_name = 'Đặt lịch'
        verbose_name_plural = 'Đặt lịch'
        ordering = ['-ngay_hen', '-gio_hen']
    
    def __str__(self):
        return f"{self.ma_dat_lich} - {self.ten_khach_hang or self.khach_hang}"


# =============================================
# 8. DỊCH VỤ TRONG ĐẶT LỊCH
# =============================================
class DichVuDatLich(models.Model):
    dat_lich = models.ForeignKey(DatLich, on_delete=models.CASCADE, related_name='dich_vu_dat_lich')
    dich_vu = models.ForeignKey(DichVu, on_delete=models.SET_NULL, null=True)
    ten_dich_vu = models.CharField(max_length=100)
    gia = models.DecimalField(max_digits=10, decimal_places=2)
    so_luong = models.IntegerField(default=1)
    thanh_tien = models.DecimalField(max_digits=10, decimal_places=2)
    ngay_tao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'dich_vu_dat_lich'
        verbose_name = 'Dịch vụ đặt lịch'
        verbose_name_plural = 'Dịch vụ đặt lịch'
    
    def __str__(self):
        return f"{self.dat_lich.ma_dat_lich} - {self.ten_dich_vu}"


# =============================================
# 9. HÓA ĐƠN
# =============================================
class HoaDon(models.Model):
    PHUONG_THUC_CHOICES = [
        ('tien_mat', 'Tiền mặt'),
        ('chuyen_khoan', 'Chuyển khoản'),
        ('vi_dien_tu', 'Ví điện tử'),
        ('the', 'Thẻ'),
    ]
    
    ma_hoa_don = models.CharField(max_length=20, unique=True)
    dat_lich = models.ForeignKey(DatLich, on_delete=models.SET_NULL, null=True, blank=True, related_name='hoa_don')
    khach_hang = models.ForeignKey(NguoiDung, on_delete=models.SET_NULL, null=True, blank=True, related_name='hoa_don')
    ten_khach_hang = models.CharField(max_length=100)
    so_dien_thoai_khach = models.CharField(max_length=15)
    nhan_vien = models.ForeignKey(NguoiDung, on_delete=models.PROTECT, related_name='hoa_don_nhan_vien')
    tam_tinh = models.DecimalField(max_digits=10, decimal_places=2)
    tien_giam_gia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    thanh_tien = models.DecimalField(max_digits=10, decimal_places=2)
    phuong_thuc_thanh_toan = models.CharField(max_length=30, choices=PHUONG_THUC_CHOICES)
    tien_khach_dua = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tien_thua = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nguoi_tao = models.ForeignKey(NguoiDung, on_delete=models.PROTECT, related_name='hoa_don_tao')
    ngay_thanh_toan = models.DateTimeField(default=timezone.now)
    ghi_chu = models.TextField(null=True, blank=True)
    ngay_tao = models.DateTimeField(default=timezone.now)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'hoa_don'
        verbose_name = 'Hóa đơn'
        verbose_name_plural = 'Hóa đơn'
        ordering = ['-ngay_thanh_toan']
    
    def __str__(self):
        return f"{self.ma_hoa_don} - {self.thanh_tien}đ"


# =============================================
# 10. CHI TIẾT HÓA ĐƠN
# =============================================
class ChiTietHoaDon(models.Model):
    hoa_don = models.ForeignKey(HoaDon, on_delete=models.CASCADE, related_name='chi_tiet')
    dich_vu = models.ForeignKey(DichVu, on_delete=models.SET_NULL, null=True)
    ten_dich_vu = models.CharField(max_length=100)
    gia = models.DecimalField(max_digits=10, decimal_places=2)
    so_luong = models.IntegerField(default=1)
    thanh_tien = models.DecimalField(max_digits=10, decimal_places=2)
    ngay_tao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'chi_tiet_hoa_don'
        verbose_name = 'Chi tiết hóa đơn'
        verbose_name_plural = 'Chi tiết hóa đơn'
    
    def __str__(self):
        return f"{self.hoa_don.ma_hoa_don} - {self.ten_dich_vu}"


# =============================================
# 11. VOUCHER
# =============================================
class Voucher(models.Model):
    LOAI_GIAM_CHOICES = [
        ('phan_tram', 'Phần trăm'),
        ('tien_mat', 'Tiền mặt'),
    ]
    
    AP_DUNG_CHO_CHOICES = [
        ('khach_moi', 'Khách mới'),
        ('khach_cu', 'Khách cũ'),
        ('tat_ca', 'Tất cả'),
    ]
    
    ma_voucher = models.CharField(max_length=50, unique=True)
    ten_voucher = models.CharField(max_length=100)
    mo_ta = models.TextField(null=True, blank=True)
    loai_giam = models.CharField(max_length=20, choices=LOAI_GIAM_CHOICES)
    gia_tri_giam = models.DecimalField(max_digits=10, decimal_places=2)
    gia_tri_don_toi_thieu = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    giam_toi_da = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ngay_bat_dau = models.DateField()
    ngay_ket_thuc = models.DateField()
    so_luong_tong = models.IntegerField(null=True, blank=True)
    so_luong_da_dung = models.IntegerField(default=0)
    gioi_han_moi_khach = models.IntegerField(default=1)
    ap_dung_cho = models.CharField(max_length=20, choices=AP_DUNG_CHO_CHOICES, default='tat_ca')
    hien_thi_cong_khai = models.BooleanField(default=True)
    trang_thai = models.BooleanField(default=True)
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'voucher'
        verbose_name = 'Voucher'
        verbose_name_plural = 'Voucher'
        ordering = ['-ngay_tao']
    
    def __str__(self):
        return f"{self.ma_voucher} - {self.ten_voucher}"


# =============================================
# 12. CÀI ĐẶT HỆ THỐNG
# =============================================
class CaiDatHeThong(models.Model):
    # Thông tin chung
    ten_tiem = models.CharField(max_length=200, default='Barbershop HotTocNam')
    hotline = models.CharField(max_length=20, null=True, blank=True)
    dia_chi = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    logo = models.CharField(max_length=255, null=True, blank=True)
    mo_ta = models.TextField(null=True, blank=True)
    
    # Giờ làm việc
    gio_mo_cua = models.TimeField(default='08:00')
    gio_dong_cua = models.TimeField(default='21:00')
    ngay_lam_viec = models.JSONField(default=dict)  # {'monday': True, 'tuesday': True, ...}
    thoi_gian_slot = models.IntegerField(default=30)  # phút
    
    # Cài đặt dịch vụ
    tu_dong_xac_nhan = models.BooleanField(default=True)
    cho_phep_chon_nhan_vien = models.BooleanField(default=True)
    yeu_cau_dat_coc = models.BooleanField(default=False)
    so_tien_dat_coc = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    loai_dat_coc = models.CharField(max_length=10, choices=[('VND', 'VNĐ'), ('%', '%')], default='VND')
    
    # Cài đặt đặt lịch
    thoi_gian_dat_truoc_toi_thieu = models.IntegerField(default=60)  # phút
    thoi_gian_dat_truoc_toi_da = models.IntegerField(default=43200)  # phút (30 ngày)
    thoi_gian_huy_lich = models.IntegerField(default=60)  # phút
    gui_nhac_nho = models.BooleanField(default=True)
    
    # Thanh toán
    thanh_toan_tien_mat = models.BooleanField(default=True)
    thanh_toan_the = models.BooleanField(default=True)
    thanh_toan_chuyen_khoan = models.BooleanField(default=True)
    so_tai_khoan = models.CharField(max_length=50, null=True, blank=True)
    ten_ngan_hang = models.CharField(max_length=100, null=True, blank=True)
    thanh_toan_momo = models.BooleanField(default=False)
    so_dien_thoai_momo = models.CharField(max_length=15, null=True, blank=True)
    thanh_toan_vnpay = models.BooleanField(default=False)
    vnpay_api_key = models.CharField(max_length=255, null=True, blank=True)
    
    # Thông báo
    sms_dat_lich_moi = models.BooleanField(default=True)
    sms_nhac_lich_hen = models.BooleanField(default=True)
    sms_huy_lich = models.BooleanField(default=False)
    email_hoa_don = models.BooleanField(default=True)
    email_bao_cao = models.BooleanField(default=False)
    
    # Giao diện
    mau_chu_dao = models.CharField(max_length=7, default='#8b4513')
    mau_phu = models.CharField(max_length=7, default='#d2691e')
    che_do_toi = models.BooleanField(default=False)
    
    # Sao lưu
    tu_dong_sao_luu = models.CharField(
        max_length=20, 
        choices=[
            ('none', 'Không tự động'),
            ('daily', 'Hàng ngày'),
            ('weekly', 'Hàng tuần'),
            ('monthly', 'Hàng tháng')
        ],
        default='weekly'
    )
    lan_sao_luu_cuoi = models.DateTimeField(null=True, blank=True)
    
    # Nâng cao
    che_do_bao_tri = models.BooleanField(default=False)
    debug_mode = models.BooleanField(default=False)
    
    # Metadata
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'cai_dat_he_thong'
        verbose_name = 'Cài đặt hệ thống'
        verbose_name_plural = 'Cài đặt hệ thống'
    
    def __str__(self):
        return self.ten_tiem
    
    @classmethod
    def get_settings(cls):
        """Get or create settings instance"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'ten_tiem': 'Barbershop HotTocNam',
                'ngay_lam_viec': {
                    'monday': True,
                    'tuesday': True, 
                    'wednesday': True,
                    'thursday': True,
                    'friday': True,
                    'saturday': True,
                    'sunday': False
                }
            }
        )
        return settings


# =============================================
# 15. ĐƠN XIN NGHỈ
# =============================================
class DonXinNghi(models.Model):
    TRANG_THAI_CHOICES = [
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối'),
    ]
    
    LOAI_NGHI_CHOICES = [
        ('nghi_phep', 'Nghỉ phép'),
        ('nghi_om', 'Nghỉ ốm'),
        ('nghi_co_phep', 'Nghỉ có phép'),
        ('nghi_khong_phep', 'Nghỉ không phép'),
    ]
    
    nhan_vien = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='don_xin_nghi')
    tu_ngay = models.DateField()
    den_ngay = models.DateField()
    loai_nghi = models.CharField(max_length=20, choices=LOAI_NGHI_CHOICES, default='nghi_phep')
    ly_do = models.TextField()
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='cho_duyet')
    nguoi_duyet = models.ForeignKey(NguoiDung, on_delete=models.SET_NULL, null=True, blank=True, related_name='don_duyet')
    ly_do_tu_choi = models.TextField(null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'don_xin_nghi'
        verbose_name = 'Đơn xin nghỉ'
        verbose_name_plural = 'Đơn xin nghỉ'
        ordering = ['-ngay_tao']
    
    def __str__(self):
        return f"{self.nhan_vien.ho_ten} - {self.tu_ngay} đến {self.den_ngay}"
    
    @property
    def so_ngay_nghi(self):
        return (self.den_ngay - self.tu_ngay).days + 1

class DanhGia(models.Model):
    """Model cho đánh giá của khách hàng"""
    khach_hang = models.ForeignKey(
        NguoiDung, 
        on_delete=models.CASCADE, 
        related_name='danh_gia_khach_hang',
        limit_choices_to={'vai_tro': 'khach_hang'}
    )
    hoa_don = models.ForeignKey(
        'HoaDon', 
        on_delete=models.CASCADE, 
        related_name='danh_gia_hoa_don'
    )
    dich_vu = models.ForeignKey(
        DichVu, 
        on_delete=models.CASCADE, 
        related_name='danh_gia_dich_vu'
    )
    nhan_vien = models.ForeignKey(
        NguoiDung, 
        on_delete=models.CASCADE, 
        related_name='danh_gia_nhan_vien',
        limit_choices_to={'vai_tro': 'nhan_vien'}
    )
    so_sao = models.IntegerField(
        choices=[(i, f"{i} sao") for i in range(1, 6)],
        help_text="Đánh giá từ 1-5 sao"
    )
    noi_dung = models.TextField(
        help_text="Nội dung đánh giá của khách hàng"
    )
    hinh_anh = models.ImageField(
        upload_to='reviews/',
        null=True,
        blank=True,
        help_text="Hình ảnh đính kèm (tùy chọn)"
    )
    phan_hoi = models.TextField(
        null=True,
        blank=True,
        help_text="Phản hồi từ quản lý"
    )
    nguoi_phan_hoi = models.ForeignKey(
        NguoiDung,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='phan_hoi_danh_gia',
        limit_choices_to={'vai_tro': 'quan_ly'}
    )
    ngay_phan_hoi = models.DateTimeField(
        null=True,
        blank=True
    )
    da_duyet = models.BooleanField(
        default=True,
        help_text="Đánh giá đã được duyệt hiển thị"
    )
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    da_xoa = models.BooleanField(default=False)
    ngay_xoa = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'danh_gia'
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Đánh giá'
        ordering = ['-ngay_tao']
        unique_together = ['khach_hang', 'hoa_don', 'dich_vu']
    
    def __str__(self):
        return f"{self.khach_hang.ho_ten} - {self.so_sao} sao - {self.dich_vu.ten_dich_vu}"
    
    @property
    def has_reply(self):
        return bool(self.phan_hoi)
    
    def save(self, *args, **kwargs):
        if self.phan_hoi and not self.ngay_phan_hoi:
            self.ngay_phan_hoi = timezone.now()
        super().save(*args, **kwargs)

# CÁC MODEL KHÁC (Voucher khách hàng, Điểm đổi thưởng, Giao dịch điểm, 
# Ghi chú khách hàng, Lịch sử tóc, Stylist yêu thích, 
# Thông báo, Nội dung website, Combo dịch vụ) 
# Có thể thêm sau nếu cần...
