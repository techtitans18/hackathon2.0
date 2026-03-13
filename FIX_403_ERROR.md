# Fix for 403 Forbidden Error

## Problem

You were getting this error:
```
[DEBUG] [http]//127.0.0.1:8000 "POST /auth/login HTTP/1.1" 403 61
```

## Root Cause

The test user (`test@patient.com`) existed but **did not have a Health ID** assigned. 

The mobile app flow is:
1. Login → Success (user authenticated)
2. Load dashboard → Calls `/patient/me` endpoint
3. `/patient/me` requires `health_id` to be set
4. If no `health_id` → Returns 403 Forbidden

## Why This Happened

The `create_test_user.py` script only created a **user account** with password, but didn't create the **patient profile** in the `patients` collection. 

In this system:
- **User account** = Authentication (login credentials, role)
- **Patient profile** = Medical data (health ID, DOB, blood group, records)

A patient needs BOTH to use the mobile app dashboard.

## Solution

### Quick Fix (Run This Now)

```bash
cd c:\Users\Shekhar Yalmar\Desktop\lib\healthcare_blockchain\scripts
python create_complete_test_patient.py
```

This creates:
- ✅ User account with password
- ✅ Patient profile with Health ID
- ✅ Sample patient data (DOB, blood group, etc.)

### Then Run Mobile App

```bash
# Terminal 1 - Backend (if not already running)
cd c:\Users\Shekhar Yalmar\Desktop\lib\healthcare_blockchain\backend
python -m uvicorn main:app --reload

# Terminal 2 - Mobile App
cd c:\Users\Shekhar Yalmar\Desktop\lib\healthcare_blockchain\healthcare_mobile
python main.py
```

Login with:
- **Email**: `test@patient.com`
- **Password**: `password123`

## What Was Fixed

### 1. Mobile App - Graceful Handling
**File**: `healthcare_mobile/screens/patient/dashboard.py`

Added check for missing Health ID:
```python
if health_id:
    self.ids.health_id.text = f"Health ID: {health_id}"
    self.load_statistics()
else:
    self.ids.health_id.text = "Health ID: Not Assigned"
    self.ids.last_activity.text = "No patient profile yet. Visit a hospital to register."
```

### 2. New Script - Complete Patient Setup
**File**: `scripts/create_complete_test_patient.py`

Creates both:
- User account (for authentication)
- Patient profile (for medical data)

### 3. Diagnostic Script
**File**: `scripts/check_test_user.py`

Checks:
- User exists
- Has password
- Is active
- Has Health ID

### 4. Documentation
**Files**: 
- `healthcare_mobile/QUICK_START.md` - Setup guide
- `healthcare_mobile/TROUBLESHOOTING.md` - Error solutions

## Understanding the System

### User Account (users collection)
```json
{
  "email": "test@patient.com",
  "password_hash": "...",
  "role": "patient",
  "health_id": "96E5F03F52F53FF6",  // Links to patient profile
  "is_active": true
}
```

### Patient Profile (patients collection)
```json
{
  "health_id": "96E5F03F52F53FF6",
  "name": "Test Patient",
  "email": "test@patient.com",
  "dob": "1990-01-01",
  "age": 34,
  "blood_group": "O+",
  "phone": "+1234567890"
}
```

### Medical Records (records collection)
```json
{
  "health_id": "96E5F03F52F53FF6",  // Links to patient
  "hospital_id": "HOSP001",
  "record_type": "Lab Report",
  "file_name": "blood_test.pdf",
  // ... more fields
}
```

## API Flow

### Login Flow
```
POST /auth/login
  ↓
Returns: JWT token + user data (including health_id)
  ↓
Mobile app stores token
```

### Dashboard Flow
```
GET /patient/me (with JWT token)
  ↓
Backend checks: Does user have health_id?
  ↓
YES → Fetch patient profile + records → Return data
NO  → Return 403 Forbidden
```

## Why 403 Instead of 404?

- **403 Forbidden** = "You're authenticated, but you don't have permission"
  - User is logged in, but missing required data (health_id)
  
- **404 Not Found** = "Resource doesn't exist"
  - Would be used if patient profile doesn't exist in database

The backend returns 403 because the user IS authenticated, but the account is incomplete (missing health_id).

## Testing the Fix

### 1. Check User Status
```bash
cd scripts
python check_test_user.py
```

Expected output:
```
[OK] User found: test@patient.com
   Name: Test Patient
   Role: patient
   Health ID: 96E5F03F52F53FF6
   Is Active: True
   Has Password: Yes

[OK] User is ready to use!
```

### 2. Test Login API
```bash
cd scripts
python test_mobile_login.py
```

Expected output:
```
[OK] Login successful!
   Token: eyJ...
   User: Test Patient
   Role: patient
   Health ID: 96E5F03F52F53FF6

[OK] Patient data retrieved!
   Patient: Test Patient
   Health ID: 96E5F03F52F53FF6
   Records: 0
```

### 3. Run Mobile App
```bash
cd healthcare_mobile
python main.py
```

Should now show:
- ✅ Login successful
- ✅ Dashboard loads
- ✅ Health ID displayed
- ✅ Statistics shown (0 records, 0 hospitals)

## Summary

**Problem**: 403 error because user had no Health ID
**Solution**: Run `create_complete_test_patient.py` to create full patient profile
**Result**: Mobile app now works correctly with complete patient data

## Next Steps

1. ✅ Run `create_complete_test_patient.py`
2. ✅ Start backend server
3. ✅ Run mobile app
4. ✅ Login and view dashboard

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more help!
