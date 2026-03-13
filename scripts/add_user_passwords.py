"""
Utility script to add passwords to existing users.
Run this to enable email/password login for existing Google OAuth users.
"""
import hashlib
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from database.db import get_user_collection


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def add_password_to_user(email: str, password: str):
    """Add password to existing user"""
    users = get_user_collection()
    
    # Check if user exists
    user = users.find_one({"email": email.lower().strip()})
    if not user:
        print(f"❌ User not found: {email}")
        return False
    
    # Hash password
    password_hash = hash_password(password)
    
    # Update user
    result = users.update_one(
        {"email": email.lower().strip()},
        {"$set": {"password_hash": password_hash}}
    )
    
    if result.modified_count > 0:
        print(f"✅ Password added for: {email}")
        print(f"   Role: {user.get('role')}")
        print(f"   Name: {user.get('name')}")
        return True
    else:
        print(f"⚠️  User already has password: {email}")
        return True


def add_password_to_all_users(default_password: str = "password123"):
    """Add default password to all users without passwords"""
    users = get_user_collection()
    
    # Find users without password_hash
    users_without_password = users.find({"password_hash": {"$exists": False}})
    
    count = 0
    for user in users_without_password:
        email = user.get("email")
        if email:
            password_hash = hash_password(default_password)
            users.update_one(
                {"email": email},
                {"$set": {"password_hash": password_hash}}
            )
            print(f"✅ Added password to: {email} (Role: {user.get('role')})")
            count += 1
    
    if count == 0:
        print("ℹ️  All users already have passwords")
    else:
        print(f"\n✅ Added passwords to {count} users")
        print(f"   Default password: {default_password}")


if __name__ == "__main__":
    print("=" * 60)
    print("Add Passwords to Existing Users")
    print("=" * 60)
    print()
    
    # Option 1: Add password to specific user
    print("Option 1: Add password to specific user")
    print("Example: add_password_to_user('admin@example.com', 'mypassword')")
    print()
    
    # Option 2: Add default password to all users
    print("Option 2: Add default password to all users without passwords")
    print()
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        email = input("Enter user email: ").strip()
        password = input("Enter password: ").strip()
        if email and password:
            add_password_to_user(email, password)
        else:
            print("❌ Email and password are required")
    
    elif choice == "2":
        default_password = input("Enter default password (default: password123): ").strip()
        if not default_password:
            default_password = "password123"
        
        confirm = input(f"Add password '{default_password}' to all users without passwords? (yes/no): ").strip().lower()
        if confirm == "yes":
            add_password_to_all_users(default_password)
        else:
            print("❌ Cancelled")
    
    else:
        print("❌ Invalid option")
    
    print()
    print("=" * 60)
