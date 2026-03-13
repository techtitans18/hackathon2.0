"""
Test Patient Access OTP with All Search Options
Tests Health ID, Mobile Number, and Email Address search
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_all_search_options():
    print("=" * 70)
    print("Testing Patient Access OTP - All Search Options")
    print("=" * 70)
    
    hospital_token = "YOUR_HOSPITAL_TOKEN_HERE"
    
    # Test data - update with actual patient data
    test_cases = [
        {
            "name": "Health ID Search",
            "search_type": "health_id",
            "search_value": "PATIENT_HEALTH_ID_HERE"
        },
        {
            "name": "Mobile Number Search",
            "search_type": "mobile",
            "search_value": "+1234567890"
        },
        {
            "name": "Email Address Search",
            "search_type": "email",
            "search_value": "patient@example.com"
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {hospital_token}",
        "Content-Type": "application/json"
    }
    
    for test_case in test_cases:
        print(f"\n{'='*70}")
        print(f"Test: {test_case['name']}")
        print(f"{'='*70}")
        
        # Send OTP
        print(f"\n1. Sending OTP via {test_case['search_type']}...")
        send_payload = {
            "search_type": test_case["search_type"],
            "search_value": test_case["search_value"]
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/patient_access/send_otp",
                json=send_payload,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ OTP sent to: {data['email_masked']}")
                print(f"  Expires in: {data['expires_in_minutes']} minutes")
                print("\n  Check server console for OTP")
            else:
                print(f"✗ Failed: {response.json()}")
                
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n{'='*70}")
    print("Test Summary")
    print(f"{'='*70}")
    print("\nAll three search options tested:")
    print("  1. Health ID - Direct patient identifier")
    print("  2. Mobile Number - Phone-based lookup")
    print("  3. Email Address - Email-based lookup")
    print("\nNext steps:")
    print("  1. Update test_cases with actual patient data")
    print("  2. Add valid hospital token")
    print("  3. Run test and verify OTPs in console")
    print("  4. Test verification with actual OTP codes")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SETUP REQUIRED:")
    print("="*70)
    print("1. Update hospital_token with valid JWT token")
    print("2. Update test_cases with actual patient data:")
    print("   - Valid Health ID")
    print("   - Valid Mobile Number")
    print("   - Valid Email Address")
    print("3. Ensure patient is registered with your hospital")
    print("4. Start server: python -m uvicorn main:app --reload")
    print("="*70)
    
    # Uncomment to run test
    # test_all_search_options()
