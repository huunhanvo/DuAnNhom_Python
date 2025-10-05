-- =============================================
-- DỮ LIỆU MẪU BỔ SUNG - ĐÃ SỬA LỖI FOREIGN KEY
-- =============================================

-- 1. Thêm người dùng (khách hàng) - PHẢI CHẠY TRƯỚC
INSERT INTO nguoi_dung (ho_ten, so_dien_thoai, email, mat_khau_hash, vai_tro, ngay_sinh, gioi_tinh, diem_tich_luy) VALUES
('Vũ Văn Giang', '0913333333', 'giang@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1994-03-12', 'nam', 750),
('Đỗ Thị Hoa', '0914444444', 'hoa@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1996-07-08', 'nu', 520),
('Bùi Văn Khải', '0915555555', 'khai@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1990-11-25', 'nam', 1850),
('Đinh Thị Lan', '0916666666', 'lan@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1998-01-30', 'nu', 300),
('Trương Văn Minh', '0917777777', 'minh@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7M.E3bpFUq', 'khach_hang', '1987-09-15', 'nam', 2400);

-- 2. Thêm lịch làm việc tuần 2 (08/10 - 14/10)
INSERT INTO lich_lam_viec (nhan_vien_id, ngay_lam, ca_lam, gio_bat_dau, gio_ket_thuc, trang_thai) VALUES
-- Trần Minh Hoàng (id=2)
(2, '2025-10-08', 'sang', '08:00', '12:00', 'da_duyet'),
(2, '2025-10-08', 'chieu', '13:00', '17:00', 'da_duyet'),
(2, '2025-10-09', 'sang', '08:00', '12:00', 'da_duyet'),
(2, '2025-10-09', 'toi', '17:00', '21:00', 'da_duyet'),
(2, '2025-10-13', 'chieu', '13:00', '17:00', 'da_duyet'),
(2, '2025-10-13', 'toi', '17:00', '21:00', 'da_duyet'),
(2, '2025-10-14', 'sang', '08:00', '12:00', 'da_duyet'),

-- Lê Văn Tuấn (id=3)
(3, '2025-10-08', 'chieu', '13:00', '17:00', 'da_duyet'),
(3, '2025-10-08', 'toi', '17:00', '21:00', 'da_duyet'),
(3, '2025-10-09', 'sang', '08:00', '12:00', 'da_duyet'),
(3, '2025-10-09', 'chieu', '13:00', '17:00', 'da_duyet'),
(3, '2025-10-10', 'sang', '08:00', '12:00', 'da_duyet'),
(3, '2025-10-11', 'chieu', '13:00', '17:00', 'da_duyet'),
(3, '2025-10-11', 'toi', '17:00', '21:00', 'da_duyet'),
(3, '2025-10-14', 'sang', '08:00', '12:00', 'da_duyet'),
(3, '2025-10-14', 'toi', '17:00', '21:00', 'da_duyet'),

-- Phạm Đức Anh (id=4)
(4, '2025-10-08', 'sang', '08:00', '12:00', 'da_duyet'),
(4, '2025-10-09', 'chieu', '13:00', '17:00', 'da_duyet'),
(4, '2025-10-09', 'toi', '17:00', '21:00', 'da_duyet'),
(4, '2025-10-10', 'sang', '08:00', '12:00', 'da_duyet'),
(4, '2025-10-10', 'toi', '17:00', '21:00', 'da_duyet'),
(4, '2025-10-11', 'sang', '08:00', '12:00', 'da_duyet'),
(4, '2025-10-13', 'chieu', '13:00', '17:00', 'da_duyet'),
(4, '2025-10-14', 'sang', '08:00', '12:00', 'da_duyet'),

-- Hoàng Minh Tuấn (id=5)
(5, '2025-10-08', 'toi', '17:00', '21:00', 'da_duyet'),
(5, '2025-10-09', 'sang', '08:00', '12:00', 'da_duyet'),
(5, '2025-10-10', 'chieu', '13:00', '17:00', 'da_duyet'),
(5, '2025-10-10', 'toi', '17:00', '21:00', 'da_duyet'),
(5, '2025-10-11', 'sang', '08:00', '12:00', 'da_duyet'),
(5, '2025-10-13', 'sang', '08:00', '12:00', 'da_duyet'),
(5, '2025-10-13', 'toi', '17:00', '21:00', 'da_duyet'),
(5, '2025-10-14', 'chieu', '13:00', '17:00', 'da_duyet');

