"""
Check User Authentication and Permissions
Run this to verify your login token and permissions
"""

print("""
╔═══════════════════════════════════════════════════════════╗
║  CHECK YOUR AUTHENTICATION TOKEN                          ║
╚═══════════════════════════════════════════════════════════╝

STEP 1: Open Browser Console
  - Press F12 or Right-click → Inspect
  - Go to "Console" tab

STEP 2: Run this command:
  localStorage.getItem('access_token')

STEP 3: Copy the token and decode it at: https://jwt.io

STEP 4: Check the payload for:
  {
    "sub": "google-user-id",
    "email": "your@email.com",
    "name": "Your Name",
    "role": "hospital",           ← Must be "hospital"
    "hospital_id": "HOSP123",     ← Must have a value
    "health_id": null,
    "exp": 1234567890
  }

╔═══════════════════════════════════════════════════════════╗
║  COMMON ISSUES                                            ║
╚═══════════════════════════════════════════════════════════╝

❌ Issue 1: role is NOT "hospital"
   Solution: Admin must assign you hospital role
   
❌ Issue 2: hospital_id is null or missing
   Solution: Admin must assign you a hospital_id
   
❌ Issue 3: Token expired
   Solution: Logout and login again
   
❌ Issue 4: No token in localStorage
   Solution: You're not logged in

╔═══════════════════════════════════════════════════════════╗
║  QUICK FIX                                                ║
╚═══════════════════════════════════════════════════════════╝

If you're missing hospital_id:

1. Ask admin to go to Admin Dashboard
2. Admin clicks "User Management"
3. Admin finds your email
4. Admin assigns:
   - Role: hospital
   - Hospital ID: (your hospital ID)
5. Logout and login again

╔═══════════════════════════════════════════════════════════╗
║  TEST YOUR TOKEN                                          ║
╚═══════════════════════════════════════════════════════════╝

Run this in browser console:

// Get token
const token = localStorage.getItem('access_token');
if (!token) {
  console.error('❌ No token found - Not logged in');
} else {
  // Decode token
  const payload = JSON.parse(atob(token.split('.')[0]));
  console.log('✓ Token found');
  console.log('Role:', payload.role);
  console.log('Hospital ID:', payload.hospital_id);
  console.log('Email:', payload.email);
  
  // Check permissions
  if (payload.role !== 'hospital') {
    console.error('❌ Wrong role:', payload.role);
  } else {
    console.log('✓ Role is correct');
  }
  
  if (!payload.hospital_id) {
    console.error('❌ No hospital_id assigned');
  } else {
    console.log('✓ Hospital ID assigned:', payload.hospital_id);
  }
  
  // Check expiry
  const now = Math.floor(Date.now() / 1000);
  if (payload.exp < now) {
    console.error('❌ Token expired');
  } else {
    console.log('✓ Token valid');
  }
}

╔═══════════════════════════════════════════════════════════╗
║  PERMISSION REQUIREMENTS                                  ║
╚═══════════════════════════════════════════════════════════╝

Endpoint                    Required Role
─────────────────────────────────────────────────────────
/blockchain                 admin OR hospital ✓ FIXED
/patient_access/send_otp    hospital
/patient_access/verify_otp  hospital
/register_patient           hospital
/add_record                 hospital

If you get 403 Forbidden:
1. Check your role is "hospital"
2. Check you have hospital_id
3. Logout and login again
4. Clear browser cache

╔═══════════════════════════════════════════════════════════╗
║  BACKEND CHECK                                            ║
╚═══════════════════════════════════════════════════════════╝

Check server logs for:

[DEBUG] Current user role: hospital
[DEBUG] Current user hospital_id: HOSP123

If you see:
- role: None → Not logged in
- hospital_id: None → Not assigned

Contact admin to fix your account.

""")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Copy the commands above and run in browser console")
    print("="*60)
