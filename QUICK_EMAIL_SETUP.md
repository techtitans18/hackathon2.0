# Quick Setup: Enable Email OTP

## Current Status
✅ Code updated - Email sending implemented
❌ SMTP not configured - OTPs printing to console

## 3-Step Setup (5 minutes)

### Step 1: Get Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with: yalmarshekhar9@gmail.com
3. Click "Generate" 
4. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

**Note:** You need 2-Factor Authentication enabled first
- If not enabled: https://myaccount.google.com/security

### Step 2: Update .env File

Open `.env` file and replace this line:
```
SMTP_PASSWORD=your_gmail_app_password_here
```

With:
```
SMTP_PASSWORD=abcd efgh ijkl mnop
```
(Use the password from Step 1, remove spaces)

### Step 3: Restart Server

```bash
# Stop server (Ctrl+C)
# Start again
python -m uvicorn main:app --reload
```

## Test It

1. Go to Hospital Dashboard
2. Click "Patient Access (OTP)"
3. Search for patient
4. Click "Send OTP"
5. **Check patient's email** ✅

## What Happens

**Before setup:**
```
[OTP EMAIL - DEVELOPMENT MODE]
To: patient@example.com
OTP: 123456
```
OTP only in console

**After setup:**
```
[OTP EMAIL] Successfully sent to patient@example.com
```
Patient receives professional email with OTP

## Email Template

Patient receives:
```
Subject: Healthcare Access OTP

Your OTP: 123456
Valid for: 10 minutes
```

## Troubleshooting

**"Authentication failed"**
- Enable 2FA first
- Generate new app password
- Copy password without spaces

**"Still printing to console"**
- Check .env has SMTP_PASSWORD set
- Restart server
- Check no typos in .env

**"Email not received"**
- Check spam folder
- Verify patient email is correct
- Check server console for errors

## Alternative: Keep Console Mode

If you don't want to setup email:
- Leave SMTP_PASSWORD as is
- OTPs will print to console
- Copy OTP from console and use it
- Works fine for development/testing

## Summary

**Setup:** 5 minutes
**Cost:** Free
**Result:** Professional OTP emails to patients

See SETUP_EMAIL_OTP.md for detailed guide.
