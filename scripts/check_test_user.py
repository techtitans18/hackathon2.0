"""
Check and fix test user status
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from database.db import get_user_collection

def check_test_user():
    """Check test user status"""
    users = get_user_collection()
    
    email = "test@patient.com"
    user = users.find_one({"email": email})
    
    if not user:
        print(f"[X] User {email} does NOT exist!")
        print("\nRun this command to create the user:")
        print("  python scripts/create_test_user.py")
        return False
    
    print(f"[OK] User found: {email}")
    print(f"   Name: {user.get('name')}")
    print(f"   Role: {user.get('role')}")
    print(f"   Health ID: {user.get('health_id')}")
    print(f"   Is Active: {user.get('is_active')}")
    print(f"   Has Password: {'Yes' if user.get('password_hash') else 'No'}")
    
    # Check if user is inactive
    if not user.get('is_active', True):
        print("\n[!] User is INACTIVE!")
        print("   Fixing...")
        users.update_one(
            {"email": email},
            {"$set": {"is_active": True}}
        )
        print("[OK] User activated!")
        return True
    
    # Check if user has no password
    if not user.get('password_hash'):
        print("\n[!] User has NO PASSWORD!")
        print("   Run this command to add password:")
        print("  python scripts/create_test_user.py")
        return False
    
    print("\n[OK] User is ready to use!")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Checking Test User Status")
    print("=" * 60)
    print()
    
    try:
        check_test_user()
    except Exception as e:
        print(f"[X] Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
