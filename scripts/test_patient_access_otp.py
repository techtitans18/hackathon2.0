"""
Test Patient Access OTP Feature
Run this after starting the server to test the OTP flow
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_patient_access_otp():
    print("=" * 60)
    print("Testing Patient Access OTP Feature")
    print("=" * 60)
    
    # Note: You need to:
    # 1. Have a hospital user logged in
    # 2. Have a patient registered with that hospital
    # 3. Replace the token and search values below
    
    hospital_token = "YOUR_HOSPITAL_TOKEN_HERE"
    patient_health_id = "PATIENT_HEALTH_ID_HERE"
    
    headers = {
        "Authorization": f"Bearer {hospital_token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Send OTP
    print("\n1. Sending OTP...")
    send_payload = {
        "search_type": "health_id",
        "search_value": patient_health_id
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/patient_access/send_otp",
            json=send_payload,
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✓ OTP sent successfully!")
            print("Check server console for OTP (in development mode)")
            
            # Test 2: Verify OTP
            otp = input("\nEnter the OTP from server console: ")
            
            print("\n2. Verifying OTP...")
            verify_payload = {
                "search_type": "health_id",
                "search_value": patient_health_id,
                "otp": otp
            }
            
            response = requests.post(
                f"{BASE_URL}/patient_access/verify_otp",
                json=verify_payload,
                headers=headers
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("\n✓ OTP verified successfully!")
                print(f"\nPatient: {data['patient']['name']}")
                print(f"Health ID: {data['patient']['health_id']}")
                print(f"Records: {len(data['records'])} found")
            else:
                print(f"\n✗ Verification failed: {response.json()}")
        else:
            print(f"\n✗ Failed to send OTP: {response.json()}")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("\nIMPORTANT: Update the script with:")
    print("1. Valid hospital token (from localStorage after login)")
    print("2. Valid patient Health ID")
    print("\nThen run: python test_patient_access_otp.py")
    print("\n" + "=" * 60)
    
    # Uncomment to run test
    # test_patient_access_otp()
