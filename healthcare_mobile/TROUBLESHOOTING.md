# Mobile App Troubleshooting Guide

## Common Errors and Solutions

### Error: 403 Forbidden on Login

**Symptoms:**
```
[DEBUG] [http]//127.0.0.1:8000 "POST /auth/login HTTP/1.1" 403 61
```

**Possible Causes:**

1. **User account is inactive**
   - Solution: Run `python scripts/check_test_user.py` to check and fix

2. **User has no Health ID (patient profile not created)**
   - Solution: Run `python scripts/create_complete_test_patient.py`
   - This creates both user account AND patient profile with Health ID

3. **User registered via Google OAuth (no password set)**
   - Solution: Run `python scripts/create_complete_test_patient.py` to add password

**Quick Fix:**
```bash
cd scripts
python create_complete_test_patient.py
```

---

### Error: 404 Not Found

**Symptoms:**
```
[DEBUG] [http]//127.0.0.1:8000 "GET /patient/me HTTP/1.1" 404 22
```

**Cause:** Backend server is not running

**Solution:**
1. Open a new terminal
2. Navigate to backend: `cd backend`
3. Start server: `python -m uvicorn main:app --reload`
4. Keep this terminal running!

---

### Error: Connection Refused

**Symptoms:**
```
ConnectionRefusedError: [WinError 10061] No connection could be made
```

**Cause:** Backend server is not running or wrong URL

**Solution:**
1. Verify backend is running on `http://127.0.0.1:8000`
2. Check `healthcare_mobile/config.py` has correct API_BASE_URL
3. Try accessing `http://127.0.0.1:8000/docs` in browser

---

### Error: Patient Dashboard Shows "Not Assigned"

**Symptoms:**
- Login successful
- Dashboard shows "Health ID: Not Assigned"
- No records displayed

**Cause:** User account exists but patient profile doesn't

**Solution:**
```bash
cd scripts
python create_complete_test_patient.py
```

This creates the patient profile with Health ID.

---

### Error: Invalid Email or Password

**Symptoms:**
```
[DEBUG] [http]//127.0.0.1:8000 "POST /auth/login HTTP/1.1" 401 ...
```

**Possible Causes:**

1. **Wrong credentials**
   - Default: `test@patient.com` / `password123`

2. **User doesn't exist**
   - Solution: Run `python scripts/create_complete_test_patient.py`

3. **User has no password (Google OAuth only)**
   - Solution: Run `python scripts/create_complete_test_patient.py`

---

## Diagnostic Scripts

### Check User Status
```bash
cd scripts
python check_test_user.py
```

Shows:
- If user exists
- User role
- Health ID status
- Password status
- Active status

### Create Complete Test Patient
```bash
cd scripts
python create_complete_test_patient.py
```

Creates:
- User account with password
- Patient profile with Health ID
- Sample patient data

### Test Backend Endpoints
```bash
cd scripts
python test_mobile_login.py
```

Tests:
- Login endpoint
- Patient/me endpoint
- Shows response data

---

## Step-by-Step Debugging

### 1. Verify Backend is Running

```bash
# In Terminal 1
cd backend
python -m uvicorn main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Test in browser: `http://127.0.0.1:8000/docs`

### 2. Check/Create Test User

```bash
# In Terminal 2
cd scripts
python check_test_user.py
```

If issues found:
```bash
python create_complete_test_patient.py
```

### 3. Test Login

```bash
cd scripts
python test_mobile_login.py
```

Should show:
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

### 4. Run Mobile App

```bash
cd healthcare_mobile
python main.py
```

Login with:
- Email: `test@patient.com`
- Password: `password123`

---

## Understanding the 403 Error

The 403 error on `/auth/login` can happen for these reasons:

1. **Account Inactive** (`is_active: False`)
   - Fixed by: `check_test_user.py` (auto-fixes)

2. **No Health ID** (patient profile missing)
   - Fixed by: `create_complete_test_patient.py`
   - The `/patient/me` endpoint requires a health_id
   - Without it, you can login but can't view dashboard

3. **No Password** (Google OAuth user)
   - Fixed by: `create_complete_test_patient.py`
   - Adds password to existing user

---

## Complete Setup Checklist

- [ ] MongoDB is running
- [ ] Backend `.env` file configured
- [ ] Backend server running (`uvicorn main:app --reload`)
- [ ] Test patient created (`create_complete_test_patient.py`)
- [ ] Test login works (`test_mobile_login.py`)
- [ ] Mobile app config.py has correct API URL
- [ ] Mobile app runs (`python main.py`)

---

## Still Having Issues?

1. Check backend logs for detailed error messages
2. Verify MongoDB connection in backend
3. Check firewall settings
4. Try restarting both backend and mobile app
5. Delete and recreate test user

## Quick Reset

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2 - Setup
cd scripts
python create_complete_test_patient.py
python test_mobile_login.py

# Terminal 3 - Mobile App
cd healthcare_mobile
python main.py
```