-- 3. Thêm đặt lịch đã hoàn thành (tháng 8)
INSERT INTO dat_lich (ma_dat_lich, khach_hang_id, ten_khach_hang, so_dien_thoai_khach, email_khach, nhan_vien_id, ngay_hen, gio_hen, loai_dat_lich, tong_tien, tien_giam_gia, thanh_tien, trang_thai, ngay_check_in, ngay_hoan_thanh) VALUES
('BK20250805001', 6, 'Nguyễn Văn Bình', '0906666666', 'binh@email.com', 2, '2025-08-05', '10:00', 'online', 100000, 0, 100000, 'hoan_thanh', '2025-08-05 09:55:00', '2025-08-05 10:30:00'),
('BK20250812001', 8, 'Lê Minh Đức', '0908888888', 'duc@email.com', 3, '2025-08-12', '15:00', 'online', 250000, 0, 250000, 'hoan_thanh', '2025-08-12 14:50:00', '2025-08-12 15:50:00'),
('BK20250820001', 10, 'Hoàng Văn Phong', '0910000000', 'phong@email.com', 4, '2025-08-20', '14:00', 'online', 370000, 0, 370000, 'hoan_thanh', '2025-08-20 13:55:00', '2025-08-20 15:10:00'),
('BK20250825001', 13, 'Bùi Văn Khải', '0915555555', 'khai@email.com', 2, '2025-08-25', '09:30', 'online', 150000, 0, 150000, 'hoan_thanh', '2025-08-25 09:25:00', '2025-08-25 10:15:00');

-- 4. Dịch vụ cho booking tháng 8
INSERT INTO dich_vu_dat_lich (dat_lich_id, dich_vu_id, ten_dich_vu, gia, so_luong, thanh_tien) VALUES
(10, 1, 'Cắt tóc Basic', 100000, 1, 100000),
(11, 3, 'Cắt tóc VIP', 250000, 1, 250000),
(12, 2, 'Cắt tóc Premium', 150000, 1, 150000),
(12, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),
(12, 13, 'Massage đầu vai gáy', 120000, 1, 120000),
(13, 2, 'Cắt tóc Premium', 150000, 1, 150000);

-- 5. Hóa đơn tháng 8
INSERT INTO hoa_don (ma_hoa_don, dat_lich_id, khach_hang_id, ten_khach_hang, so_dien_thoai_khach, nhan_vien_id, tam_tinh, tien_giam_gia, thanh_tien, phuong_thuc_thanh_toan, tien_khach_dua, tien_thua, nguoi_tao_id, ngay_thanh_toan) VALUES
('INV20250805001', 10, 6, 'Nguyễn Văn Bình', '0906666666', 2, 100000, 0, 100000, 'tien_mat', 100000, 0, 2, '2025-08-05 10:30:00'),
('INV20250812001', 11, 8, 'Lê Minh Đức', '0908888888', 3, 250000, 0, 250000, 'chuyen_khoan', NULL, NULL, 3, '2025-08-12 15:50:00'),
('INV20250820001', 12, 10, 'Hoàng Văn Phong', '0910000000', 4, 370000, 0, 370000, 'vi_dien_tu', NULL, NULL, 4, '2025-08-20 15:10:00'),
('INV20250825001', 13, 13, 'Bùi Văn Khải', '0915555555', 2, 150000, 0, 150000, 'tien_mat', 200000, 50000, 2, '2025-08-25 10:15:00');

-- 6. Chi tiết hóa đơn tháng 8
INSERT INTO chi_tiet_hoa_don (hoa_don_id, dich_vu_id, ten_dich_vu, gia, so_luong, thanh_tien) VALUES
(9, 1, 'Cắt tóc Basic', 100000, 1, 100000),
(10, 3, 'Cắt tóc VIP', 250000, 1, 250000),
(11, 2, 'Cắt tóc Premium', 150000, 1, 150000),
(11, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),
(11, 13, 'Massage đầu vai gáy', 120000, 1, 120000),
(12, 2, 'Cắt tóc Premium', 150000, 1, 150000);

