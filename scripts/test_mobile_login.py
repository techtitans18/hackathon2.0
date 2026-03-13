"""
Test mobile app login and patient/me endpoint
"""
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_login():
    """Test login endpoint"""
    print("Testing login...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "test@patient.com",
            "password": "password123"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful!")
        print(f"   Token: {data.get('access_token', '')[:50]}...")
        print(f"   User: {data.get('user', {}).get('name')}")
        print(f"   Role: {data.get('user', {}).get('role')}")
        print(f"   Health ID: {data.get('user', {}).get('health_id')}")
        return data.get('access_token')
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def test_patient_me(token):
    """Test /patient/me endpoint"""
    print("\nTesting /patient/me...")
    response = requests.get(
        f"{BASE_URL}/patient/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Patient data retrieved!")
        print(f"   Patient: {data.get('patient', {}).get('name')}")
        print(f"   Health ID: {data.get('patient', {}).get('HealthID')}")
        print(f"   Records: {len(data.get('records', []))}")
        return data
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Mobile App Backend Endpoints")
    print("=" * 60)
    print()
    
    # Test login
    token = test_login()
    
    if token:
        # Test patient/me
        test_patient_me(token)
    
    print()
    print("=" * 60)
