# Setup Email Sending for OTP

## Current Status

**Development Mode**: OTPs are printed to server console
**Production Mode**: Requires SMTP configuration

## Quick Setup with Gmail

### Step 1: Enable 2-Factor Authentication

1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Follow the setup process

### Step 2: Generate App Password

1. Go to https://myaccount.google.com/apppasswords
2. Select app: "Mail"
3. Select device: "Other (Custom name)"
4. Enter name: "Healthcare OTP"
5. Click "Generate"
6. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 3: Update .env File

Add these lines to your `.env` file:

```env
# Email Configuration for OTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
SMTP_FROM=your_email@gmail.com
```

**Replace:**
- `your_email@gmail.com` with your Gmail address
- `abcd efgh ijkl mnop` with the app password from Step 2

### Step 4: Restart Server

```bash
# Stop server (Ctrl+C)
# Start server again
python -m uvicorn main:app --reload
```

### Step 5: Test

1. Go to Hospital Dashboard
2. Click "Patient Access (OTP)"
3. Search for patient
4. Click "Send OTP"
5. **Check patient's email inbox** ✅

---

## Alternative: Other Email Services

### Using Outlook/Hotmail

```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your_email@outlook.com
SMTP_PASSWORD=your_password
SMTP_FROM=your_email@outlook.com
```

### Using Yahoo Mail

```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your_email@yahoo.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your_email@yahoo.com
```

### Using Custom SMTP Server

```env
SMTP_HOST=mail.yourdomain.com
SMTP_PORT=587
SMTP_USER=noreply@yourdomain.com
SMTP_PASSWORD=your_password
SMTP_FROM=noreply@yourdomain.com
```

---

## Email Template

When configured, patients will receive:

**Subject:** Healthcare Access OTP

**Body:**
```
Healthcare Access OTP

Your OTP for healthcare record access is: 123456

This code is valid for 10 minutes.

If you did not request this code, please ignore this email.

Thank you,
Healthcare System
```

---

## Troubleshooting

### Issue 1: "Authentication failed"

**Cause:** Wrong email or password

**Solution:**
- Verify email address is correct
- Verify app password is correct (no spaces)
- Make sure 2FA is enabled
- Generate new app password

### Issue 2: "Connection refused"

**Cause:** Wrong SMTP host or port

**Solution:**
- Gmail: `smtp.gmail.com:587`
- Outlook: `smtp-mail.outlook.com:587`
- Check firewall settings

### Issue 3: "Email not received"

**Possible causes:**
- Email in spam folder
- Wrong patient email address
- SMTP not configured (check server console)

**Check:**
1. Look in spam/junk folder
2. Check server console for errors
3. Verify patient email is correct

### Issue 4: Still printing to console

**Cause:** SMTP not configured in .env

**Solution:**
- Add SMTP settings to .env
- Restart server
- Check .env file is in project root

---

## Development vs Production

### Development Mode (No SMTP configured)

```
[OTP EMAIL - DEVELOPMENT MODE]
To: patient@example.com
OTP: 123456
Valid for: 10 minutes
```

**Use this for:**
- Local testing
- Development
- When you don't have email setup

**How to use:**
- Check server console for OTP
- Copy OTP from console
- Enter in application

### Production Mode (SMTP configured)

```
[OTP EMAIL] Successfully sent to patient@example.com
```

**Use this for:**
- Production deployment
- Real patient access
- When email is required

**How to use:**
- Patient receives email
- Patient provides OTP to staff
- Staff enters OTP

---

## Security Best Practices

### 1. Use App Passwords (Not Account Password)

❌ **Don't use:**
```env
SMTP_PASSWORD=MyGmailPassword123
```

✅ **Use:**
```env
SMTP_PASSWORD=abcd efgh ijkl mnop  # App password
```

### 2. Keep .env Secure

```bash
# Add to .gitignore
echo ".env" >> .gitignore

# Never commit .env to git
git rm --cached .env
```

### 3. Use Environment Variables in Production

```bash
# Set environment variables instead of .env file
export SMTP_HOST=smtp.gmail.com
export SMTP_USER=your_email@gmail.com
export SMTP_PASSWORD=your_app_password
```

### 4. Rotate Passwords Regularly

- Generate new app password every 3-6 months
- Revoke old app passwords
- Update .env with new password

---

## Testing Email Sending

### Test Script

Create `test_email.py`:

```python
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def test_email():
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    smtp_from = os.getenv('SMTP_FROM')
    
    if not all([smtp_host, smtp_user, smtp_password]):
        print("❌ SMTP not configured in .env")
        return
    
    # Test email
    msg = MIMEText("This is a test email from Healthcare OTP system.")
    msg['Subject'] = 'Test Email'
    msg['From'] = smtp_from
    msg['To'] = smtp_user  # Send to yourself
    
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"✅ Test email sent successfully to {smtp_user}")
        print("Check your inbox!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    test_email()
```

Run test:
```bash
python test_email.py
```

---

## Gmail Specific Notes

### Daily Sending Limits

- **Free Gmail**: 500 emails/day
- **Google Workspace**: 2000 emails/day

For this OTP system, this is more than enough.

### Less Secure Apps

**Don't enable "Less secure app access"** - Use app passwords instead.

### SMTP Settings

```
Host: smtp.gmail.com
Port: 587 (TLS) or 465 (SSL)
Security: STARTTLS or SSL/TLS
```

---

## Quick Start Checklist

- [ ] Enable 2FA on Gmail
- [ ] Generate app password
- [ ] Add SMTP settings to .env
- [ ] Restart server
- [ ] Test sending OTP
- [ ] Check patient email inbox
- [ ] Verify OTP works

---

## Summary

**Without SMTP configured:**
- ✅ OTP printed to console
- ✅ Works for development
- ❌ Patient doesn't receive email

**With SMTP configured:**
- ✅ OTP sent to patient email
- ✅ Professional email template
- ✅ Ready for production
- ✅ Patient receives email instantly

**Setup time:** 5 minutes
**Cost:** Free (using Gmail)