-- 7. Thêm đặt lịch tháng 9 (đã hoàn thành)
INSERT INTO dat_lich (ma_dat_lich, khach_hang_id, ten_khach_hang, so_dien_thoai_khach, email_khach, nhan_vien_id, ngay_hen, gio_hen, loai_dat_lich, tong_tien, tien_giam_gia, thanh_tien, trang_thai, ngay_check_in, ngay_hoan_thanh) VALUES
('BK20250910001', 11, 'Vũ Văn Giang', '0913333333', 'giang@email.com', 2, '2025-09-10', '10:00', 'online', 100000, 0, 100000, 'hoan_thanh', '2025-09-10 09:55:00', '2025-09-10 10:30:00'),
('BK20250912001', 13, 'Bùi Văn Khải', '0915555555', 'khai@email.com', 3, '2025-09-12', '15:00', 'online', 250000, 0, 250000, 'hoan_thanh', '2025-09-12 14:50:00', '2025-09-12 15:45:00'),
('BK20250917001', 12, 'Đỗ Thị Hoa', '0914444444', 'hoa@email.com', 4, '2025-09-17', '11:00', 'online', 150000, 0, 150000, 'hoan_thanh', '2025-09-17 10:55:00', '2025-09-17 11:45:00'),
('BK20250919001', 15, 'Trương Văn Minh', '0917777777', 'minh@email.com', 2, '2025-09-19', '16:30', 'online', 650000, 0, 650000, 'hoan_thanh', '2025-09-19 16:25:00', '2025-09-19 18:40:00'),
('BK20250923001', 14, 'Đinh Thị Lan', '0916666666', 'lan@email.com', 5, '2025-09-23', '14:00', 'online', 80000, 0, 80000, 'hoan_thanh', '2025-09-23 13:55:00', '2025-09-23 14:25:00'),
('BK20250916001', 11, 'Vũ Văn Giang', '0913333333', 'giang@email.com', 3, '2025-09-16', '10:00', 'online', 150000, 0, 150000, 'da_huy', NULL, NULL),
('BK20250921001', 14, 'Đinh Thị Lan', '0916666666', 'lan@email.com', 4, '2025-09-21', '09:00', 'online', 100000, 0, 100000, 'khong_den', NULL, NULL);

-- 8. Dịch vụ cho đặt lịch tháng 9
INSERT INTO dich_vu_dat_lich (dat_lich_id, dich_vu_id, ten_dich_vu, gia, so_luong, thanh_tien) VALUES
-- BK20250910001
(14, 1, 'Cắt tóc Basic', 100000, 1, 100000),
-- BK20250912001
(15, 3, 'Cắt tóc VIP', 250000, 1, 250000),
-- BK20250917001
(16, 2, 'Cắt tóc Premium', 150000, 1, 150000),
-- BK20250919001
(17, 3, 'Cắt tóc VIP', 250000, 1, 250000),
(17, 5, 'Nhuộm toàn bộ', 300000, 1, 300000),
(17, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),
-- BK20250923001
(18, 4, 'Cắt tóc trẻ em', 80000, 1, 80000),
-- BK20250916001 (đã hủy)
(19, 2, 'Cắt tóc Premium', 150000, 1, 150000),
-- BK20250921001 (không đến)
(20, 1, 'Cắt tóc Basic', 100000, 1, 100000);

-- 9. Thêm đặt lịch trong tương lai (tháng 10)
INSERT INTO dat_lich (ma_dat_lich, khach_hang_id, ten_khach_hang, so_dien_thoai_khach, email_khach, nhan_vien_id, ngay_hen, gio_hen, loai_dat_lich, tong_tien, tien_giam_gia, thanh_tien, trang_thai) VALUES
('BK20251005001', 11, 'Vũ Văn Giang', '0913333333', 'giang@email.com', 3, '2025-10-05', '10:00', 'online', 150000, 0, 150000, 'da_xac_nhan'),
('BK20251005002', 12, 'Đỗ Thị Hoa', '0914444444', 'hoa@email.com', 4, '2025-10-05', '15:30', 'online', 370000, 0, 370000, 'da_xac_nhan'),
('BK20251006001', 13, 'Bùi Văn Khải', '0915555555', 'khai@email.com', 2, '2025-10-06', '09:00', 'online', 250000, 0, 250000, 'da_xac_nhan'),
('BK20251007001', 7, 'Trần Thị Cẩm', '0907777777', 'cam@email.com', 3, '2025-10-07', '14:00', 'online', 120000, 0, 120000, 'da_xac_nhan'),
('BK20251008001', 15, 'Trương Văn Minh', '0917777777', 'minh@email.com', 4, '2025-10-08', '16:00', 'online', 400000, 0, 400000, 'da_xac_nhan'),
('BK20251009001', 6, 'Nguyễn Văn Bình', '0906666666', 'binh@email.com', 3, '2025-10-09', '10:30', 'online', 100000, 0, 100000, 'da_xac_nhan'),
('BK20251010001', 14, 'Đinh Thị Lan', '0916666666', 'lan@email.com', 5, '2025-10-10', '14:30', 'online', 300000, 0, 300000, 'da_xac_nhan');

-- 10. Dịch vụ cho đặt lịch tháng 10
INSERT INTO dich_vu_dat_lich (dat_lich_id, dich_vu_id, ten_dich_vu, gia, so_luong, thanh_tien) VALUES
-- BK20251005001
(21, 2, 'Cắt tóc Premium', 150000, 1, 150000),
-- BK20251005002
(22, 2, 'Cắt tóc Premium', 150000, 1, 150000),
(22, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),
(22, 13, 'Massage đầu vai gáy', 120000, 1, 120000),
-- BK20251006001
(23, 3, 'Cắt tóc VIP', 250000, 1, 250000),
-- BK20251007001
(24, 1, 'Cắt tóc Basic', 100000, 1, 100000),
(24, 11, 'Gội đầu thường', 50000, 1, 50000),
-- BK20251008001
(25, 8, 'Uốn xoăn Hàn Quốc', 400000, 1, 400000),
-- BK20251009001
(26, 1, 'Cắt tóc Basic', 100000, 1, 100000),
-- BK20251010001
(27, 5, 'Nhuộm toàn bộ', 300000, 1, 300000);

