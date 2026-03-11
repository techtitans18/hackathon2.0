# 403 Forbidden Error - Complete Fix Guide

## What is 403 Forbidden?

**403 Forbidden** means you don't have permission to access the endpoint. This happens when:
1. You're not logged in
2. Your role is wrong (not "hospital")
3. You don't have a hospital_id assigned
4. Token expired

---

## Quick Fix Steps

### Step 1: Check Your Login Status

**In Browser Console (F12):**
```javascript
// Check if logged in
const token = localStorage.getItem('access_token');
console.log('Token exists:', !!token);
```

**Result:**
- ✅ Token exists: true → Go to Step 2
- ❌ Token exists: false → **You're not logged in. Login first!**

---

### Step 2: Check Your Role and Hospital ID

**In Browser Console:**
```javascript
const token = localStorage.getItem('access_token');
const payload = JSON.parse(atob(token.split('.')[0]));

console.log('Your Details:');
console.log('  Email:', payload.email);
console.log('  Role:', payload.role);
console.log('  Hospital ID:', payload.hospital_id);
```

**Expected Output:**
```
Your Details:
  Email: hospital@example.com
  Role: hospital              ← MUST be "hospital"
  Hospital ID: HOSP123        ← MUST have a value (not null)
```

**If Wrong:**

❌ **Role is NOT "hospital"** (e.g., "patient", "admin", null)
- **Fix**: Admin must change your role to "hospital"
- Go to Admin Dashboard → User Management → Find your email → Set role to "hospital"

❌ **Hospital ID is null or undefined**
- **Fix**: Admin must assign you a hospital_id
- Go to Admin Dashboard → User Management → Find your email → Set hospital_id

❌ **Both are wrong**
- **Fix**: Admin must set both role AND hospital_id
- Then logout and login again

---

### Step 3: Logout and Login Again

After admin fixes your account:

1. Click Logout button
2. Clear browser cache (Ctrl+Shift+Delete)
3. Login again with Google
4. Check token again (Step 2)

---

## Detailed Troubleshooting

### Issue 1: Not Logged In

**Symptoms:**
- 403 on all endpoints
- No token in localStorage
- Redirected to login page

**Solution:**
```
1. Go to http://127.0.0.1:8000/app
2. Click "Sign in with Google"
3. Authorize the app
4. Should redirect to dashboard
```

---

### Issue 2: Wrong Role

**Symptoms:**
- 403 on /blockchain
- 403 on /patient_access/send_otp
- Token exists but role is not "hospital"

**Check:**
```javascript
const token = localStorage.getItem('access_token');
const payload = JSON.parse(atob(token.split('.')[0]));
console.log('Role:', payload.role);
// Should be: "hospital"
```

**Solution:**
Admin must update your role:

**For Admin:**
1. Login as admin
2. Go to Admin Dashboard
3. Click "User Management"
4. Find the user's email
5. Edit user:
   - Role: hospital
   - Hospital ID: (assign a hospital ID)
6. Save

**For User:**
1. Logout
2. Login again
3. Check role again

---

### Issue 3: No Hospital ID

**Symptoms:**
- 403 on hospital-specific endpoints
- Token shows hospital_id: null

**Check:**
```javascript
const token = localStorage.getItem('access_token');
const payload = JSON.parse(atob(token.split('.')[0]));
console.log('Hospital ID:', payload.hospital_id);
// Should be: "HOSP123" (some value)
```

**Solution:**
Admin must assign hospital_id:

**For Admin:**
1. Go to Admin Dashboard → User Management
2. Find user
3. Set hospital_id field
4. Save

**For User:**
1. Logout and login again
2. Verify hospital_id is set

---

### Issue 4: Token Expired

**Symptoms:**
- Was working before
- Now getting 403 on all endpoints
- Token exists but expired

**Check:**
```javascript
const token = localStorage.getItem('access_token');
const payload = JSON.parse(atob(token.split('.')[0]));
const now = Math.floor(Date.now() / 1000);
const expired = payload.exp < now;
console.log('Token expired:', expired);
```

**Solution:**
```
1. Logout
2. Login again
3. New token will be issued
```

---

### Issue 5: Blockchain Endpoint 403

**Fixed!** Blockchain endpoint now allows both admin AND hospital roles.

**Before:**
```python
@router.get("/blockchain")
def get_blockchain(
    _: SessionUser = Depends(require_roles(ROLE_ADMIN)),  # Only admin
)
```

**After:**
```python
@router.get("/blockchain")
def get_blockchain(
    _: SessionUser = Depends(require_roles(ROLE_ADMIN, ROLE_HOSPITAL)),  # Admin OR hospital
)
```

**If still getting 403:**
- Check your role is "hospital" (Step 2)
- Logout and login again
- Clear browser cache

---

## Permission Matrix

