"""
Quick script to create a test user with password for mobile app testing.
"""
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from database.db import get_user_collection


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def create_test_user():
    """Create a test patient user with password"""
    users = get_user_collection()
    
    # Test user credentials
    email = "test@patient.com"
    password = "password123"
    name = "Test Patient"
    
    # Check if user already exists
    existing = users.find_one({"email": email})
    if existing:
        # Update with password
        password_hash = hash_password(password)
        users.update_one(
            {"email": email},
            {"$set": {"password_hash": password_hash}}
        )
        print(f"✅ Updated existing user: {email}")
    else:
        # Create new user
        now = datetime.now(timezone.utc)
        user_doc = {
            "email": email,
            "subject": email,
            "name": name,
            "password_hash": hash_password(password),
            "picture": None,
            "role": "patient",
            "health_id": None,
            "hospital_id": None,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "last_login_at": now,
        }
        users.insert_one(user_doc)
        print(f"✅ Created new user: {email}")
    
    print()
    print("=" * 60)
    print("Test User Credentials for Mobile App:")
    print("=" * 60)
    print(f"Email:    {email}")
    print(f"Password: {password}")
    print(f"Role:     patient")
    print("=" * 60)
    print()
    print("Use these credentials to login in the mobile app!")


if __name__ == "__main__":
    print("=" * 60)
    print("Creating Test User for Mobile App")
    print("=" * 60)
    print()
    
    try:
        create_test_user()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