-- 11. Hóa đơn từ booking tháng 9
INSERT INTO hoa_don (ma_hoa_don, dat_lich_id, khach_hang_id, ten_khach_hang, so_dien_thoai_khach, nhan_vien_id, tam_tinh, tien_giam_gia, thanh_tien, phuong_thuc_thanh_toan, tien_khach_dua, tien_thua, nguoi_tao_id, ngay_thanh_toan) VALUES
('INV20250910001', 14, 11, 'Vũ Văn Giang', '0913333333', 2, 100000, 0, 100000, 'tien_mat', 100000, 0, 2, '2025-09-10 10:30:00'),
('INV20250912001', 15, 13, 'Bùi Văn Khải', '0915555555', 3, 250000, 0, 250000, 'chuyen_khoan', NULL, NULL, 3, '2025-09-12 15:45:00'),
('INV20250917001', 16, 12, 'Đỗ Thị Hoa', '0914444444', 4, 150000, 0, 150000, 'vi_dien_tu', NULL, NULL, 4, '2025-09-17 11:45:00'),
('INV20250919001', 17, 15, 'Trương Văn Minh', '0917777777', 2, 650000, 0, 650000, 'the', NULL, NULL, 2, '2025-09-19 18:40:00'),
('INV20250923001', 18, 14, 'Đinh Thị Lan', '0916666666', 5, 80000, 0, 80000, 'tien_mat', 100000, 20000, 5, '2025-09-23 14:25:00');

-- 12. Chi tiết hóa đơn tháng 9
INSERT INTO chi_tiet_hoa_don (hoa_don_id, dich_vu_id, ten_dich_vu, gia, so_luong, thanh_tien) VALUES
-- INV20250910001
(13, 1, 'Cắt tóc Basic', 100000, 1, 100000),
-- INV20250912001
(14, 3, 'Cắt tóc VIP', 250000, 1, 250000),
-- INV20250917001
(15, 2, 'Cắt tóc Premium', 150000, 1, 150000),
-- INV20250919001
(16, 3, 'Cắt tóc VIP', 250000, 1, 250000),
(16, 5, 'Nhuộm toàn bộ', 300000, 1, 300000),
(16, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),
-- INV20250923001
(17, 4, 'Cắt tóc trẻ em', 80000, 1, 80000);

-- 13. Thêm hóa đơn walk-in
INSERT INTO hoa_don (ma_hoa_don, dat_lich_id, khach_hang_id, ten_khach_hang, so_dien_thoai_khach, nhan_vien_id, tam_tinh, tien_giam_gia, thanh_tien, phuong_thuc_thanh_toan, tien_khach_dua, tien_thua, nguoi_tao_id, ngay_thanh_toan) VALUES
('INV20250911001', NULL, 11, 'Vũ Văn Giang', '0913333333', 3, 150000, 0, 150000, 'tien_mat', 200000, 50000, 3, '2025-09-11 17:00:00'),
('INV20250914001', NULL, 13, 'Bùi Văn Khải', '0915555555', 4, 200000, 0, 200000, 'chuyen_khoan', NULL, NULL, 4, '2025-09-14 19:30:00'),
('INV20250926001', NULL, NULL, 'Phạm Văn Tân', '0918888888', 2, 100000, 0, 100000, 'tien_mat', 100000, 0, 2, '2025-09-26 10:45:00'),
('INV20250929001', NULL, NULL, 'Lương Thị Uyên', '0919999999', 5, 250000, 0, 250000, 'vi_dien_tu', NULL, NULL, 5, '2025-09-29 16:20:00');

-- 14. Chi tiết hóa đơn walk-in
INSERT INTO chi_tiet_hoa_don (hoa_don_id, dich_vu_id, ten_dich_vu, gia, so_luong, thanh_tien) VALUES
-- INV20250911001
(18, 2, 'Cắt tóc Premium', 150000, 1, 150000),
-- INV20250914001
(19, 1, 'Cắt tóc Basic', 100000, 1, 100000),
(19, 12, 'Gội đầu dưỡng sinh', 100000, 1, 100000),
-- INV20250926001
(20, 1, 'Cắt tóc Basic', 100000, 1, 100000),
-- INV20250929001
(21, 3, 'Cắt tóc VIP', 250000, 1, 250000);

