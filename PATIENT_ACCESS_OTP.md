# Patient Access with OTP Verification

## Overview
Hospital staff can provide patients with secure access to their medical records when they visit the hospital. The system uses email OTP verification to ensure only authorized access.

## How It Works

### 1. Patient Arrives at Hospital
When a patient visits the hospital, staff can look them up using:
- **Health ID** - Unique patient identifier
- **Mobile Number** - Registered phone number
- **Email Address** - Registered email address

### 2. OTP Verification Flow
1. Hospital staff enters patient's Health ID or mobile number
2. System sends 6-digit OTP to patient's registered email
3. Patient receives OTP on their email (masked for privacy: abc***@example.com)
4. Staff enters OTP provided by patient
5. Upon successful verification, patient's full profile and medical records are displayed

### 3. Security Features
- **OTP Expiry**: OTPs expire after 10 minutes
- **Attempt Limit**: Maximum 3 verification attempts per OTP
- **Hospital Verification**: Only patients registered with that specific hospital can be accessed
- **Email Masking**: Patient email is partially hidden for privacy
- **In-Memory Storage**: OTPs stored temporarily (use Redis for production)

## API Endpoints

### Send OTP
```http
POST /patient_access/send_otp
Authorization: Bearer <hospital_token>
Content-Type: application/json

{
  "search_type": "health_id",  // or "mobile" or "email"
  "search_value": "ABC123XYZ"
}
```

**Response:**
```json
{
  "message": "OTP sent successfully to patient's email.",
  "email_masked": "abc***@example.com",
  "expires_in_minutes": 10
}
```

### Verify OTP
```http
POST /patient_access/verify_otp
Authorization: Bearer <hospital_token>
Content-Type: application/json

{
  "search_type": "health_id",  // or "mobile" or "email"
  "search_value": "ABC123XYZ",
  "otp": "123456"
}
```

**Response:**
```json
{
  "patient": {
    "health_id": "ABC123XYZ",
    "name": "John Doe",
    "age": 45,
    "phone": "+1234567890",
    "email": "john@example.com",
    "blood_group": "O+"
  },
  "records": [
    {
      "record_type": "Lab Report",
      "description": "Blood test results",
      "file_name": "blood_test.pdf",
      "download_url": "/record/file/uuid_blood_test.pdf",
      "summary_download_url": "/record/summary/uuid_summary.txt",
      "record_hash": "abc123...",
      "timestamp": "2024-01-15T10:30:00Z",
      "hospital_id": "HOSP123"
    }
  ]
}
```

## Frontend Usage

### Hospital Dashboard
Navigate to **Patient Access (OTP)** tab:

1. **Select Search Type**: Health ID, Mobile Number, or Email Address
2. **Enter Value**: Patient's Health ID, mobile number, or email
3. **Send OTP**: Click "Send OTP" button
4. **Patient Receives Email**: Patient checks their email for 6-digit OTP
5. **Enter OTP**: Staff enters OTP provided by patient
6. **Verify**: Click "Verify OTP" to access records
7. **View Records**: Patient profile and all medical records displayed

### Features Displayed
- Patient Information (Health ID, Name, Age, Phone, Email, Blood Group)
- Medical Records List with:
  - Record type and description
  - Upload date
  - Download buttons for original file and AI summary
  - Blockchain hash verification

## Email Configuration (Production)

For production deployment, configure SMTP in `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=noreply@hospital.com
```

### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password in `SMTP_PASSWORD`

### Update Code
In `routes/patient_access_routes.py`, replace `_send_otp_email()` function:

```python
import smtplib
from email.mime.text import MIMEText
import os

def _send_otp_email(email: str, otp: str) -> None:
    msg = MIMEText(f"Your healthcare access OTP is: {otp}\n\nValid for 10 minutes.")
    msg['Subject'] = 'Healthcare Access OTP'
    msg['From'] = os.getenv('SMTP_FROM', 'noreply@hospital.com')
    msg['To'] = email
    
    with smtplib.SMTP(os.getenv('SMTP_HOST', 'smtp.gmail.com'), 
                      int(os.getenv('SMTP_PORT', 587))) as server:
        server.starttls()
        server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
        server.send_message(msg)
```

## Production Recommendations

### 1. Use Redis for OTP Storage
Replace in-memory `_otp_store` with Redis:

```python
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def _store_otp(key: str, otp: str, email: str) -> datetime:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES)
    redis_client.setex(
        key, 
        OTP_EXPIRY_MINUTES * 60,
        json.dumps({"otp": otp, "email": email, "attempts": 0})
    )
    return expires_at
```

### 2. Rate Limiting
Add rate limiting to prevent OTP spam:

```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/patient_access/send_otp")
@limiter.limit("5/minute")
def send_patient_access_otp(...):
    ...
```

### 3. Audit Logging
Log all patient access attempts:

```python
access_log = {
    "hospital_id": current_user.hospital_id,
    "patient_health_id": patient["health_id"],
    "access_type": "otp_verification",
    "timestamp": datetime.now(timezone.utc),
    "success": True
}
get_access_logs_collection().insert_one(access_log)
```

## Testing

### Development Mode
Currently, OTPs are printed to console:
```
[OTP EMAIL] To: patient@example.com, OTP: 123456
```

Check server logs to see the OTP for testing.

### Test Flow
1. Register a patient with valid email
2. Go to Hospital Dashboard → Patient Access (OTP)
3. Search by Health ID or mobile
4. Check server console for OTP
5. Enter OTP and verify
6. View patient records

## Security Considerations

✅ **Implemented:**
- OTP expiry (10 minutes)
- Attempt limiting (3 tries)
- Hospital-patient relationship verification
- Email masking for privacy
- Secure token-based authentication

⚠️ **Production TODO:**
- Implement actual email sending (SMTP/AWS SES)
- Use Redis for distributed OTP storage
- Add rate limiting on OTP requests
- Implement comprehensive audit logging
- Add IP-based access controls
- Consider SMS OTP as backup option

## Use Cases

1. **Walk-in Patients**: Quick access to records during hospital visit
2. **Emergency Situations**: Fast verification when patient can't log in
3. **Consultation**: Doctor needs immediate access to patient history
4. **Lab Results**: Patient wants to view recent test results at hospital
5. **Prescription Pickup**: Verify patient identity before dispensing medication
