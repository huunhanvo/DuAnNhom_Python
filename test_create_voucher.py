import urllib.request
import urllib.parse
import http.cookiejar
import json

# Tạo cookie jar để maintain session
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

def get_csrf_token():
    """Get CSRF token from the page"""
    response = opener.open('http://127.0.0.1:8000/test/promotions/')
    html = response.read().decode('utf-8')
    
    # Find CSRF token in HTML
    import re
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]*)"', html)
    if csrf_match:
        return csrf_match.group(1)
    return None

def test_create_voucher():
    """Test creating a new voucher"""
    csrf_token = get_csrf_token()
    if not csrf_token:
        print("Could not get CSRF token")
        return
    
    print(f"Got CSRF token: {csrf_token}")
    
    # Test data
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'voucher_id': '',  # Empty for new voucher
        'ma_voucher': 'UNIQUE2025',
        'ten_voucher': 'Test Voucher 2025',
        'mo_ta': 'Test voucher tạo qua script',
        'loai_giam': 'phan_tram',
        'gia_tri_giam': '25',
        'gia_tri_don_hang_toi_thieu': '50000',
        'gia_tri_giam_toi_da': '100000',
        'ngay_bat_dau': '2025-01-01T09:00',
        'ngay_ket_thuc': '2025-12-31T23:59',
        'so_luong_toi_da': '50',
        'trang_thai': 'active',
    }
    
    # Encode data
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    
    # Create request
    request = urllib.request.Request(
        'http://127.0.0.1:8000/test/promotions/',
        data=encoded_data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://127.0.0.1:8000/test/promotions/',
        }
    )
    
    try:
        response = opener.open(request)
        print(f"POST response status: {response.status}")
        print(f"POST response URL: {response.url}")
        
        if response.status == 200:
            print("Form submitted successfully!")
        else:
            print(f"Unexpected status: {response.status}")
            
    except Exception as e:
        print(f"Error submitting form: {e}")

if __name__ == "__main__":
    print("Starting voucher creation test...")
    test_create_voucher()
    print("Test completed.")