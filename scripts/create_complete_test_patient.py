"""
Create a complete test patient with health ID and patient profile
"""
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from database.db import get_user_collection, get_patient_collection

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_health_id(email: str, dob: str) -> str:
    """Generate deterministic health ID"""
    health_id_input = f"{email}|{dob}"
    return hashlib.sha256(health_id_input.encode('utf-8')).hexdigest()[:16].upper()

def create_complete_test_patient():
    """Create a complete test patient with user account and patient profile"""
    users = get_user_collection()
    patients = get_patient_collection()
    
    # Test patient data
    email = "test@patient.com"
    password = "password123"
    name = "Test Patient"
    dob = "1990-01-01"
    age = 34
    phone = "+1234567890"
    blood_group = "O+"
    
    # Generate health ID
    health_id = generate_health_id(email, dob)
    
    now = datetime.now(timezone.utc)
    
    # Create or update user account
    existing_user = users.find_one({"email": email})
    if existing_user:
        users.update_one(
            {"email": email},
            {
                "$set": {
                    "password_hash": hash_password(password),
                    "health_id": health_id,
                    "is_active": True,
                    "updated_at": now
                }
            }
        )
        print(f"[OK] Updated user account: {email}")
    else:
        user_doc = {
            "email": email,
            "subject": email,
            "name": name,
            "password_hash": hash_password(password),
            "picture": None,
            "role": "patient",
            "health_id": health_id,
            "hospital_id": None,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "last_login_at": now,
        }
        users.insert_one(user_doc)
        print(f"[OK] Created user account: {email}")
    
    # Create or update patient profile
    existing_patient = patients.find_one({"health_id": health_id})
    if existing_patient:
        patients.update_one(
            {"health_id": health_id},
            {
                "$set": {
                    "name": name,
                    "age": age,
                    "phone": phone,
                    "blood_group": blood_group,
                    "updated_at": now
                }
            }
        )
        print(f"[OK] Updated patient profile: {health_id}")
    else:
        patient_doc = {
            "health_id": health_id,
            "name": name,
            "age": age,
            "phone": phone,
            "dob": dob,
            "blood_group": blood_group,
            "photo_url": None,
            "email": email,
            "created_at": now,
            "created_by_hospital_id": "SYSTEM",
        }
        patients.insert_one(patient_doc)
        print(f"[OK] Created patient profile: {health_id}")
    
    print()
    print("=" * 60)
    print("Complete Test Patient Created!")
    print("=" * 60)
    print(f"Email:      {email}")
    print(f"Password:   {password}")
    print(f"Name:       {name}")
    print(f"Health ID:  {health_id}")
    print(f"DOB:        {dob}")
    print(f"Age:        {age}")
    print(f"Phone:      {phone}")
    print(f"Blood:      {blood_group}")
    print(f"Role:       patient")
    print("=" * 60)
    print()
    print("You can now login to the mobile app with these credentials!")
    print("The patient will have a Health ID and can view their dashboard.")

if __name__ == "__main__":
    print("=" * 60)
    print("Creating Complete Test Patient")
    print("=" * 60)
    print()
    
    try:
        create_complete_test_patient()
    except Exception as e:
        print(f"[X] Error: {e}")
        import traceback
        traceback.print_exc()
