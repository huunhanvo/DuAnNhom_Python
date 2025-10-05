-- =============================================
-- HỆ THỐNG QUẢN LÝ BARBERSHOP
-- Database: PostgreSQL
-- Sử dụng: Soft Delete (cot da_xoa)
-- -- =============================================

-- -- Xóa database nếu tồn tại và tạo mới
-- DROP DATABASE IF EXISTS quan_ly_barbershop;
-- CREATE DATABASE quan_ly_barbershop
--     WITH 
--     ENCODING = 'UTF8';


-- =============================================
-- 1. BẢNG NGƯỜI DÙNG (Users)
-- =============================================
CREATE TABLE nguoi_dung (
    id SERIAL PRIMARY KEY,
    ho_ten VARCHAR(100) NOT NULL,
    so_dien_thoai VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    mat_khau_hash VARCHAR(255) NOT NULL,
    vai_tro VARCHAR(20) NOT NULL CHECK (vai_tro IN ('khach_hang', 'nhan_vien', 'quan_ly')),
    ngay_sinh DATE,
    gioi_tinh VARCHAR(10) CHECK (gioi_tinh IN ('nam', 'nu', 'khac')),
    dia_chi TEXT,
    anh_dai_dien VARCHAR(255),
    diem_tich_luy INTEGER DEFAULT 0,
    trang_thai BOOLEAN DEFAULT TRUE,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 2. BẢNG THÔNG TIN NHÂN VIÊN
-- =============================================
CREATE TABLE thong_tin_nhan_vien (
    id SERIAL PRIMARY KEY,
    nguoi_dung_id INTEGER REFERENCES nguoi_dung(id),
    mo_ta TEXT,
    chuyen_mon TEXT,
    kinh_nghiem_nam INTEGER,
    chung_chi TEXT[],
    danh_gia_trung_binh DECIMAL(2,1) DEFAULT 0.0,
    tong_luot_phuc_vu INTEGER DEFAULT 0,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 3. BẢNG DANH MỤC DỊCH VỤ
-- =============================================
CREATE TABLE danh_muc_dich_vu (
    id SERIAL PRIMARY KEY,
    ten_danh_muc VARCHAR(100) NOT NULL,
    mo_ta TEXT,
    thu_tu INTEGER DEFAULT 0,
    trang_thai BOOLEAN DEFAULT TRUE,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 4. BẢNG DỊCH VỤ
-- =============================================
CREATE TABLE dich_vu (
    id SERIAL PRIMARY KEY,
    danh_muc_id INTEGER REFERENCES danh_muc_dich_vu(id),
    ten_dich_vu VARCHAR(100) NOT NULL,
    mo_ta_ngan TEXT,
    mo_ta_chi_tiet TEXT,
    gia DECIMAL(10,2) NOT NULL,
    thoi_gian_thuc_hien INTEGER NOT NULL, -- phút
    anh_minh_hoa VARCHAR(255),
    thu_tu INTEGER DEFAULT 0,
    trang_thai BOOLEAN DEFAULT TRUE,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 5. BẢNG LỊCH LÀM VIỆC
-- =============================================
CREATE TABLE lich_lam_viec (
    id SERIAL PRIMARY KEY,
    nhan_vien_id INTEGER REFERENCES nguoi_dung(id),
    ngay_lam DATE NOT NULL,
    ca_lam VARCHAR(20) NOT NULL CHECK (ca_lam IN ('sang', 'chieu', 'toi')),
    gio_bat_dau TIME NOT NULL,
    gio_ket_thuc TIME NOT NULL,
    trang_thai VARCHAR(20) DEFAULT 'da_duyet' CHECK (trang_thai IN ('cho_duyet', 'da_duyet', 'tu_choi')),
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP,
    UNIQUE(nhan_vien_id, ngay_lam, ca_lam)
);

-- =============================================
-- 6. BẢNG YÊU CẦU NGHỈ PHÉP
-- =============================================
CREATE TABLE yeu_cau_nghi_phep (
    id SERIAL PRIMARY KEY,
    nhan_vien_id INTEGER REFERENCES nguoi_dung(id),
    ngay_bat_dau DATE NOT NULL,
    ngay_ket_thuc DATE NOT NULL,
    ly_do TEXT,
    trang_thai VARCHAR(20) DEFAULT 'cho_duyet' CHECK (trang_thai IN ('cho_duyet', 'da_duyet', 'tu_choi')),
    nguoi_duyet_id INTEGER REFERENCES nguoi_dung(id),
    ghi_chu_duyet TEXT,
    ngay_duyet TIMESTAMP,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 7. BẢNG ĐẶT LỊCH (BOOKING)
-- =============================================
CREATE TABLE dat_lich (
    id SERIAL PRIMARY KEY,
    ma_dat_lich VARCHAR(20) UNIQUE NOT NULL,
    khach_hang_id INTEGER REFERENCES nguoi_dung(id),
    ten_khach_hang VARCHAR(100),
    so_dien_thoai_khach VARCHAR(15) NOT NULL,
    email_khach VARCHAR(100),
    nhan_vien_id INTEGER REFERENCES nguoi_dung(id),
    ngay_hen DATE NOT NULL,
    gio_hen TIME NOT NULL,
    loai_dat_lich VARCHAR(20) DEFAULT 'online' CHECK (loai_dat_lich IN ('online', 'walk_in')),
    tong_tien DECIMAL(10,2) NOT NULL,
    tien_giam_gia DECIMAL(10,2) DEFAULT 0,
    thanh_tien DECIMAL(10,2) NOT NULL,
    trang_thai VARCHAR(20) DEFAULT 'da_xac_nhan' CHECK (trang_thai IN ('cho_xac_nhan', 'da_xac_nhan', 'da_checkin', 'hoan_thanh', 'da_huy', 'khong_den')),
    ghi_chu TEXT,
    ly_do_huy TEXT,
    ngay_check_in TIMESTAMP,
    ngay_hoan_thanh TIMESTAMP,
    ngay_huy TIMESTAMP,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 8. BẢNG DỊCH VỤ TRONG ĐẶT LỊCH
-- =============================================
CREATE TABLE dich_vu_dat_lich (
    id SERIAL PRIMARY KEY,
    dat_lich_id INTEGER REFERENCES dat_lich(id) ON DELETE CASCADE,
    dich_vu_id INTEGER REFERENCES dich_vu(id),
    ten_dich_vu VARCHAR(100) NOT NULL,
    gia DECIMAL(10,2) NOT NULL,
    so_luong INTEGER DEFAULT 1,
    thanh_tien DECIMAL(10,2) NOT NULL,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 9. BẢNG HÓA ĐƠN (INVOICE - POS)
-- =============================================
CREATE TABLE hoa_don (
    id SERIAL PRIMARY KEY,
    ma_hoa_don VARCHAR(20) UNIQUE NOT NULL,
    dat_lich_id INTEGER REFERENCES dat_lich(id),
    khach_hang_id INTEGER REFERENCES nguoi_dung(id),
    ten_khach_hang VARCHAR(100) NOT NULL,
    so_dien_thoai_khach VARCHAR(15) NOT NULL,
    nhan_vien_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    tam_tinh DECIMAL(10,2) NOT NULL,
    tien_giam_gia DECIMAL(10,2) DEFAULT 0,
    thanh_tien DECIMAL(10,2) NOT NULL,
    phuong_thuc_thanh_toan VARCHAR(30) NOT NULL CHECK (phuong_thuc_thanh_toan IN ('tien_mat', 'chuyen_khoan', 'vi_dien_tu', 'the')),
    tien_khach_dua DECIMAL(10,2),
    tien_thua DECIMAL(10,2),
    nguoi_tao_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    ngay_thanh_toan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 10. BẢNG CHI TIẾT HÓA ĐƠN
-- =============================================
CREATE TABLE chi_tiet_hoa_don (
    id SERIAL PRIMARY KEY,
    hoa_don_id INTEGER REFERENCES hoa_don(id) ON DELETE CASCADE,
    dich_vu_id INTEGER REFERENCES dich_vu(id),
    ten_dich_vu VARCHAR(100) NOT NULL,
    gia DECIMAL(10,2) NOT NULL,
    so_luong INTEGER DEFAULT 1,
    thanh_tien DECIMAL(10,2) NOT NULL,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 11. BẢNG VOUCHER
-- =============================================
CREATE TABLE voucher (
    id SERIAL PRIMARY KEY,
    ma_voucher VARCHAR(50) UNIQUE NOT NULL,
    ten_voucher VARCHAR(100) NOT NULL,
    mo_ta TEXT,
    loai_giam VARCHAR(20) NOT NULL CHECK (loai_giam IN ('phan_tram', 'tien_mat')),
    gia_tri_giam DECIMAL(10,2) NOT NULL,
    gia_tri_don_toi_thieu DECIMAL(10,2) DEFAULT 0,
    giam_toi_da DECIMAL(10,2),
    ngay_bat_dau DATE NOT NULL,
    ngay_ket_thuc DATE NOT NULL,
    so_luong_tong INTEGER,
    so_luong_da_dung INTEGER DEFAULT 0,
    gioi_han_moi_khach INTEGER DEFAULT 1,
    ap_dung_cho VARCHAR(20) DEFAULT 'tat_ca' CHECK (ap_dung_cho IN ('khach_moi', 'khach_cu', 'tat_ca')),
    hien_thi_cong_khai BOOLEAN DEFAULT TRUE,
    trang_thai BOOLEAN DEFAULT TRUE,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 12. BẢNG VOUCHER CỦA KHÁCH HÀNG
-- =============================================
CREATE TABLE voucher_khach_hang (
    id SERIAL PRIMARY KEY,
    voucher_id INTEGER REFERENCES voucher(id),
    khach_hang_id INTEGER REFERENCES nguoi_dung(id),
    ma_voucher_ca_nhan VARCHAR(50) UNIQUE NOT NULL,
    da_su_dung BOOLEAN DEFAULT FALSE,
    dat_lich_id INTEGER REFERENCES dat_lich(id),
    hoa_don_id INTEGER REFERENCES hoa_don(id),
    ngay_su_dung TIMESTAMP,
    ngay_het_han DATE NOT NULL,
    ngay_nhan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 13. BẢNG ĐIỂM ĐỔI THƯỞNG
-- =============================================
CREATE TABLE diem_doi_thuong (
    id SERIAL PRIMARY KEY,
    ten_thuong VARCHAR(100) NOT NULL,
    mo_ta TEXT,
    diem_yeu_cau INTEGER NOT NULL,
    loai_giam VARCHAR(20) NOT NULL CHECK (loai_giam IN ('phan_tram', 'tien_mat')),
    gia_tri_giam DECIMAL(10,2) NOT NULL,
    gia_tri_don_toi_thieu DECIMAL(10,2) DEFAULT 0,
    thoi_han_su_dung INTEGER DEFAULT 30, -- số ngày
    trang_thai BOOLEAN DEFAULT TRUE,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 14. BẢNG LỊCH SỬ GIAO DỊCH ĐIỂM
-- =============================================
CREATE TABLE giao_dich_diem (
    id SERIAL PRIMARY KEY,
    khach_hang_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    diem INTEGER NOT NULL,
    loai_giao_dich VARCHAR(20) NOT NULL CHECK (loai_giao_dich IN ('cong', 'tru', 'doi_thuong')),
    mo_ta TEXT,
    dat_lich_id INTEGER REFERENCES dat_lich(id),
    hoa_don_id INTEGER REFERENCES hoa_don(id),
    diem_doi_thuong_id INTEGER REFERENCES diem_doi_thuong(id),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 15. BẢNG ĐÁNH GIÁ
-- =============================================
CREATE TABLE danh_gia (
    id SERIAL PRIMARY KEY,
    dat_lich_id INTEGER REFERENCES dat_lich(id) NOT NULL,
    khach_hang_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    nhan_vien_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    diem_nhan_vien INTEGER CHECK (diem_nhan_vien BETWEEN 1 AND 5),
    diem_dich_vu INTEGER CHECK (diem_dich_vu BETWEEN 1 AND 5),
    diem_khong_gian INTEGER CHECK (diem_khong_gian BETWEEN 1 AND 5),
    binh_luan TEXT,
    anh_danh_gia TEXT[],
    hien_thi_cong_khai BOOLEAN DEFAULT TRUE,
    trang_thai VARCHAR(20) DEFAULT 'cho_duyet' CHECK (trang_thai IN ('cho_duyet', 'da_duyet', 'da_an')),
    phan_hoi_quan_ly TEXT,
    ngay_phan_hoi TIMESTAMP,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP,
    UNIQUE(dat_lich_id, khach_hang_id)
);

-- =============================================
-- 16. BẢNG GHI CHÚ KHÁCH HÀNG (của nhân viên)
-- =============================================
CREATE TABLE ghi_chu_khach_hang (
    id SERIAL PRIMARY KEY,
    nhan_vien_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    khach_hang_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    ghi_chu TEXT NOT NULL,
    dat_lich_id INTEGER REFERENCES dat_lich(id),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 17. BẢNG LỊCH SỬ TÓC
-- =============================================
CREATE TABLE lich_su_toc (
    id SERIAL PRIMARY KEY,
    dat_lich_id INTEGER REFERENCES dat_lich(id) NOT NULL,
    khach_hang_id INTEGER REFERENCES nguoi_dung(id),
    nhan_vien_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    anh_ket_qua TEXT[],
    ghi_chu TEXT,
    nguoi_tao_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 18. BẢNG STYLIST YÊU THÍCH
-- =============================================
CREATE TABLE stylist_yeu_thich (
    id SERIAL PRIMARY KEY,
    khach_hang_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    nhan_vien_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(khach_hang_id, nhan_vien_id)
);

-- =============================================
-- 19. BẢNG THÔNG BÁO
-- =============================================
CREATE TABLE thong_bao (
    id SERIAL PRIMARY KEY,
    nguoi_dung_id INTEGER REFERENCES nguoi_dung(id) NOT NULL,
    loai_thong_bao VARCHAR(30) NOT NULL,
    tieu_de VARCHAR(200) NOT NULL,
    noi_dung TEXT NOT NULL,
    da_doc BOOLEAN DEFAULT FALSE,
    lien_ket VARCHAR(255),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 20. BẢNG CÀI ĐẶT HỆ THỐNG
-- =============================================
CREATE TABLE cai_dat_he_thong (
    id SERIAL PRIMARY KEY,
    khoa VARCHAR(50) UNIQUE NOT NULL,
    gia_tri TEXT NOT NULL,
    mo_ta TEXT,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 21. BẢNG NỘI DUNG WEBSITE
-- =============================================
CREATE TABLE noi_dung_website (
    id SERIAL PRIMARY KEY,
    loai_noi_dung VARCHAR(30) NOT NULL CHECK (loai_noi_dung IN ('banner', 'gioi_thieu', 'gallery', 'tin_tuc')),
    tieu_de VARCHAR(200),
    noi_dung TEXT,
    anh_minh_hoa VARCHAR(255),
    lien_ket VARCHAR(255),
    thu_tu INTEGER DEFAULT 0,
    trang_thai BOOLEAN DEFAULT TRUE,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 22. BẢNG COMBO DỊCH VỤ
-- =============================================
CREATE TABLE combo_dich_vu (
    id SERIAL PRIMARY KEY,
    ten_combo VARCHAR(100) NOT NULL,
    mo_ta TEXT,
    gia_goc DECIMAL(10,2) NOT NULL,
    gia_combo DECIMAL(10,2) NOT NULL,
    anh_minh_hoa VARCHAR(255),
    trang_thai BOOLEAN DEFAULT TRUE,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    da_xoa BOOLEAN DEFAULT FALSE,
    ngay_xoa TIMESTAMP
);

-- =============================================
-- 23. BẢNG CHI TIẾT COMBO
-- =============================================
CREATE TABLE chi_tiet_combo (
    id SERIAL PRIMARY KEY,
    combo_id INTEGER REFERENCES combo_dich_vu(id) ON DELETE CASCADE,
    dich_vu_id INTEGER REFERENCES dich_vu(id),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- TẠO CÁC INDEX ĐỂ TỐI ƯU HIỆU SUẤT
-- =============================================

-- Index cho bảng người dùng
CREATE INDEX idx_nguoi_dung_so_dien_thoai ON nguoi_dung(so_dien_thoai) WHERE da_xoa = FALSE;
CREATE INDEX idx_nguoi_dung_email ON nguoi_dung(email) WHERE da_xoa = FALSE;
CREATE INDEX idx_nguoi_dung_vai_tro ON nguoi_dung(vai_tro) WHERE da_xoa = FALSE;

-- Index cho bảng đặt lịch
CREATE INDEX idx_dat_lich_ma ON dat_lich(ma_dat_lich) WHERE da_xoa = FALSE;
CREATE INDEX idx_dat_lich_ngay_hen ON dat_lich(ngay_hen, gio_hen) WHERE da_xoa = FALSE;
CREATE INDEX idx_dat_lich_khach_hang ON dat_lich(khach_hang_id) WHERE da_xoa = FALSE;
CREATE INDEX idx_dat_lich_nhan_vien ON dat_lich(nhan_vien_id) WHERE da_xoa = FALSE;
CREATE INDEX idx_dat_lich_trang_thai ON dat_lich(trang_thai) WHERE da_xoa = FALSE;

-- Index cho bảng hóa đơn
CREATE INDEX idx_hoa_don_ma ON hoa_don(ma_hoa_don) WHERE da_xoa = FALSE;
CREATE INDEX idx_hoa_don_ngay ON hoa_don(ngay_thanh_toan) WHERE da_xoa = FALSE;
CREATE INDEX idx_hoa_don_nhan_vien ON hoa_don(nhan_vien_id) WHERE da_xoa = FALSE;
CREATE INDEX idx_hoa_don_khach_hang ON hoa_don(khach_hang_id) WHERE da_xoa = FALSE;

-- Index cho bảng voucher
CREATE INDEX idx_voucher_ma ON voucher(ma_voucher) WHERE da_xoa = FALSE;
CREATE INDEX idx_voucher_ngay ON voucher(ngay_bat_dau, ngay_ket_thuc) WHERE da_xoa = FALSE;

-- Index cho bảng lịch làm việc
CREATE INDEX idx_lich_lam_viec_nhan_vien_ngay ON lich_lam_viec(nhan_vien_id, ngay_lam) WHERE da_xoa = FALSE;

-- Index cho bảng đánh giá
CREATE INDEX idx_danh_gia_nhan_vien ON danh_gia(nhan_vien_id) WHERE da_xoa = FALSE;
CREATE INDEX idx_danh_gia_khach_hang ON danh_gia(khach_hang_id) WHERE da_xoa = FALSE;

-- =============================================
-- CHÈN DỮ LIỆU MẪU
-- =============================================

-- 1. Cài đặt hệ thống
INSERT INTO cai_dat_he_thong (khoa, gia_tri, mo_ta) VALUES
('ten_tiem', 'Barbershop Hoàng Gia', 'Tên tiệm'),
('so_dien_thoai', '0901234567', 'Số điện thoại tiệm'),
('email', 'contact@barbershop.vn', 'Email tiệm'),
('dia_chi', '123 Đường Lê Lợi, Quận 1, TP.HCM', 'Địa chỉ tiệm'),
('gio_mo_cua', '08:00', 'Giờ mở cửa'),
('gio_dong_cua', '21:00', 'Giờ đóng cửa'),
('dat_lich_toi_da_ngay', '30', 'Số ngày đặt lịch tối đa trước'),
('thoi_gian_huy_toi_thieu', '120', 'Thời gian hủy lịch tối thiểu (phút)'),
('ty_le_quy_doi_diem', '1000', '1000đ = 1 điểm'),
('diem_dang_ky_moi', '100', 'Điểm thưởng đăng ký mới'),
('diem_danh_gia', '50', 'Điểm thưởng khi đánh giá'),
('diem_sinh_nhat', '200', 'Điểm thưởng sinh nhật');

-- 2. Người dùng (mật khẩu: "123456" đã hash với bcrypt)
INSERT INTO nguoi_dung (ho_ten, so_dien_thoai, email, mat_khau_hash, vai_tro, ngay_sinh, gioi_tinh, diem_tich_luy) VALUES
-- Quản lý
('Nguyễn Văn An', '0901111111', 'admin@barbershop.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'quan_ly', '1985-03-15', 'nam', 0),

-- Nhân viên
('Trần Minh Hoàng', '0902222222', 'hoang@barbershop.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'nhan_vien', '1992-07-20', 'nam', 0),
('Lê Văn Tuấn', '0903333333', 'tuan@barbershop.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'nhan_vien', '1990-11-10', 'nam', 0),
('Phạm Đức Anh', '0904444444', 'anh@barbershop.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'nhan_vien', '1995-05-25', 'nam', 0),
('Hoàng Minh Tuấn', '0905555555', 'tuan2@barbershop.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'nhan_vien', '1993-09-08', 'nam', 0),

-- Khách hàng
('Nguyễn Văn Bình', '0906666666', 'binh@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1988-12-05', 'nam', 1250),
('Trần Thị Cẩm', '0907777777', 'cam@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1995-06-18', 'nu', 850),
('Lê Minh Đức', '0908888888', 'duc@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1991-04-22', 'nam', 2100),
('Phạm Thị Em', '0909999999', 'em@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1997-08-30', 'nu', 450),
('Hoàng Văn Phong', '0910000000', 'phong@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1989-02-14', 'nam', 3200);

-- 3. Thông tin nhân viên
INSERT INTO thong_tin_nhan_vien (nguoi_dung_id, mo_ta, chuyen_mon, kinh_nghiem_nam, chung_chi, danh_gia_trung_binh, tong_luot_phuc_vu) VALUES
(2, 'Stylist chuyên nghiệp với hơn 10 năm kinh nghiệm', 'Cắt tóc nam Hàn Quốc, Undercut, Fade', 10, ARRAY['Chứng chỉ Vidal Sassoon', 'Toni & Guy Advanced'], 4.8, 523),
(3, 'Chuyên gia về các kiểu tóc Classic và hiện đại', 'Classic, Pompadour, Side Part', 8, ARRAY['Barber License Korea', 'Advanced Styling'], 4.7, 412),
(4, 'Stylist trẻ năng động, theo kịp xu hướng mới nhất', 'Tóc nam Hàn Quốc, Perm, Nhuộm', 5, ARRAY['Basic Barber Certificate', 'Color Specialist'], 4.6, 289),
(5, 'Chuyên về tóc ngắn và tạo kiểu nhanh', 'Buzz Cut, Crew Cut, Quân đội', 6, ARRAY['Military Barber Certified'], 4.5, 356);

-- 4. Danh mục dịch vụ
INSERT INTO danh_muc_dich_vu (ten_danh_muc, mo_ta, thu_tu) VALUES
('Cắt tóc', 'Các dịch vụ cắt tóc cơ bản và cao cấp', 1),
('Nhuộm tóc', 'Dịch vụ nhuộm và highlight', 2),
('Uốn tóc', 'Uốn xoăn và uốn thẳng', 3),
('Gội đầu & Massage', 'Gội đầu dưỡng sinh và massage thư giãn', 4),
('Cạo râu & Tạo kiểu', 'Cạo mặt và tạo kiểu râu', 5),
('Chăm sóc da mặt', 'Các dịch vụ chăm sóc da chuyên sâu', 6);

-- 5. Dịch vụ
INSERT INTO dich_vu (danh_muc_id, ten_dich_vu, mo_ta_ngan, mo_ta_chi_tiet, gia, thoi_gian_thuc_hien, thu_tu) VALUES
-- Cắt tóc
(1, 'Cắt tóc Basic', 'Cắt tóc nam cơ bản', 'Cắt tóc nam truyền thống với kéo và tông đơ, phù hợp mọi kiểu tóc đơn giản', 100000, 30, 1),
(1, 'Cắt tóc Premium', 'Cắt tóc cao cấp với tư vấn', 'Tư vấn kiểu tóc phù hợp, cắt chuyên nghiệp, tạo kiểu hoàn thiện', 150000, 45, 2),
(1, 'Cắt tóc VIP', 'Dịch vụ VIP với stylist chuyên nghiệp', 'Dịch vụ cao cấp nhất: Tư vấn chi tiết, massage đầu, cắt tỉ mỉ, tạo kiểu hoàn hảo', 250000, 60, 3),
(1, 'Cắt tóc trẻ em', 'Cắt tóc cho bé từ 3-12 tuổi', 'Cắt tóc nhẹ nhàng, thoải mái cho các bé, có đồ chơi giải trí', 80000, 25, 4),

-- Nhuộm tóc
(2, 'Nhuộm toàn bộ', 'Nhuộm màu toàn đầu', 'Nhuộm toàn bộ với thuốc nhuộm cao cấp, bảo vệ tóc tối đa', 300000, 90, 5),
(2, 'Nhuộm Highlight', 'Tạo điểm nhấn với highlight', 'Nhuộm highlight tạo chiều sâu và cá tính cho mái tóc', 350000, 120, 6),
(2, 'Tẩy màu', 'Tẩy màu cũ để nhuộm màu mới', 'Tẩy màu chuyên nghiệp, giảm thiểu hư tổn tóc', 200000, 60, 7),

-- Uốn tóc
(3, 'Uốn xoăn Hàn Quốc', 'Uốn xoăn tự nhiên kiểu Hàn', 'Uốn xoăn nhẹ nhàng, tự nhiên theo phong cách Hàn Quốc', 400000, 120, 8),
(3, 'Uốn Perm', 'Uốn xoăn cổ điển', 'Uốn perm tạo độ phồng và xoăn bền lâu', 350000, 90, 9),
(3, 'Duỗi/Ép thẳng', 'Duỗi tóc thẳng tự nhiên', 'Duỗi thẳng công nghệ mới, giữ độ mượt lâu dài', 300000, 90, 10),

-- Gội đầu & Massage
(4, 'Gội đầu thường', 'Gội đầu cơ bản', 'Gội sạch với dầu gội cao cấp', 50000, 15, 11),
(4, 'Gội đầu dưỡng sinh', 'Gội đầu kết hợp massage', 'Gội đầu thư giãn với massage huyệt đạo, giảm stress', 100000, 30, 12),
(4, 'Massage đầu vai gáy', 'Massage chuyên sâu', 'Massage thư giãn toàn bộ vùng đầu, vai, gáy giúp giảm mỏi', 120000, 30, 13),

-- Cạo râu
(5, 'Cạo mặt truyền thống', 'Cạo râu bằng dao', 'Cạo mặt bằng dao cạo truyền thống, mát xa thư giãn', 80000, 20, 14),
(5, 'Tạo kiểu râu', 'Tạo hình và chăm sóc râu', 'Tạo kiểu râu theo yêu cầu, cắt tỉa và dưỡng râu', 100000, 25, 15),

-- Chăm sóc da
(6, 'Chăm sóc da cơ bản', 'Làm sạch và dưỡng da', 'Làm sạch da mặt, tẩy tế bào chết, đắp mặt nạ dưỡng ẩm', 150000, 40, 16),
(6, 'Chăm sóc da cao cấp', 'Trị liệu da toàn diện', 'Chăm sóc da chuyên sâu: Làm sạch, tẩy da chết, đắp mặt nạ, massage mặt', 250000, 60, 17);

-- 6. Combo dịch vụ
INSERT INTO combo_dich_vu (ten_combo, mo_ta, gia_goc, gia_combo, trang_thai) VALUES
('Combo Học sinh', 'Cắt tóc Basic + Gội đầu', 150000, 120000, TRUE),
('Combo Thư giãn', 'Cắt tóc Premium + Gội dưỡng sinh + Massage', 370000, 300000, TRUE),
('Combo Tổng thể', 'Cắt tóc VIP + Nhuộm + Gội massage', 650000, 550000, TRUE),
('Combo VIP', 'Cắt VIP + Cạo mặt + Chăm sóc da cao cấp + Massage', 680000, 580000, TRUE);

-- 7. Chi tiết combo (liên kết dịch vụ với combo)
INSERT INTO chi_tiet_combo (combo_id, dich_vu_id) VALUES
-- Combo Học sinh
(1, 1), (1, 11),
-- Combo Thư giãn
(2, 2), (2, 12), (2, 13),
-- Combo Tổng thể
(3, 3), (3, 5), (3, 12),
-- Combo VIP
(4, 3), (4, 14), (4, 17), (4, 13);

-- 8. Lịch làm việc (2 tuần tới)
INSERT INTO lich_lam_viec (nhan_vien_id, ngay_lam, ca_lam, gio_bat_dau, gio_ket_thuc, trang_thai) VALUES
-- Tuần 1: 2025-10-01 đến 2025-10-07
-- Trần Minh Hoàng (id=2)
(2, '2025-10-01', 'sang', '08:00', '12:00', 'da_duyet'),
(2, '2025-10-01', 'chieu', '13:00', '17:00', 'da_duyet'),
(2, '2025-10-02', 'sang', '08:00', '12:00', 'da_duyet'),
(2, '2025-10-02', 'chieu', '13:00', '17:00', 'da_duyet'),
(2, '2025-10-03', 'sang', '08:00', '12:00', 'da_duyet'),
(2, '2025-10-03', 'toi', '17:00', '21:00', 'da_duyet'),
(2, '2025-10-04', 'chieu', '13:00', '17:00', 'da_duyet'),
(2, '2025-10-04', 'toi', '17:00', '21:00', 'da_duyet'),

-- Lê Văn Tuấn (id=3)
(3, '2025-10-01', 'chieu', '13:00', '17:00', 'da_duyet'),
(3, '2025-10-01', 'toi', '17:00', '21:00', 'da_duyet'),
(3, '2025-10-02', 'sang', '08:00', '12:00', 'da_duyet'),
(3, '2025-10-02', 'toi', '17:00', '21:00', 'da_duyet'),
(3, '2025-10-03', 'chieu', '13:00', '17:00', 'da_duyet'),
(3, '2025-10-03', 'toi', '17:00', '21:00', 'da_duyet'),
(3, '2025-10-05', 'sang', '08:00', '12:00', 'da_duyet'),
(3, '2025-10-05', 'chieu', '13:00', '17:00', 'da_duyet'),

-- Phạm Đức Anh (id=4)
(4, '2025-10-01', 'sang', '08:00', '12:00', 'da_duyet'),
(4, '2025-10-01', 'toi', '17:00', '21:00', 'da_duyet'),
(4, '2025-10-03', 'sang', '08:00', '12:00', 'da_duyet'),
(4, '2025-10-03', 'chieu', '13:00', '17:00', 'da_duyet'),
(4, '2025-10-04', 'sang', '08:00', '12:00', 'da_duyet'),
(4, '2025-10-04', 'toi', '17:00', '21:00', 'da_duyet'),
(4, '2025-10-06', 'chieu', '13:00', '17:00', 'da_duyet'),
(4, '2025-10-06', 'toi', '17:00', '21:00', 'da_duyet'),

-- Hoàng Minh Tuấn (id=5)
(5, '2025-10-02', 'chieu', '13:00', '17:00', 'da_duyet'),
(5, '2025-10-02', 'toi', '17:00', '21:00', 'da_duyet'),
(5, '2025-10-04', 'sang', '08:00', '12:00', 'da_duyet'),
(5, '2025-10-04', 'chieu', '13:00', '17:00', 'da_duyet'),
(5, '2025-10-05', 'toi', '17:00', '21:00', 'da_duyet'),
(5, '2025-10-06', 'sang', '08:00', '12:00', 'da_duyet'),
(5, '2025-10-07', 'sang', '08:00', '12:00', 'da_duyet'),
(5, '2025-10-07', 'chieu', '13:00', '17:00', 'da_duyet');

-- 9. Voucher
INSERT INTO voucher (ma_voucher, ten_voucher, mo_ta, loai_giam, gia_tri_giam, gia_tri_don_toi_thieu, giam_toi_da, ngay_bat_dau, ngay_ket_thuc, so_luong_tong, so_luong_da_dung, ap_dung_cho, hien_thi_cong_khai) VALUES
('GIAM20K', 'Giảm 20K cho đơn từ 150K', 'Voucher giảm giá cho khách hàng mới', 'tien_mat', 20000, 150000, 20000, '2025-10-01', '2025-10-31', 100, 15, 'khach_moi', TRUE),
('GIAM10', 'Giảm 10% tối đa 50K', 'Giảm 10% cho mọi đơn hàng', 'phan_tram', 10, 200000, 50000, '2025-10-01', '2025-10-31', 200, 45, 'tat_ca', TRUE),
('SINH_NHAT', 'Giảm 50K sinh nhật', 'Voucher tặng sinh nhật khách hàng', 'tien_mat', 50000, 100000, 50000, '2025-10-01', '2025-12-31', NULL, 8, 'tat_ca', FALSE),
('VIP100', 'Giảm 100K cho VIP', 'Voucher dành cho khách VIP', 'tien_mat', 100000, 500000, 100000, '2025-10-01', '2025-11-30', 50, 12, 'khach_cu', TRUE),
('COMBO20', 'Giảm 20% Combo', 'Giảm 20% khi đặt combo', 'phan_tram', 20, 300000, 100000, '2025-10-01', '2025-10-15', 80, 23, 'tat_ca', TRUE);

-- 10. Voucher của khách hàng
INSERT INTO voucher_khach_hang (voucher_id, khach_hang_id, ma_voucher_ca_nhan, da_su_dung, ngay_het_han) VALUES
(1, 6, 'GIAM20K-KH001', FALSE, '2025-10-31'),
(2, 6, 'GIAM10-KH001', FALSE, '2025-10-31'),
(3, 7, 'SINH_NHAT-KH002', FALSE, '2025-12-31'),
(4, 8, 'VIP100-KH003', FALSE, '2025-11-30'),
(2, 8, 'GIAM10-KH003', TRUE, '2025-10-31'),
(5, 9, 'COMBO20-KH004', FALSE, '2025-10-15'),
(2, 10, 'GIAM10-KH005', FALSE, '2025-10-31');

-- 11. Điểm đổi thưởng
INSERT INTO diem_doi_thuong (ten_thuong, mo_ta, diem_yeu_cau, loai_giam, gia_tri_giam, gia_tri_don_toi_thieu, thoi_han_su_dung) VALUES
('Voucher 50K', 'Đổi 500 điểm lấy voucher 50K', 500, 'tien_mat', 50000, 100000, 30),
('Voucher 100K', 'Đổi 1000 điểm lấy voucher 100K', 1000, 'tien_mat', 100000, 200000, 30),
('Giảm 15%', 'Đổi 800 điểm lấy voucher giảm 15%', 800, 'phan_tram', 15, 150000, 45),
('Voucher 200K', 'Đổi 2000 điểm lấy voucher 200K', 2000, 'tien_mat', 200000, 400000, 60),
('Giảm 25%', 'Đổi 1500 điểm lấy voucher giảm 25%', 1500, 'phan_tram', 25, 300000, 45);

-- 12. Đặt lịch (booking) - đã hoàn thành
INSERT INTO dat_lich (ma_dat_lich, khach_hang_id, ten_khach_hang, so_dien_thoai_khach, email_khach, nhan_vien_id, ngay_hen, gio_hen, loai_dat_lich, tong_tien, tien_giam_gia, thanh_tien, trang_thai, ngay_check_in, ngay_hoan_thanh) VALUES
('BK20250915001', 6, 'Nguyễn Văn Bình', '0906666666', 'binh@email.com', 2, '2025-09-15', '09:00', 'online', 150000, 0, 150000, 'hoan_thanh', '2025-09-15 08:55:00', '2025-09-15 09:45:00'),
('BK20250920001', 7, 'Trần Thị Cẩm', '0907777777', 'cam@email.com', 3, '2025-09-20', '14:00', 'online', 370000, 0, 370000, 'hoan_thanh', '2025-09-20 13:50:00', '2025-09-20 15:10:00'),
('BK20250925001', 8, 'Lê Minh Đức', '0908888888', 'duc@email.com', 2, '2025-09-25', '10:00', 'online', 650000, 100000, 550000, 'hoan_thanh', '2025-09-25 09:55:00', '2025-09-25 12:15:00'),
('BK20250928001', 10, 'Hoàng Văn Phong', '0910000000', 'phong@email.com', 4, '2025-09-28', '15:30', 'online', 100000, 0, 100000, 'hoan_thanh', '2025-09-28 15:25:00', '2025-09-28 16:00:00'),

-- Đặt lịch sắp tới
('BK20251002001', 6, 'Nguyễn Văn Bình', '0906666666', 'binh@email.com', 2, '2025-10-02', '09:30', 'online', 250000, 20000, 230000, 'da_xac_nhan', NULL, NULL),
('BK20251003001', 8, 'Lê Minh Đức', '0908888888', 'duc@email.com', 3, '2025-10-03', '14:00', 'online', 100000, 0, 100000, 'da_xac_nhan', NULL, NULL),
('BK20251004001', 9, 'Phạm Thị Em', '0909999999', 'em@email.com', 4, '2025-10-04', '10:00', 'online', 300000, 60000, 240000, 'da_xac_nhan', NULL, NULL),

-- Walk-in (khách vãng lai)
('BK20250918001', NULL, 'Nguyễn Văn Khách', '0911111111', NULL, 2, '2025-09-18', '11:00', 'walk_in', 100000, 0, 100000, 'hoan_thanh', '2025-09-18 11:00:00', '2025-09-18 11:30:00'),
('BK20250922001', NULL, 'Trần Văn Khách 2', '0912222222', NULL, 3, '2025-09-22', '16:00', 'walk_in', 150000, 0, 150000, 'hoan_thanh', '2025-09-22 16:00:00', '2025-09-22 16:45:00');

-- 13. Dịch vụ trong đặt lịch
INSERT INTO dich_vu_dat_lich (dat_lich_id, dich_vu_id, ten_dich_vu, gia, so_luong, thanh_tien) VALUES
-- BK20250915001
(1, 2, 'Cắt tóc Premium', 150000, 1, 150000),

-- BK20250920001
(2, 2, 'Cắt tóc Premium', 150000, 1, 150000),
(2, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),
(2, 13, 'Massage đầu vai gáy', 120000, 1, 120000),

-- BK20250925001
(3, 3, 'Cắt tóc VIP', 250000, 1, 250000),
(3, 5, 'Nhuộm toàn bộ', 300000, 1, 300000),
(3, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),

-- BK20250928001
(4, 1, 'Cắt tóc Basic', 100000, 1, 100000),

-- BK20251002001
(5, 3, 'Cắt tóc VIP', 250000, 1, 250000),

-- BK20251003001
(6, 1, 'Cắt tóc Basic', 100000, 1, 100000),

-- BK20251004001
(7, 5, 'Nhuộm toàn bộ', 300000, 1, 300000),

-- Walk-in
(8, 1, 'Cắt tóc Basic', 100000, 1, 100000),
(9, 2, 'Cắt tóc Premium', 150000, 1, 150000);

-- 14. Hóa đơn (Invoice từ POS)
INSERT INTO hoa_don (ma_hoa_don, dat_lich_id, khach_hang_id, ten_khach_hang, so_dien_thoai_khach, nhan_vien_id, tam_tinh, tien_giam_gia, thanh_tien, phuong_thuc_thanh_toan, tien_khach_dua, tien_thua, nguoi_tao_id, ngay_thanh_toan) VALUES
-- Từ booking
('INV20250915001', 1, 6, 'Nguyễn Văn Bình', '0906666666', 2, 150000, 0, 150000, 'tien_mat', 200000, 50000, 2, '2025-09-15 09:45:00'),
('INV20250920001', 2, 7, 'Trần Thị Cẩm', '0907777777', 3, 370000, 0, 370000, 'chuyen_khoan', NULL, NULL, 3, '2025-09-20 15:10:00'),
('INV20250925001', 3, 8, 'Lê Minh Đức', '0908888888', 2, 650000, 100000, 550000, 'tien_mat', 600000, 50000, 2, '2025-09-25 12:15:00'),
('INV20250928001', 4, 10, 'Hoàng Văn Phong', '0910000000', 4, 100000, 0, 100000, 'vi_dien_tu', NULL, NULL, 4, '2025-09-28 16:00:00'),

-- Walk-in (không có booking)
('INV20250918001', 8, NULL, 'Nguyễn Văn Khách', '0911111111', 2, 100000, 0, 100000, 'tien_mat', 100000, 0, 2, '2025-09-18 11:30:00'),
('INV20250922001', 9, NULL, 'Trần Văn Khách 2', '0912222222', 3, 150000, 0, 150000, 'tien_mat', 200000, 50000, 3, '2025-09-22 16:45:00'),

-- Walk-in với khách có tài khoản
('INV20250924001', NULL, 6, 'Nguyễn Văn Bình', '0906666666', 3, 200000, 20000, 180000, 'chuyen_khoan', NULL, NULL, 3, '2025-09-24 17:30:00'),
('INV20250927001', NULL, 8, 'Lê Minh Đức', '0908888888', 4, 350000, 0, 350000, 'the', NULL, NULL, 4, '2025-09-27 19:15:00');

-- 15. Chi tiết hóa đơn
INSERT INTO chi_tiet_hoa_don (hoa_don_id, dich_vu_id, ten_dich_vu, gia, so_luong, thanh_tien) VALUES
-- INV20250915001
(1, 2, 'Cắt tóc Premium', 150000, 1, 150000),

-- INV20250920001
(2, 2, 'Cắt tóc Premium', 150000, 1, 150000),
(2, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),
(2, 13, 'Massage đầu vai gáy', 120000, 1, 120000),

-- INV20250925001
(3, 3, 'Cắt tóc VIP', 250000, 1, 250000),
(3, 5, 'Nhuộm toàn bộ', 300000, 1, 300000),
(3, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),

-- INV20250928001
(4, 1, 'Cắt tóc Basic', 100000, 1, 100000),

-- INV20250918001 (walk-in)
(5, 1, 'Cắt tóc Basic', 100000, 1, 100000),

-- INV20250922001 (walk-in)
(6, 2, 'Cắt tóc Premium', 150000, 1, 150000),

-- INV20250924001 (walk-in với tài khoản)
(7, 1, 'Cắt tóc Basic', 100000, 1, 100000),
(7, 11, 'Gội đầu thường', 50000, 1, 50000),
(7, 11, 'Gội đầu thường', 50000, 1, 50000),

-- INV20250927001 (walk-in với tài khoản)
(8, 2, 'Cắt tóc Premium', 150000, 1, 150000),
(8, 5, 'Nhuộm toàn bộ', 300000, 1, 300000),
(8, 11, 'Gội đầu thường', 50000, 1, 50000);

-- 16. Giao dịch điểm
INSERT INTO giao_dich_diem (khach_hang_id, diem, loai_giao_dich, mo_ta, dat_lich_id, hoa_don_id, ngay_tao) VALUES
-- Cộng điểm từ booking đã hoàn thành
(6, 150, 'cong', 'Cộng điểm từ đơn hàng BK20250915001', 1, 1, '2025-09-15 09:45:00'),
(7, 370, 'cong', 'Cộng điểm từ đơn hàng BK20250920001', 2, 2, '2025-09-20 15:10:00'),
(8, 550, 'cong', 'Cộng điểm từ đơn hàng BK20250925001', 3, 3, '2025-09-25 12:15:00'),
(10, 100, 'cong', 'Cộng điểm từ đơn hàng BK20250928001', 4, 4, '2025-09-28 16:00:00'),

-- Cộng điểm từ walk-in
(6, 180, 'cong', 'Cộng điểm từ hóa đơn INV20250924001', NULL, 7, '2025-09-24 17:30:00'),
(8, 350, 'cong', 'Cộng điểm từ hóa đơn INV20250927001', NULL, 8, '2025-09-27 19:15:00'),

-- Cộng điểm thưởng
(6, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-09-01 10:00:00'),
(7, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-09-02 14:30:00'),
(8, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-08-15 09:00:00'),
(9, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-09-10 16:00:00'),
(10, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-08-01 11:00:00'),

-- Cộng điểm từ đánh giá
(6, 50, 'cong', 'Điểm thưởng viết đánh giá', 1, NULL, '2025-09-16 10:00:00'),
(7, 50, 'cong', 'Điểm thưởng viết đánh giá', 2, NULL, '2025-09-21 09:30:00'),
(8, 50, 'cong', 'Điểm thưởng viết đánh giá', 3, NULL, '2025-09-26 14:00:00'),

-- Trừ điểm (đổi thưởng)
(8, -500, 'doi_thuong', 'Đổi voucher 50K', NULL, NULL, '2025-09-27 10:00:00'),
(10, -1000, 'doi_thuong', 'Đổi voucher 100K', NULL, NULL, '2025-09-20 15:30:00'),

-- Cộng điểm sinh nhật
(6, 200, 'cong', 'Điểm thưởng sinh nhật', NULL, NULL, '2024-12-05 00:00:00'),
(10, 200, 'cong', 'Điểm thưởng sinh nhật', NULL, NULL, '2025-02-14 00:00:00');

-- 17. Đánh giá
INSERT INTO danh_gia (dat_lich_id, khach_hang_id, nhan_vien_id, diem_nhan_vien, diem_dich_vu, diem_khong_gian, binh_luan, hien_thi_cong_khai, trang_thai, ngay_tao) VALUES
(1, 6, 2, 5, 5, 5, 'Rất hài lòng với dịch vụ! Anh Hoàng cắt tóc rất tỉ mỉ và chuyên nghiệp. Không gian thoải mái, sạch sẽ. Sẽ quay lại lần sau!', TRUE, 'da_duyet', '2025-09-16 10:00:00'),
(2, 7, 3, 5, 5, 4, 'Dịch vụ tuyệt vời, anh Tuấn rất nhiệt tình. Gội đầu massage rất thư giãn. Chỉ có điều chỗ đậu xe hơi khó một chút.', TRUE, 'da_duyet', '2025-09-21 09:30:00'),
(3, 8, 2, 5, 4, 5, 'Cắt và nhuộm tóc đẹp lắm! Màu nhuộm rất chuẩn, đúng như mình mong muốn. Anh Hoàng tư vấn rất tận tâm. Giá cả hợp lý.', TRUE, 'da_duyet', '2025-09-26 14:00:00'),
(4, 10, 4, 4, 4, 5, 'Dịch vụ tốt, cắt nhanh gọn. Không gian đẹp, nhân viên thân thiện. Sẽ giới thiệu bạn bè đến.', TRUE, 'da_duyet', '2025-09-29 11:00:00');

-- 18. Ghi chú khách hàng
INSERT INTO ghi_chu_khach_hang (nhan_vien_id, khach_hang_id, ghi_chu, dat_lich_id, ngay_tao) VALUES
(2, 6, 'Khách thích cắt undercut, để mái dài phía trước. Không dùng sáp tạo kiểu.', 1, '2025-09-15 09:45:00'),
(3, 7, 'Khách ưa thích phong cách Hàn Quốc, tóc xoăn nhẹ. Hay đặt lịch vào chiều thứ 6.', 2, '2025-09-20 15:10:00'),
(2, 8, 'Khách VIP, thích thử màu tóc mới. Da đầu nhạy cảm, cần dùng thuốc nhuộm cao cấp.', 3, '2025-09-25 12:15:00'),
(4, 10, 'Khách cắt tóc ngắn gọn, không cầu kỳ. Thường đến buổi chiều sau giờ làm.', 4, '2025-09-28 16:00:00');

-- 19. Lịch sử tóc
INSERT INTO lich_su_toc (dat_lich_id, khach_hang_id, nhan_vien_id, anh_ket_qua, ghi_chu, nguoi_tao_id, ngay_tao) VALUES
(1, 6, 2, ARRAY['https://example.com/hair1.jpg'], 'Cắt undercut fade, để mái dài 7cm', 2, '2025-09-15 09:45:00'),
(2, 7, 3, ARRAY['https://example.com/hair2.jpg', 'https://example.com/hair2b.jpg'], 'Cắt layer Hàn Quốc, massage thư giãn', 3, '2025-09-20 15:10:00'),
(3, 8, 2, ARRAY['https://example.com/hair3.jpg'], 'Cắt side part + nhuộm màu nâu khói, gội dưỡng màu', 2, '2025-09-25 12:15:00'),
(4, 10, 4, ARRAY['https://example.com/hair4.jpg'], 'Cắt buzz cut số 3', 4, '2025-09-28 16:00:00');

-- 20. Stylist yêu thích
INSERT INTO stylist_yeu_thich (khach_hang_id, nhan_vien_id, ngay_tao) VALUES
(6, 2, '2025-09-16 10:30:00'),
(7, 3, '2025-09-21 10:00:00'),
(8, 2, '2025-09-26 14:30:00'),
(10, 4, '2025-09-29 11:30:00'),
(9, 3, '2025-09-15 16:00:00');

-- 21. Thông báo
INSERT INTO thong_bao (nguoi_dung_id, loai_thong_bao, tieu_de, noi_dung, da_doc, lien_ket, ngay_tao) VALUES
(6, 'xac_nhan_dat_lich', 'Đặt lịch thành công', 'Bạn đã đặt lịch thành công cho ngày 02/10/2025 lúc 09:30. Mã đặt lịch: BK20251002001', FALSE, '/customer/booking/5', '2025-09-30 14:00:00'),
(6, 'nhac_lich', 'Nhắc lịch hẹn', 'Bạn có lịch hẹn vào ngày mai 02/10/2025 lúc 09:30 tại Barbershop Hoàng Gia', FALSE, '/customer/booking/5', '2025-10-01 09:30:00'),
(8, 'xac_nhan_dat_lich', 'Đặt lịch thành công', 'Bạn đã đặt lịch thành công cho ngày 03/10/2025 lúc 14:00. Mã đặt lịch: BK20251003001', TRUE, '/customer/booking/6', '2025-09-29 10:00:00'),
(9, 'khuyen_mai', 'Voucher mới cho bạn!', 'Bạn vừa nhận được voucher COMBO20 - Giảm 20% khi đặt combo. Hạn sử dụng đến 15/10/2025', FALSE, '/customer/rewards', '2025-09-28 09:00:00'),
(10, 'cong_diem', 'Cộng điểm thành công', 'Bạn vừa được cộng 100 điểm từ đơn hàng BK20250928001. Tổng điểm hiện tại: 3200', TRUE, '/customer/rewards', '2025-09-28 16:00:00'),
(2, 'lich_lam_viec', 'Lịch làm việc tuần mới', 'Lịch làm việc tuần 01/10 - 07/10 đã được phê duyệt. Vui lòng kiểm tra.', FALSE, '/staff/schedule', '2025-09-29 08:00:00'),
(3, 'danh_gia_moi', 'Bạn có đánh giá mới', 'Khách hàng Trần Thị Cẩm vừa đánh giá 5 sao dịch vụ của bạn', TRUE, '/staff/reviews', '2025-09-21 09:30:00');

-- 22. Nội dung website
INSERT INTO noi_dung_website (loai_noi_dung, tieu_de, noi_dung, anh_minh_hoa, lien_ket, thu_tu, trang_thai) VALUES
-- Banner
('banner', 'Chào mừng đến Barbershop Hoàng Gia', 'Phong cách nam tính - Đẳng cấp hoàng gia', 'https://example.com/banner1.jpg', '/services', 1, TRUE),
('banner', 'Giảm 20% cho khách hàng mới', 'Đăng ký ngay hôm nay để nhận ưu đãi', 'https://example.com/banner2.jpg', '/register', 2, TRUE),
('banner', 'Combo tiết kiệm - Chỉ từ 120K', 'Cắt + Gội chỉ từ 120K - Tiết kiệm 30K', 'https://example.com/banner3.jpg', '/services', 3, TRUE),

-- Giới thiệu
('gioi_thieu', 'Về chúng tôi', 'Barbershop Hoàng Gia được thành lập năm 2015 với sứ mệnh mang đến dịch vụ cắt tóc nam chuyên nghiệp và đẳng cấp. Với đội ngũ thợ cắt tóc giàu kinh nghiệm, được đào tạo bài bản, chúng tôi cam kết mang lại sự hài lòng tuyệt đối cho khách hàng.', 'https://example.com/about.jpg', NULL, 1, TRUE),

-- Gallery
('gallery', 'Không gian tiệm', NULL, 'https://example.com/gallery1.jpg', NULL, 1, TRUE),
('gallery', 'Ghế cắt tóc cao cấp', NULL, 'https://example.com/gallery2.jpg', NULL, 2, TRUE),
('gallery', 'Khu vực chờ', NULL, 'https://example.com/gallery3.jpg', NULL, 3, TRUE),
('gallery', 'Mẫu tóc Undercut', NULL, 'https://example.com/style1.jpg', NULL, 4, TRUE),
('gallery', 'Mẫu tóc Pompadour', NULL, 'https://example.com/style2.jpg', NULL, 5, TRUE),
('gallery', 'Mẫu tóc Hàn Quốc', NULL, 'https://example.com/style3.jpg', NULL, 6, TRUE),

-- Tin tức
('tin_tuc', 'Xu hướng tóc nam 2025', 'Khám phá những xu hướng tóc nam hot nhất năm 2025: Undercut, Two Block, Comma Hair...', 'https://example.com/news1.jpg', '/blog/1', 1, TRUE),
('tin_tuc', 'Bí quyết chăm sóc tóc sau nhuộm', 'Cách chăm sóc tóc nhuộm để giữ màu đẹp lâu và tóc khỏe mạnh', 'https://example.com/news2.jpg', '/blog/2', 2, TRUE);

-- 23. Yêu cầu nghỉ phép
INSERT INTO yeu_cau_nghi_phep (nhan_vien_id, ngay_bat_dau, ngay_ket_thuc, ly_do, trang_thai, nguoi_duyet_id, ghi_chu_duyet, ngay_duyet) VALUES
(2, '2025-10-10', '2025-10-12', 'Về quê có việc gia đình', 'da_duyet', 1, 'Đã duyệt', '2025-09-25 10:00:00'),
(3, '2025-10-15', '2025-10-15', 'Khám sức khỏe định kỳ', 'da_duyet', 1, 'Đã duyệt', '2025-09-28 09:00:00'),
(4, '2025-10-20', '2025-10-22', 'Tham gia khóa đào tạo', 'cho_duyet', NULL, NULL, NULL),
(5, '2025-11-01', '2025-11-03', 'Du lịch nghỉ ngơi', 'cho_duyet', NULL, NULL, NULL);

-- =============================================