# -*- coding: utf-8 -*-
template_content = """{% extends 'base.html' %}
{% load static %}

{% block title %}Chỉnh sửa nhân viên - Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2><i class="fas fa-user-edit me-2"></i>Chỉnh sửa nhân viên</h2>
        </div>
    </div>

    <div class="row">
        <div class="col-md-8 offset-md-2">
            <div class="card">
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Họ tên *</label>
                                <input type="text" class="form-control" name="ho_ten" value="{{ staff.ho_ten }}" required>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Số điện thoại *</label>
                                <input type="tel" class="form-control" name="so_dien_thoai" value="{{ staff.so_dien_thoai }}" required>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" name="email" value="{{ staff.email|default:'' }}">
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Địa chỉ</label>
                                <input type="text" class="form-control" name="dia_chi" value="{{ staff.dia_chi|default:'' }}">
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Ngày sinh</label>
                                <input type="date" class="form-control" name="ngay_sinh" value="{% if staff_info and staff_info.ngay_sinh %}{{ staff_info.ngay_sinh|date:'Y-m-d' }}{% endif %}">
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Giới tính</label>
                                <select class="form-select" name="gioi_tinh">
                                    <option value="">-- Chọn --</option>
                                    <option value="nam" {% if staff_info and staff_info.gioi_tinh == 'nam' %}selected{% endif %}>Nam</option>
                                    <option value="nu" {% if staff_info and staff_info.gioi_tinh == 'nu' %}selected{% endif %}>Nữ</option>
                                    <option value="khac" {% if staff_info and staff_info.gioi_tinh == 'khac' %}selected{% endif %}>Khác</option>
                                </select>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">CCCD</label>
                                <input type="text" class="form-control" name="cccd" value="{% if staff_info %}{{ staff_info.cccd|default:'' }}{% endif %}">
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Trạng thái</label>
                                <div class="form-check form-switch mt-2">
                                    <input class="form-check-input" type="checkbox" id="trangThaiSwitch" name="trang_thai" {% if staff.trang_thai %}checked{% endif %}>
                                    <label class="form-check-label" for="trangThaiSwitch">Đang làm việc</label>
                                </div>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Kinh nghiệm (năm)</label>
                                <input type="number" class="form-control" name="kinh_nghiem_nam" value="{% if staff_info %}{{ staff_info.kinh_nghiem_nam|default:'0' }}{% else %}0{% endif %}" min="0">
                            </div>
                            
                            <div class="col-12 mb-3">
                                <label class="form-label">Chuyên môn</label>
                                <textarea class="form-control" name="chuyen_mon" rows="2" placeholder="Ví dụ: Cắt tóc, Nhuộm tóc, Uốn tóc">{% if staff_info %}{{ staff_info.chuyen_mon|default:'' }}{% endif %}</textarea>
                                <small class="text-muted">Ngăn cách bằng dấu phẩy</small>
                            </div>
                            
                            <div class="col-12 mb-3">
                                <label class="form-label">Chứng chỉ</label>
                                <input type="text" class="form-control" name="chung_chi" value="{% if staff_info %}{{ staff_info.chung_chi|default:'' }}{% endif %}" placeholder="Các chứng chỉ nghề nghiệp">
                            </div>
                            
                            <div class="col-12 mb-3">
                                <label class="form-label">Mô tả</label>
                                <textarea class="form-control" name="mo_ta" rows="3" placeholder="Thông tin thêm về nhân viên">{% if staff_info %}{{ staff_info.mo_ta|default:'' }}{% endif %}</textarea>
                            </div>
                        </div>
                        
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'admin_staff_detail' staff.id %}" class="btn btn-secondary">
                                <i class="fas fa-times me-1"></i> Hủy
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-1"></i> Lưu thay đổi
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

with open(r'd:\Project\WebsiteHotTocNam\templates\admin\staff-edit.html', 'w', encoding='utf-8') as f:
    f.write(template_content)

print("File created successfully!")
