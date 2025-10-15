/**
 * Customer JavaScript
 * Barbershop Website
 */

$(document).ready(function() {
    console.log('Customer JS loaded');
    
    // ===================================
    // SMOOTH SCROLL
    // ===================================
    $('a[href^="#"]').on('click', function(e) {
        const target = $(this.getAttribute('href'));
        if (target.length) {
            e.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 80
            }, 800);
        }
    });
    
    // ===================================
    // NAVBAR SCROLL EFFECT
    // ===================================
    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('.navbar').addClass('scrolled');
        } else {
            $('.navbar').removeClass('scrolled');
        }
    });
    
    // ===================================
    // SERVICE SELECTION (BOOKING)
    // ===================================
    $('.service-option').click(function() {
        const checkbox = $(this).find('input[type="checkbox"]');
        checkbox.prop('checked', !checkbox.prop('checked'));
        $(this).toggleClass('selected');
        updateBookingSummary();
    });
    
    // ===================================
    // TIME SLOT SELECTION
    // ===================================
    $('.time-slot').click(function() {
        if (!$(this).hasClass('disabled')) {
            $('.time-slot').removeClass('selected');
            $(this).addClass('selected');
            $('#selected_time').val($(this).data('time'));
        }
    });
    
    // ===================================
    // BOOKING SUMMARY UPDATE
    // ===================================
    function updateBookingSummary() {
        let totalPrice = 0;
        let totalDuration = 0;
        let services = [];
        
        $('.service-option.selected').each(function() {
            const price = parseFloat($(this).data('price'));
            const duration = parseInt($(this).data('duration'));
            const name = $(this).find('.service-option-name').text();
            
            totalPrice += price;
            totalDuration += duration;
            services.push(name);
        });
        
        $('#total-price').text(formatMoney(totalPrice));
        $('#total-duration').text(totalDuration + ' phút');
        $('#selected-services-list').text(services.join(', '));
        
        // Enable/disable next button
        if (services.length > 0) {
            $('#btn-next-step').prop('disabled', false);
        } else {
            $('#btn-next-step').prop('disabled', true);
        }
    }
    
    // ===================================
    // VOUCHER SELECTION
    // ===================================
    $('.voucher-select-btn').click(function() {
        const voucherCode = $(this).data('code');
        const discountValue = $(this).data('value');
        const discountType = $(this).data('type');
        
        $('#selected_voucher').val(voucherCode);
        $('.voucher-card').removeClass('selected');
        $(this).closest('.voucher-card').addClass('selected');
        
        calculateDiscount(discountValue, discountType);
    });
    
    // ===================================
    // CALCULATE DISCOUNT
    // ===================================
    function calculateDiscount(value, type) {
        const subtotal = parseFloat($('#subtotal').text().replace(/[,.]/g, ''));
        let discount = 0;
        
        if (type === 'phan_tram') {
            discount = (subtotal * value) / 100;
            const maxDiscount = parseFloat($('#max-discount').val());
            if (maxDiscount && discount > maxDiscount) {
                discount = maxDiscount;
            }
        } else {
            discount = value;
        }
        
        const finalPrice = subtotal - discount;
        
        $('#discount-amount').text(formatMoney(discount));
        $('#final-price').text(formatMoney(finalPrice));
    }
    
    // ===================================
    // POINTS REDEMPTION
    // ===================================
    $('#use-points-btn').click(function() {
        const availablePoints = parseInt($('#available-points').text());
        const pointsToUse = parseInt($('#points-to-use').val());
        const pointsValue = 1000; // 1 point = 1000 VND
        
        if (pointsToUse > availablePoints) {
            showAlert('Bạn không đủ điểm!', 'warning');
            return;
        }
        
        const discount = pointsToUse * pointsValue;
        const currentDiscount = parseFloat($('#discount-amount').text().replace(/[,.]/g, '')) || 0;
        const totalDiscount = currentDiscount + discount;
        
        $('#discount-amount').text(formatMoney(totalDiscount));
        
        const subtotal = parseFloat($('#subtotal').text().replace(/[,.]/g, ''));
        const finalPrice = subtotal - totalDiscount;
        $('#final-price').text(formatMoney(finalPrice));
    });
    
    // ===================================
    // CANCEL BOOKING
    // ===================================
    $('.cancel-booking-btn').click(function() {
        const bookingId = $(this).data('booking-id');
        const bookingCode = $(this).data('booking-code');
        
        if (confirm(`Bạn có chắc muốn hủy lịch hẹn ${bookingCode}?`)) {
            // Show cancel reason modal
            $('#cancelBookingModal').modal('show');
            $('#confirm-cancel-btn').data('booking-id', bookingId);
        }
    });
    
    $('#confirm-cancel-btn').click(function() {
        const bookingId = $(this).data('booking-id');
        const cancelReason = $('#cancel-reason').val();
        
        if (!cancelReason) {
            showAlert('Vui lòng chọn lý do hủy', 'warning');
            return;
        }
        
        $.ajax({
            url: `/customer/booking/${bookingId}/cancel/`,
            method: 'POST',
            data: {
                'reason': cancelReason,
                'csrfmiddlewaretoken': getCsrfToken()
            },
            success: function(response) {
                showAlert('Đã hủy lịch hẹn thành công', 'success');
                $('#cancelBookingModal').modal('hide');
                location.reload();
            },
            error: function() {
                showAlert('Có lỗi xảy ra. Vui lòng thử lại', 'danger');
            }
        });
    });
    
    // ===================================
    // FAVORITE STYLIST TOGGLE
    // ===================================
    $('.favorite-stylist-btn').click(function() {
        const stylistId = $(this).data('stylist-id');
        const button = $(this);
        
        $.ajax({
            url: '/customer/toggle-favorite-stylist/',
            method: 'POST',
            data: {
                'stylist_id': stylistId,
                'csrfmiddlewaretoken': getCsrfToken()
            },
            success: function(response) {
                if (response.is_favorite) {
                    button.html('<i class="fas fa-heart"></i> Đã yêu thích');
                    button.removeClass('btn-outline-danger').addClass('btn-danger');
                } else {
                    button.html('<i class="far fa-heart"></i> Yêu thích');
                    button.removeClass('btn-danger').addClass('btn-outline-danger');
                }
            }
        });
    });
    
    // ===================================
    // REVIEW FORM - STAR RATING
    // ===================================
    $('.star-rating i').click(function() {
        const rating = $(this).data('rating');
        const category = $(this).closest('.star-rating').data('category');
        
        // Update stars
        $(this).closest('.star-rating').find('i').each(function(index) {
            if (index < rating) {
                $(this).removeClass('far').addClass('fas');
            } else {
                $(this).removeClass('fas').addClass('far');
            }
        });
        
        // Update hidden input
        $(`#${category}-rating`).val(rating);
    });
    
    // ===================================
    // REDEEM POINTS FOR VOUCHER
    // ===================================
    $('.redeem-btn').click(function() {
        const rewardId = $(this).data('reward-id');
        const pointsRequired = $(this).data('points-required');
        const availablePoints = parseInt($('#user-points').text());
        
        if (availablePoints < pointsRequired) {
            showAlert('Bạn không đủ điểm để đổi phần thưởng này!', 'warning');
            return;
        }
        
        if (confirm(`Bạn có chắc muốn đổi ${pointsRequired} điểm?`)) {
            $.ajax({
                url: '/customer/redeem-reward/',
                method: 'POST',
                data: {
                    'reward_id': rewardId,
                    'csrfmiddlewaretoken': getCsrfToken()
                },
                success: function(response) {
                    showAlert('Đã đổi thành công! Voucher đã được thêm vào tài khoản', 'success');
                    setTimeout(() => location.reload(), 1500);
                },
                error: function(xhr) {
                    const error = xhr.responseJSON?.error || 'Có lỗi xảy ra';
                    showAlert(error, 'danger');
                }
            });
        }
    });
    
    // ===================================
    // FORM VALIDATION
    // ===================================
    $('form.needs-validation').submit(function(e) {
        if (!this.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        $(this).addClass('was-validated');
    });
    
    // ===================================
    // DATE PICKER CONFIGURATION
    // ===================================
    if ($('#booking-date').length) {
        $('#booking-date').attr('min', new Date().toISOString().split('T')[0]);
        
        // Calculate max date (30 days from now)
        const maxDate = new Date();
        maxDate.setDate(maxDate.getDate() + 30);
        $('#booking-date').attr('max', maxDate.toISOString().split('T')[0]);
    }
    
    // ===================================
    // LOAD TIME SLOTS WHEN DATE SELECTED
    // ===================================
    $('#booking-date, #stylist-select').change(function() {
        const date = $('#booking-date').val();
        const stylistId = $('#stylist-select').val();
        const duration = $('#total-duration').val();
        
        if (date) {
            loadAvailableTimeSlots(date, stylistId, duration);
        }
    });
    
    // ===================================
    // AJAX LOAD TIME SLOTS
    // ===================================
    function loadAvailableTimeSlots(date, stylistId, duration) {
        $('#time-slots-container').html('<div class="loading-spinner"></div>');
        
        $.ajax({
            url: '/booking/get-available-slots/',
            method: 'GET',
            data: {
                'date': date,
                'stylist_id': stylistId,
                'duration': duration
            },
            success: function(response) {
                let slotsHtml = '<div class="time-slots-grid">';
                
                response.slots.forEach(slot => {
                    const disabledClass = slot.available ? '' : 'disabled';
                    slotsHtml += `
                        <div class="time-slot ${disabledClass}" data-time="${slot.time}">
                            <div class="time-text">${slot.time}</div>
                        </div>
                    `;
                });
                
                slotsHtml += '</div>';
                $('#time-slots-container').html(slotsHtml);
                
                // Re-attach click event
                $('.time-slot').click(function() {
                    if (!$(this).hasClass('disabled')) {
                        $('.time-slot').removeClass('selected');
                        $(this).addClass('selected');
                        $('#selected_time').val($(this).data('time'));
                    }
                });
            },
            error: function() {
                showAlert('Không thể tải lịch trống. Vui lòng thử lại', 'danger');
            }
        });
    }
    
    // ===================================
    // UTILITY FUNCTIONS
    // ===================================
    
    function formatMoney(amount) {
        return new Intl.NumberFormat('vi-VN').format(amount) + 'đ';
    }
    
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    
    function showAlert(message, type = 'info') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        $('#alert-container').html(alertHtml);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            $('.alert').fadeOut();
        }, 5000);
    }
    
    // ===================================
    // TOOLTIPS & POPOVERS
    // ===================================
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});