-- 15. Giao dịch điểm
INSERT INTO giao_dich_diem (khach_hang_id, diem, loai_giao_dich, mo_ta, dat_lich_id, hoa_don_id, ngay_tao) VALUES
-- Cộng điểm đăng ký mới
(11, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-09-05 10:00:00'),
(12, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-09-08 14:00:00'),
(13, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-08-20 09:30:00'),
(14, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-09-12 16:00:00'),
(15, 100, 'cong', 'Điểm thưởng đăng ký tài khoản mới', NULL, NULL, '2025-08-10 11:00:00'),

-- Cộng điểm từ booking tháng 8
(6, 100, 'cong', 'Cộng điểm từ đơn hàng BK20250805001', 10, 9, '2025-08-05 10:30:00'),
(8, 250, 'cong', 'Cộng điểm từ đơn hàng BK20250812001', 11, 10, '2025-08-12 15:50:00'),
(10, 370, 'cong', 'Cộng điểm từ đơn hàng BK20250820001', 12, 11, '2025-08-20 15:10:00'),
(13, 150, 'cong', 'Cộng điểm từ đơn hàng BK20250825001', 13, 12, '2025-08-25 10:15:00'),

-- Cộng điểm từ booking tháng 9
(11, 100, 'cong', 'Cộng điểm từ đơn hàng BK20250910001', 14, 13, '2025-09-10 10:30:00'),
(13, 250, 'cong', 'Cộng điểm từ đơn hàng BK20250912001', 15, 14, '2025-09-12 15:45:00'),
(12, 150, 'cong', 'Cộng điểm từ đơn hàng BK20250917001', 16, 15, '2025-09-17 11:45:00'),
(15, 650, 'cong', 'Cộng điểm từ đơn hàng BK20250919001', 17, 16, '2025-09-19 18:40:00'),
(14, 80, 'cong', 'Cộng điểm từ đơn hàng BK20250923001', 18, 17, '2025-09-23 14:25:00'),

-- Cộng điểm từ walk-in
(11, 150, 'cong', 'Cộng điểm từ hóa đơn INV20250911001', NULL, 18, '2025-09-11 17:00:00'),
(13, 200, 'cong', 'Cộng điểm từ hóa đơn INV20250914001', NULL, 19, '2025-09-14 19:30:00'),

-- Cộng điểm đánh giá
(11, 50, 'cong', 'Điểm thưởng viết đánh giá', 14, NULL, '2025-09-11 10:00:00'),
(13, 50, 'cong', 'Điểm thưởng viết đánh giá', 15, NULL, '2025-09-13 09:00:00'),
(15, 50, 'cong', 'Điểm thưởng viết đánh giá', 17, NULL, '2025-09-20 11:00:00'),

-- Trừ điểm đổi thưởng
(13, -500, 'doi_thuong', 'Đổi voucher 50K', NULL, NULL, '2025-09-15 10:30:00'),
(15, -1000, 'doi_thuong', 'Đổi voucher 100K', NULL, NULL, '2025-09-18 14:00:00');

-- 16. Đánh giá bổ sung
INSERT INTO danh_gia (dat_lich_id, khach_hang_id, nhan_vien_id, diem_nhan_vien, diem_dich_vu, diem_khong_gian, binh_luan, hien_thi_cong_khai, trang_thai, ngay_tao) VALUES
(14, 11, 2, 4, 4, 5, 'Dịch vụ tốt, cắt nhanh gọn. Không gian sạch sẽ, thoải mái.', TRUE, 'da_duyet', '2025-09-11 10:00:00'),
(15, 13, 3, 5, 5, 5, 'Anh Tuấn cắt rất đẹp, tư vấn nhiệt tình. Mình rất hài lòng, sẽ quay lại!', TRUE, 'da_duyet', '2025-09-13 09:00:00'),
(17, 15, 2, 5, 5, 5, 'Xuất sắc! Cả cắt và nhuộm đều hoàn hảo. Anh Hoàng rất chuyên nghiệp và chu đáo.', TRUE, 'da_duyet', '2025-09-20 11:00:00'),
(16, 12, 4, 4, 4, 4, 'Dịch vụ ổn, nhân viên thân thiện. Giá cả hợp lý.', TRUE, 'da_duyet', '2025-09-18 14:30:00');

-- 17. Ghi chú khách hàng bổ sung
INSERT INTO ghi_chu_khach_hang (nhan_vien_id, khach_hang_id, ghi_chu, dat_lich_id, ngay_tao) VALUES
(2, 11, 'Khách thích cắt tóc ngắn gọn, phong cách thể thao', 14, '2025-09-10 10:30:00'),
(3, 13, 'Khách VIP, thích kiểu tóc hiện đại, hay thử style mới', 15, '2025-09-12 15:45:00'),
(2, 15, 'Khách yêu cầu cao, cần tư vấn kỹ về màu nhuộm', 17, '2025-09-19 18:40:00'),
(4, 12, 'Khách ưa phong cách đơn giản, thanh lịch', 16, '2025-09-17 11:45:00');

-- 18. Lịch sử tóc bổ sung
INSERT INTO lich_su_toc (dat_lich_id, khach_hang_id, nhan_vien_id, anh_ket_qua, ghi_chu, nguoi_tao_id, ngay_tao) VALUES
(14, 11, 2, ARRAY['https://example.com/hair5.jpg'], 'Cắt undercut thể thao, ngắn gọn', 2, '2025-09-10 10:30:00'),
(15, 13, 3, ARRAY['https://example.com/hair6.jpg'], 'Cắt tóc VIP, side part hiện đại', 3, '2025-09-12 15:45:00'),
(16, 12, 4, ARRAY['https://example.com/hair7.jpg'], 'Cắt layer thanh lịch', 4, '2025-09-17 11:45:00'),
(17, 15, 2, ARRAY['https://example.com/hair8.jpg', 'https://example.com/hair8b.jpg'], 'Cắt + nhuộm màu xám khói, phong cách Hàn Quốc', 2, '2025-09-19 18:40:00');

-- 19. Stylist yêu thích bổ sung
INSERT INTO stylist_yeu_thich (khach_hang_id, nhan_vien_id, ngay_tao) VALUES
(11, 2, '2025-09-11 11:00:00'),
(13, 3, '2025-09-13 10:00:00'),
(15, 2, '2025-09-20 12:00:00'),
(12, 4, '2025-09-18 15:00:00');

-- 20. Voucher khách hàng bổ sung
INSERT INTO voucher_khach_hang (voucher_id, khach_hang_id, ma_voucher_ca_nhan, da_su_dung, ngay_het_han) VALUES
(1, 11, 'GIAM20K-KH006', TRUE, '2025-10-31'),
(2, 11, 'GIAM10-KH006', FALSE, '2025-10-31'),
(1, 12, 'GIAM20K-KH007', FALSE, '2025-10-31'),
(2, 13, 'GIAM10-KH008', FALSE, '2025-10-31'),
(4, 13, 'VIP100-KH008', TRUE, '2025-11-30'),
(5, 15, 'COMBO20-KH009', FALSE, '2025-10-15'),
(2, 15, 'GIAM10-KH009', TRUE, '2025-10-31'),
(3, 14, 'SINH_NHAT-KH010', FALSE, '2025-12-31');

-- 21. Thông báo bổ sung
INSERT INTO thong_bao (nguoi_dung_id, loai_thong_bao, tieu_de, noi_dung, da_doc, lien_ket, ngay_tao) VALUES
(11, 'xac_nhan_dat_lich', 'Đặt lịch thành công', 'Bạn đã đặt lịch thành công cho ngày 05/10/2025 lúc 10:00. Mã đặt lịch: BK20251005001', FALSE, '/customer/booking/21', '2025-10-01 15:00:00'),
(12, 'xac_nhan_dat_lich', 'Đặt lịch thành công', 'Bạn đã đặt lịch thành công cho ngày 05/10/2025 lúc 15:30. Mã đặt lịch: BK20251005002', TRUE, '/customer/booking/22', '2025-10-01 16:00:00'),
(13, 'cong_diem', 'Cộng điểm thành công', 'Bạn vừa được cộng 250 điểm từ đơn hàng BK20250912001. Tổng điểm hiện tại: 1850', TRUE, '/customer/rewards', '2025-09-12 15:45:00'),
(15, 'khuyen_mai', 'Chương trình ưu đãi tháng 10', 'Giảm giá 20% cho combo dịch vụ trong tháng 10. Đặt lịch ngay!', FALSE, '/promotions', '2025-10-01 09:00:00'),
(11, 'nhac_lich', 'Nhắc lịch hẹn', 'Bạn có lịch hẹn vào ngày mai 05/10/2025 lúc 10:00 tại Barbershop Hoàng Gia', FALSE, '/customer/booking/21', '2025-10-04 10:00:00'),
(14, 'sinh_nhat', 'Chúc mừng sinh nhật!', 'Chúc mừng sinh nhật bạn! Bạn đã nhận voucher sinh nhật trị giá 50K. Hãy đặt lịch để sử dụng nhé!', FALSE, '/customer/vouchers', '2025-01-30 00:00:00'),
(4, 'lich_lam_viec', 'Xác nhận lịch làm việc', 'Lịch làm việc tuần 08/10 - 14/10 đã được phê duyệt. Vui lòng kiểm tra.', FALSE, '/staff/schedule', '2025-10-01 08:00:00'),
(2, 'danh_gia_moi', 'Bạn có đánh giá mới', 'Khách hàng Trương Văn Minh vừa đánh giá 5 sao dịch vụ của bạn', TRUE, '/staff/reviews', '2025-09-20 11:00:00'),
(13, 'doi_thuong', 'Đổi điểm thành công', 'Bạn đã đổi 500 điểm lấy voucher 50K. Voucher có hiệu lực 30 ngày.', TRUE, '/customer/rewards', '2025-09-15 10:30:00'),
(7, 'nhac_lich', 'Nhắc lịch hẹn', 'Bạn có lịch hẹn vào ngày mai 07/10/2025 lúc 14:00 tại Barbershop Hoàng Gia', FALSE, '/customer/booking/24', '2025-10-06 14:00:00');

-- 22. Yêu cầu nghỉ phép bổ sung
INSERT INTO yeu_cau_nghi_phep (nhan_vien_id, ngay_bat_dau, ngay_ket_thuc, ly_do, trang_thai, nguoi_duyet_id, ghi_chu_duyet, ngay_duyet) VALUES
(2, '2025-10-25', '2025-10-27', 'Đám cưới bạn thân', 'cho_duyet', NULL, NULL, NULL),
(3, '2025-11-05', '2025-11-07', 'Nghỉ phép năm', 'cho_duyet', NULL, NULL, NULL),
(5, '2025-10-18', '2025-10-18', 'Khám bệnh', 'da_duyet', 1, 'Đã duyệt, nhớ mang giấy khám bệnh', '2025-10-10 10:00:00');

-- 23. Thêm combo dịch vụ mới
INSERT INTO combo_dich_vu (ten_combo, mo_ta, gia_goc, gia_combo, trang_thai) VALUES
('Combo Văn phòng', 'Cắt tóc Premium + Cạo mặt - Nhanh gọn cho dân văn phòng', 230000, 180000, TRUE),
('Combo Sinh viên', 'Cắt tóc Basic + Gội + Tạo kiểu', 200000, 150000, TRUE),
('Combo Lãng tử', 'Cắt VIP + Nhuộm Highlight + Chăm sóc da', 850000, 700000, TRUE);

-- 24. Chi tiết combo mới
INSERT INTO chi_tiet_combo (combo_id, dich_vu_id) VALUES
-- Combo Văn phòng (id=5)
(5, 2), (5, 14),
-- Combo Sinh viên (id=6)
(6, 1), (6, 11),
-- Combo Lãng tử (id=7)
(7, 3), (7, 6), (7, 17);

-- 25. Thêm voucher mới
INSERT INTO voucher (ma_voucher, ten_voucher, mo_ta, loai_giam, gia_tri_giam, gia_tri_don_toi_thieu, giam_toi_da, ngay_bat_dau, ngay_ket_thuc, so_luong_tong, so_luong_da_dung, ap_dung_cho, hien_thi_cong_khai) VALUES
('WEEKEND50', 'Giảm 50K cuối tuần', 'Voucher dành cho đơn hàng cuối tuần', 'tien_mat', 50000, 200000, 50000, '2025-10-05', '2025-10-31', 150, 0, 'tat_ca', TRUE),
('STUDENT20', 'Giảm 20% sinh viên', 'Ưu đãi đặc biệt cho sinh viên', 'phan_tram', 20, 100000, 40000, '2025-10-01', '2025-12-31', NULL, 0, 'tat_ca', TRUE),
('MEMBER30', 'Giảm 30K thành viên', 'Ưu đãi cho thành viên thân thiết', 'tien_mat', 30000, 150000, 30000, '2025-10-01', '2025-10-31', 200, 0, 'khach_cu', TRUE);

-- 26. Cập nhật thống kê nhân viên
UPDATE thong_tin_nhan_vien SET 
    tong_luot_phuc_vu = 535, 
    danh_gia_trung_binh = 4.8 
WHERE nguoi_dung_id = 2;

UPDATE thong_tin_nhan_vien SET 
    tong_luot_phuc_vu = 425, 
    danh_gia_trung_binh = 4.8 
WHERE nguoi_dung_id = 3;

UPDATE thong_tin_nhan_vien SET 
    tong_luot_phuc_vu = 298, 
    danh_gia_trung_binh = 4.5 
WHERE nguoi_dung_id = 4;

UPDATE thong_tin_nhan_vien SET 
    tong_luot_phuc_vu = 362, 
    danh_gia_trung_binh = 4.5 
WHERE nguoi_dung_id = 5;

-- 27. Cập nhật số lượng voucher đã sử dụng
UPDATE voucher SET so_luong_da_dung = 18 WHERE ma_voucher = 'GIAM20K';
UPDATE voucher SET so_luong_da_dung = 52 WHERE ma_voucher = 'GIAM10';
UPDATE voucher SET so_luong_da_dung = 10 WHERE ma_voucher = 'SINH_NHAT';
UPDATE voucher SET so_luong_da_dung = 15 WHERE ma_voucher = 'VIP100';
UPDATE voucher SET so_luong_da_dung = 28 WHERE ma_voucher = 'COMBO20';

-- =============================================
-- QUERY MẪU ĐỂ KIỂM TRA DỮ LIỆU
-- =============================================

-- 1. Kiểm tra tổng số người dùng theo vai trò
SELECT 
    vai_tro,
    COUNT(*) as so_luong
FROM nguoi_dung 
WHERE da_xoa = FALSE
GROUP BY vai_tro;

-- 2. Kiểm tra tổng doanh thu theo tháng
SELECT 
    TO_CHAR(ngay_thanh_toan, 'YYYY-MM') as thang,
    COUNT(*) as so_hoa_don,
    SUM(thanh_tien) as tong_doanh_thu,
    ROUND(AVG(thanh_tien), 0) as trung_binh_hoa_don
FROM hoa_don 
WHERE da_xoa = FALSE
GROUP BY TO_CHAR(ngay_thanh_toan, 'YYYY-MM')
ORDER BY thang DESC;

-- 3. Top 10 khách hàng theo điểm tích lũy
SELECT 
    ho_ten, 
    so_dien_thoai, 
    email,
    diem_tich_luy 
FROM nguoi_dung 
WHERE vai_tro = 'khach_hang' AND da_xoa = FALSE
ORDER BY diem_tich_luy DESC 
LIMIT 10;

-- 4. Thống kê đánh giá theo nhân viên
SELECT 
    nd.ho_ten,
    COUNT(dg.id) as so_danh_gia,
    ROUND(AVG(dg.diem_nhan_vien), 1) as diem_tb_nhan_vien,
    ROUND(AVG(dg.diem_dich_vu), 1) as diem_tb_dich_vu,
    ROUND(AVG(dg.diem_khong_gian), 1) as diem_tb_khong_gian
FROM nguoi_dung nd
LEFT JOIN danh_gia dg ON nd.id = dg.nhan_vien_id AND dg.da_xoa = FALSE
WHERE nd.vai_tro = 'nhan_vien' AND nd.da_xoa = FALSE
GROUP BY nd.id, nd.ho_ten
ORDER BY diem_tb_nhan_vien DESC;

-- 5. Thống kê dịch vụ phổ biến
SELECT 
    dv.ten_dich_vu,
    dm.ten_danh_muc,
    COUNT(cthd.id) as so_lan_su_dung,
    SUM(cthd.thanh_tien) as tong_doanh_thu
FROM dich_vu dv
LEFT JOIN danh_muc_dich_vu dm ON dv.danh_muc_id = dm.id
LEFT JOIN chi_tiet_hoa_don cthd ON dv.id = cthd.dich_vu_id
WHERE dv.da_xoa = FALSE
GROUP BY dv.id, dv.ten_dich_vu, dm.ten_danh_muc
ORDER BY so_lan_su_dung DESC
LIMIT 10;

-- 6. Thống kê booking theo trạng thái
SELECT 
    trang_thai,
    COUNT(*) as so_luong,
    SUM(thanh_tien) as tong_tien
FROM dat_lich
WHERE da_xoa = FALSE
GROUP BY trang_thai
ORDER BY so_luong DESC;

-- 7. Doanh thu theo nhân viên (tháng 9/2025)
SELECT 
    nd.ho_ten,
    COUNT(hd.id) as so_hoa_don,
    SUM(hd.thanh_tien) as tong_doanh_thu
FROM nguoi_dung nd
LEFT JOIN hoa_don hd ON nd.id = hd.nhan_vien_id 
    AND hd.da_xoa = FALSE
    AND DATE_TRUNC('month', hd.ngay_thanh_toan) = '2025-09-01'
WHERE nd.vai_tro = 'nhan_vien' AND nd.da_xoa = FALSE
GROUP BY nd.id, nd.ho_ten
ORDER BY tong_doanh_thu DESC;

-- 8. Kiểm tra voucher còn hiệu lực
SELECT 
    ma_voucher,
    ten_voucher,
    loai_giam,
    gia_tri_giam,
    ngay_bat_dau,
    ngay_ket_thuc,
    so_luong_tong,
    so_luong_da_dung,
    CASE 
        WHEN so_luong_tong IS NULL THEN 'Không giới hạn'
        ELSE (so_luong_tong - so_luong_da_dung)::TEXT
    END as con_lai
FROM voucher
WHERE da_xoa = FALSE 
    AND trang_thai = TRUE
    AND ngay_ket_thuc >= CURRENT_DATE
ORDER BY ngay_ket_thuc;

-- =============================================
-- KẾT THÚC DỮ LIỆU MẪU BỔ SUNG
-- =============================================