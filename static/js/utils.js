/**
 * BARBERSHOP UTILITIES
 * JavaScript utilities and helper functions
 * Hot Tóc Nam - 2025
 */

// ============ CURRENCY FORMATTER ============
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('vi-VN').format(number);
}

// ============ DATE FORMATTER ============
function formatDate(date, format = 'dd/mm/yyyy') {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    
    if (format === 'dd/mm/yyyy') {
        return `${day}/${month}/${year}`;
    } else if (format === 'yyyy-mm-dd') {
        return `${year}-${month}-${day}`;
    }
    return date;
}

function formatDateTime(datetime) {
    const d = new Date(datetime);
    return `${formatDate(d)} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}

// ============ VALIDATION ============
function validatePhone(phone) {
    const phoneRegex = /(84|0[3|5|7|8|9])+([0-9]{8})\b/;
    return phoneRegex.test(phone);
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ============ NOTIFICATIONS ============
function showNotification(message, type = 'info') {
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    
    const notification = $(`
        <div class="alert alert-${type} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    $('body').append(notification);
    
    setTimeout(() => {
        notification.fadeOut(() => notification.remove());
    }, 5000);
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showWarning(message) {
    showNotification(message, 'warning');
}

function showInfo(message) {
    showNotification(message, 'info');
}

// ============ CONFIRM DIALOG ============
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

function confirmDelete(itemName, callback) {
    const message = `Bạn có chắc muốn xóa ${itemName}?`;
    confirmAction(message, callback);
}

// ============ LOADING OVERLAY ============
function showLoading() {
    const overlay = $(`
        <div class="loading-overlay">
            <div class="spinner-border text-light" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `);
    $('body').append(overlay);
}

function hideLoading() {
    $('.loading-overlay').fadeOut(() => $('.loading-overlay').remove());
}

// ============ AJAX HELPERS ============
function ajaxGet(url, successCallback, errorCallback) {
    showLoading();
    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            hideLoading();
            if (successCallback) successCallback(response);
        },
        error: function(xhr, status, error) {
            hideLoading();
            showError('Có lỗi xảy ra: ' + error);
            if (errorCallback) errorCallback(xhr, status, error);
        }
    });
}

function ajaxPost(url, data, successCallback, errorCallback) {
    showLoading();
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        success: function(response) {
            hideLoading();
            if (successCallback) successCallback(response);
        },
        error: function(xhr, status, error) {
            hideLoading();
            showError('Có lỗi xảy ra: ' + error);
            if (errorCallback) errorCallback(xhr, status, error);
        }
    });
}

// ============ TABLE UTILITIES ============
function initDataTable(tableId, options = {}) {
    const defaultOptions = {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/vi.json'
        },
        pageLength: 10,
        responsive: true,
        ...options
    };
    
    return $(`#${tableId}`).DataTable(defaultOptions);
}

function exportToExcel(tableId, filename = 'export') {
    const table = document.getElementById(tableId);
    const wb = XLSX.utils.table_to_book(table);
    XLSX.writeFile(wb, `${filename}_${formatDate(new Date(), 'yyyy-mm-dd')}.xlsx`);
}

// ============ CHART HELPERS ============
function createLineChart(ctx, labels, data, label = 'Dữ liệu') {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: '#8b4513',
                backgroundColor: 'rgba(139, 69, 19, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function createBarChart(ctx, labels, data, label = 'Dữ liệu') {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(139, 69, 19, 0.7)',
                borderColor: '#8b4513',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function createPieChart(ctx, labels, data) {
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#8b4513',
                    '#d2691e',
                    '#ffc107',
                    '#28a745',
                    '#17a2b8'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// ============ LOCAL STORAGE ============
function saveToLocalStorage(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function getFromLocalStorage(key) {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : null;
}

function removeFromLocalStorage(key) {
    localStorage.removeItem(key);
}

// ============ FORM HELPERS ============
function serializeFormData(formId) {
    const form = $(`#${formId}`);
    const data = {};
    
    form.serializeArray().forEach(item => {
        data[item.name] = item.value;
    });
    
    return data;
}

function resetForm(formId) {
    $(`#${formId}`)[0].reset();
}

function fillForm(formId, data) {
    const form = $(`#${formId}`);
    
    Object.keys(data).forEach(key => {
        const input = form.find(`[name="${key}"]`);
        if (input.length) {
            input.val(data[key]);
        }
    });
}

// ============ DEBOUNCE ============
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ============ PRINT ============
function printElement(elementId) {
    const element = document.getElementById(elementId);
    const printWindow = window.open('', '', 'height=600,width=800');
    
    printWindow.document.write('<html><head><title>Print</title>');
    printWindow.document.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(element.innerHTML);
    printWindow.document.write('</body></html>');
    
    printWindow.document.close();
    printWindow.print();
}

// ============ COPY TO CLIPBOARD ============
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Đã sao chép vào clipboard!');
    }).catch(err => {
        showError('Không thể sao chép: ' + err);
    });
}

// ============ AUTO INITIALIZE ============
$(document).ready(function() {
    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Initialize popovers
    $('[data-bs-toggle="popover"]').popover();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert:not(.alert-permanent)').fadeOut();
    }, 5000);
    
    // Confirm delete links
    $('.delete-confirm').click(function(e) {
        if (!confirm('Bạn có chắc muốn xóa?')) {
            e.preventDefault();
        }
    });
    
    // Number input validation
    $('input[type="number"]').on('input', function() {
        if (this.value < 0) this.value = 0;
    });
    
    // Phone number formatting
    $('input[type="tel"]').on('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
    });
});

// Export functions for use in other scripts
window.BarbershopUtils = {
    formatCurrency,
    formatNumber,
    formatDate,
    formatDateTime,
    validatePhone,
    validateEmail,
    showNotification,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    confirmAction,
    confirmDelete,
    showLoading,
    hideLoading,
    ajaxGet,
    ajaxPost,
    initDataTable,
    exportToExcel,
    createLineChart,
    createBarChart,
    createPieChart,
    saveToLocalStorage,
    getFromLocalStorage,
    removeFromLocalStorage,
    serializeFormData,
    resetForm,
    fillForm,
    debounce,
    printElement,
    copyToClipboard
};
