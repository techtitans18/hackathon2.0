# Mobile App Quick Start Guide

## Issue: Backend Not Running

The mobile app requires the backend server to be running. The error you're seeing is because the backend at `http://127.0.0.1:8000` is not accessible.

## Solution: Start Backend Server

### Step 1: Open a NEW terminal/PowerShell window

### Step 2: Navigate to backend directory
```bash
cd c:\Users\Shekhar Yalmar\Desktop\lib\healthcare_blockchain\backend
```

### Step 3: Start the backend server
```bash
python -m uvicorn main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 4: Keep this terminal open!

The backend must stay running while you use the mobile app.

### Step 5: In your ORIGINAL terminal, run the mobile app again
```bash
cd c:\Users\Shekhar Yalmar\Desktop\lib\healthcare_blockchain\healthcare_mobile
python main.py
```

## Test User Credentials

Use these credentials to login:
- **Email**: `test@patient.com`
- **Password**: `password123`

## Optional: Create Test User (if needed)

If the test user doesn't exist or you're getting a 403 error, run:
```bash
cd c:\Users\Shekhar Yalmar\Desktop\lib\healthcare_blockchain\scripts
python create_complete_test_patient.py
```

This creates a complete patient with:
- User account with password
- Patient profile with Health ID
- Sample patient data (DOB, blood group, etc.)

## Troubleshooting

### Backend won't start?
- Make sure MongoDB is running
- Check `.env` file exists in backend directory
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Mobile app still can't connect?
- Verify backend is running on `http://127.0.0.1:8000`
- Check firewall settings
- Try accessing `http://127.0.0.1:8000/docs` in your browser

### Login fails?
- Run `python scripts/create_test_user.py` to create/update test user
- Check backend logs for errors

## Summary

**You need TWO terminals running simultaneously:**

1. **Terminal 1** (Backend): `cd backend && python -m uvicorn main:app --reload`
2. **Terminal 2** (Mobile App): `cd healthcare_mobile && python main.py`

Both must be running at the same time!
