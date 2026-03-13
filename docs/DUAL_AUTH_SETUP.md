# Dual Authentication Setup Guide

## Overview
The system now supports **both** Google OAuth and Email/Password authentication for web and mobile apps.

## Features
- ✅ Google OAuth (Web only)
- ✅ Email/Password (Web + Mobile)
- ✅ Secure password hashing (SHA-256)
- ✅ User registration endpoint
- ✅ Unified authentication flow

---

## Setup Instructions

### 1. Restart Backend Server
```bash
cd backend
python -m uvicorn main:app --reload
```

### 2. Add Passwords to Existing Users

Run the utility script to add passwords to existing Google OAuth users:

```bash
cd scripts
python add_user_passwords.py
```

**Options:**
- **Option 1**: Add password to specific user
- **Option 2**: Add default password to all users

**Example:**
```
Choose option (1 or 2): 2
Enter default password (default: password123): mypassword
Add password 'mypassword' to all users without passwords? (yes/no): yes
```

---

## Usage

### Web Frontend

**Google OAuth Login:**
1. Go to `http://localhost:5173`
2. Click "Sign in with Google"
3. Authenticate with Google account

**Email/Password Login:**
1. Go to `http://localhost:5173`
2. Click "Sign in with Email"
3. Enter email and password
4. Click "Sign In"

### Mobile App

**Email/Password Login:**
1. Run mobile app: `python main.py`
2. Enter email and password
3. Tap "Login"

---

## API Endpoints

### Email/Password Authentication

**Login:**
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": null,
  "token_type": "bearer",
  "expires_at": "2024-03-15T10:00:00Z",
  "user": {
    "email": "user@example.com",
    "name": "John Doe",
    "role": "patient",
    "health_id": "HID123",
    "hospital_id": null
  }
}
```

**Register (Patient only):**
```http
POST /auth/register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "securepassword",
  "name": "Jane Doe",
  "role": "patient"
}
```

### Google OAuth (Existing)

**Login:**
```http
POST /auth/google
Content-Type: application/json

{
  "credential": "google_id_token_here"
}
```

---

## User Types

### Google OAuth Users
- Have `subject` field (Google ID)
- No `password_hash` field
- Can add password later using utility script

### Email/Password Users
- Have `password_hash` field
- `subject` = email
- Can be created via `/auth/register`

### Hybrid Users
- Have both Google OAuth and password
- Can login with either method

---

## Security Notes

### Password Hashing
- Uses SHA-256 (simple for demo)
- **Production**: Use bcrypt or argon2

### Password Requirements
- Minimum 6 characters
- No complexity requirements (add in production)

### Token Security
- JWT tokens with HMAC-SHA256 signature
- 8-hour expiration
- Stored in localStorage (web) or keyring (mobile)

---

## Testing

### Test Email/Password Login

**Web:**
```bash
# 1. Add password to existing user
cd scripts
python add_user_passwords.py

# 2. Open browser
http://localhost:5173

# 3. Click "Sign in with Email"
# 4. Enter credentials
```

**Mobile:**
```bash
# 1. Run mobile app
cd healthcare_mobile
python main.py

# 2. Enter email and password
# 3. Click Login
```

### Test User Registration

**Using curl:**
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newpatient@example.com",
    "password": "password123",
    "name": "New Patient"
  }'
```

**Using Postman:**
1. POST `http://127.0.0.1:8000/auth/register`
2. Body (JSON):
```json
{
  "email": "newpatient@example.com",
  "password": "password123",
  "name": "New Patient"
}
```

---

## Troubleshooting

### "Invalid email or password"
- Check if user exists in database
- Verify password was added using utility script
- Check email is lowercase

### "This account uses Google Sign-In"
- User registered via Google OAuth
- No password set
- Run `add_user_passwords.py` to add password

### "Only patient accounts can be self-registered"
- Registration endpoint only allows patient role
- Admin/Hospital accounts must be created by admin

### Mobile app connection refused
- Ensure backend is running
- Check `config.py` has correct API URL
- Verify `.env` file exists in mobile app folder

---

## Production Recommendations

1. **Use bcrypt for password hashing**
```python
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

2. **Add password complexity requirements**
- Minimum 8 characters
- Uppercase + lowercase + numbers + symbols

3. **Implement rate limiting**
- Prevent brute force attacks
- Use libraries like `slowapi`

4. **Add email verification**
- Send verification email on registration
- Verify email before allowing login

5. **Implement refresh tokens**
- Short-lived access tokens (15 min)
- Long-lived refresh tokens (7 days)

6. **Add 2FA (Two-Factor Authentication)**
- TOTP (Time-based One-Time Password)
- SMS verification

---

## Summary

✅ **Dual authentication system ready**
- Google OAuth for web
- Email/Password for web + mobile
- Unified token system
- Secure password storage

🚀 **Next Steps:**
1. Restart backend server
2. Add passwords to existing users
3. Test web login (both methods)
4. Test mobile login
5. Deploy to production with enhanced security

---

**Built with ❤️ for better healthcare management**
