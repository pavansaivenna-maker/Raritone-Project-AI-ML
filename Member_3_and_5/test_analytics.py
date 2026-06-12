import requests

def run_analytics_tests():
    base_url = "http://127.0.0.1:8000"
    print("--- FASHION-AI ANALYTICS TESTING REPORT ---")

    # 1. Test Try-On Logging
    print("\n1. Testing Try-On Logging Endpoint...")
    try_payload = {
        "user_id": "usr_101",
        "garment_id": "grm_005",
        "processing_time_ms": 420,
        "success": True
    }
    r1 = requests.post(f"{base_url}/api/v1/analytics/try-on", json=try_payload)
    print(f"Status Code: {r1.status_code} | Response: {r1.json()}")

    # 2. Test Conversion Logging
    print("\n2. Testing Conversion Logging Endpoint...")
    conv_payload = {
        "user_id": "usr_101",
        "garment_id": "grm_005",
        "added_to_cart": True
    }
    r2 = requests.post(f"{base_url}/api/v1/analytics/conversion", json=conv_payload)
    print(f"Status Code: {r2.status_code} | Response: {r2.json()}")

    # 3. Test Dashboard Aggregation
    print("\n3. Testing Dashboard Aggregation Endpoint...")
    r3 = requests.get(f"{base_url}/api/v1/analytics/dashboard")
    print(f"Status Code: {r3.status_code} | Response: {r3.json()}")
    print("\n--- END OF REPORT ---")

if __name__ == "__main__":
    run_analytics_tests()