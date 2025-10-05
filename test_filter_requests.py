"""
Test filter functionality thông qua HTTP request
"""
import requests
from datetime import date

# Test URL
base_url = "http://127.0.0.1:8000/admin/bookings/"

def test_filter_requests():
    """Test các request filter khác nhau"""
    print("=== TESTING FILTER VIA HTTP ===")
    
    # Test 1: No filter
    print("\n1. Testing no filter...")
    response = requests.get(base_url)
    print(f"Status: {response.status_code}")
    if "Không có lịch hẹn nào" in response.text:
        print("Result: No bookings found")
    else:
        # Count booking rows
        booking_count = response.text.count('<tr data-status=')
        print(f"Result: {booking_count} bookings found")
    
    # Test 2: Date filter
    print("\n2. Testing date filter (October 2025)...")
    params = {
        'from_date': '2025-10-01',
        'to_date': '2025-10-31'
    }
    response = requests.get(base_url, params=params)
    print(f"Status: {response.status_code}")
    if "Không có lịch hẹn nào" in response.text:
        print("Result: No bookings found")
    elif "Bộ lọc đang áp dụng" in response.text:
        booking_count = response.text.count('<tr data-status=')
        print(f"Result: {booking_count} bookings found with filter applied")
    else:
        booking_count = response.text.count('<tr data-status=')
        print(f"Result: {booking_count} bookings found")
    
    # Test 3: Search filter
    print("\n3. Testing search filter...")
    params = {
        'search': 'BK'
    }
    response = requests.get(base_url, params=params)
    print(f"Status: {response.status_code}")
    booking_count = response.text.count('<tr data-status=')
    print(f"Result: {booking_count} bookings found with search 'BK'")
    
    # Test 4: Combined filter
    print("\n4. Testing combined filter...")
    params = {
        'from_date': '2025-09-01',
        'to_date': '2025-12-31',
        'search': 'Nguyễn'
    }
    response = requests.get(base_url, params=params)
    print(f"Status: {response.status_code}")
    booking_count = response.text.count('<tr data-status=')
    print(f"Result: {booking_count} bookings found with combined filter")

if __name__ == '__main__':
    try:
        test_filter_requests()
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Django server. Make sure server is running at http://127.0.0.1:8000/")