| Endpoint | Admin | Hospital | Patient |
|----------|-------|----------|---------|
| /blockchain | ✅ | ✅ | ❌ |
| /patient_access/send_otp | ❌ | ✅ | ❌ |
| /patient_access/verify_otp | ❌ | ✅ | ❌ |
| /register_patient | ❌ | ✅ | ❌ |
| /add_record | ❌ | ✅ | ❌ |
| /patient/me | ❌ | ❌ | ✅ |
| /admin/users | ✅ | ❌ | ❌ |

---

## Complete Test Script

**Run in Browser Console:**

```javascript
// Complete authentication check
function checkAuth() {
  console.log('='.repeat(60));
  console.log('AUTHENTICATION CHECK');
  console.log('='.repeat(60));
  
  // Check token exists
  const token = localStorage.getItem('access_token');
  if (!token) {
    console.error('❌ FAILED: No token found');
    console.log('→ Solution: Login first');
    return;
  }
  console.log('✓ Token exists');
  
  // Decode token
  try {
    const payload = JSON.parse(atob(token.split('.')[0]));
    
    console.log('\nUser Details:');
    console.log('  Email:', payload.email);
    console.log('  Name:', payload.name);
    console.log('  Role:', payload.role);
    console.log('  Hospital ID:', payload.hospital_id);
    
    // Check role
    if (payload.role !== 'hospital') {
      console.error('\n❌ FAILED: Wrong role');
      console.log('  Current:', payload.role);
      console.log('  Expected: hospital');
      console.log('→ Solution: Admin must set role to "hospital"');
    } else {
      console.log('\n✓ Role is correct');
    }
    
    // Check hospital_id
    if (!payload.hospital_id) {
      console.error('\n❌ FAILED: No hospital_id');
      console.log('→ Solution: Admin must assign hospital_id');
    } else {
      console.log('✓ Hospital ID assigned:', payload.hospital_id);
    }
    
    // Check expiry
    const now = Math.floor(Date.now() / 1000);
    if (payload.exp < now) {
      console.error('\n❌ FAILED: Token expired');
      console.log('→ Solution: Logout and login again');
    } else {
      const remaining = Math.floor((payload.exp - now) / 60);
      console.log(`✓ Token valid (${remaining} minutes remaining)`);
    }
    
    // Summary
    console.log('\n' + '='.repeat(60));
    if (payload.role === 'hospital' && payload.hospital_id && payload.exp > now) {
      console.log('✅ ALL CHECKS PASSED - You should have access');
    } else {
      console.log('❌ SOME CHECKS FAILED - Fix issues above');
    }
    console.log('='.repeat(60));
    
  } catch (e) {
    console.error('❌ FAILED: Invalid token format');
    console.log('→ Solution: Logout and login again');
  }
}

// Run the check
checkAuth();
```

---

## Server-Side Debugging

**Check server console for:**

```
[DEBUG] Current user role: hospital
[DEBUG] Current user hospital_id: HOSP123
[DEBUG] Search type: health_id
[DEBUG] Search value: ABC123
```

**If you see:**
- `role: None` → Not logged in
- `hospital_id: None` → Not assigned
- No debug logs → Request not reaching server (CORS issue?)

---

## Admin: How to Fix User Permissions

### Step 1: Login as Admin
```
1. Go to http://127.0.0.1:8000/app
2. Login with admin email (from ADMIN_BOOTSTRAP_EMAILS)
```

### Step 2: Go to User Management
```
1. Click "Admin Dashboard"
2. Click "User Management" tab
```

### Step 3: Find User
```
1. Look for user's email in the list
2. Click "Edit" or find their row
```

### Step 4: Set Permissions
```
1. Role: Select "hospital"
2. Hospital ID: Enter hospital ID (e.g., "HOSP001")
3. Click "Save" or "Update"
```

### Step 5: Verify
```
1. User should logout
2. User should login again
3. Check token (Step 2 above)
```

---

## Still Not Working?

### 1. Clear Everything
```
1. Logout
2. Clear browser cache (Ctrl+Shift+Delete)
3. Clear localStorage:
   localStorage.clear()
4. Close browser
5. Open browser
6. Login again
```

### 2. Check Server Logs
```
Look for errors in server console:
- Authentication errors
- Database errors
- Permission errors
```

### 3. Verify Database
```python
# Run this to check user in database
python debug_patient_search.py
# Or check users collection directly
```

### 4. Test with cURL
```bash
# Get your token
TOKEN="your_token_here"

# Test blockchain endpoint
curl -H "Authorization: Bearer $TOKEN" \
     http://127.0.0.1:8000/blockchain

# Should return blockchain data, not 403
```

---

## Summary

**Most Common Fix:**
1. Admin assigns role="hospital" and hospital_id
2. User logs out
3. User logs in again
4. Everything works ✅

**Quick Check:**
```javascript
// Run in console
const t = localStorage.getItem('access_token');
const p = JSON.parse(atob(t.split('.')[0]));
console.log('Role:', p.role, '| Hospital:', p.hospital_id);
// Should show: Role: hospital | Hospital: HOSP123
```
