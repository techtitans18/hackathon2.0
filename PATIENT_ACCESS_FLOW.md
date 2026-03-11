# Patient Access OTP Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PATIENT VISITS HOSPITAL                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 1: Hospital Staff Searches for Patient                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  Search Options:                                                         │
│  • Health ID: ABC123XYZ                                                  │
│  • Mobile Number: +1234567890                                            │
│  • Email Address: patient@example.com                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 2: System Validates & Sends OTP                                   │
│  ─────────────────────────────────────────────────────────────────────  │
│  ✓ Check if patient exists                                              │
│  ✓ Verify patient belongs to this hospital                              │
│  ✓ Generate 6-digit OTP (e.g., 123456)                                  │
│  ✓ Store OTP with 10-minute expiry                                      │
│  ✓ Send OTP to patient's email                                          │
│  ✓ Display masked email: abc***@example.com                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 3: Patient Receives OTP Email                                     │
│  ─────────────────────────────────────────────────────────────────────  │
│  To: patient@example.com                                                 │
│  Subject: Healthcare Access OTP                                          │
│  Body: Your OTP is: 123456 (Valid for 10 minutes)                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 4: Patient Provides OTP to Staff                                  │
│  ─────────────────────────────────────────────────────────────────────  │
│  Patient shows email or tells OTP: "123456"                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 5: Staff Enters OTP for Verification                              │
│  ─────────────────────────────────────────────────────────────────────  │
│  [1] [2] [3] [4] [5] [6]  [Verify OTP]                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 6: System Verifies OTP                                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  ✓ Check OTP matches stored value                                       │
│  ✓ Verify OTP not expired (< 10 minutes)                                │
│  ✓ Check attempts < 3                                                   │
│  ✓ Delete OTP after successful verification                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 7: Display Patient Records                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Patient Information                                              │   │
│  │ ─────────────────────────────────────────────────────────────── │   │
│  │ Health ID: ABC123XYZ          Blood Group: O+                   │   │
│  │ Name: John Doe                Age: 45                            │   │
│  │ Phone: +1234567890            Email: john@example.com           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Medical Records (3)                                              │   │
│  │ ─────────────────────────────────────────────────────────────── │   │
│  │ 📄 Lab Report - Blood Test (2024-01-15)                         │   │
│  │    [Download File] [AI Summary]                                  │   │
│  │                                                                   │   │
│  │ 📄 X-Ray - Chest (2024-01-10)                                    │   │
│  │    [Download File] [AI Summary]                                  │   │
│  │                                                                   │   │
│  │ 📄 Prescription - Diabetes Medication (2024-01-05)               │   │
│  │    [Download File] [AI Summary]                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Security Flow

```
┌──────────────────┐
│  Hospital Staff  │
│   (Logged In)    │
└────────┬─────────┘
         │ JWT Token
         ▼
┌──────────────────────────────────────┐
│  POST /patient_access/send_otp       │
│  ─────────────────────────────────   │
│  • Verify hospital authentication    │
│  • Check patient-hospital relation   │
│  • Generate secure 6-digit OTP       │
│  • Hash search key (SHA-256)         │
│  • Store: {otp, email, expiry}       │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  Email Service (SMTP/AWS SES)        │
│  ─────────────────────────────────   │
│  To: patient@example.com             │
│  OTP: 123456                          │
│  Expiry: 10 minutes                   │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  POST /patient_access/verify_otp     │
│  ─────────────────────────────────   │
│  • Verify hospital authentication    │
│  • Hash search key (SHA-256)         │
│  • Check OTP match                   │
│  • Verify not expired                │
│  • Check attempt count < 3           │
│  • Delete OTP on success             │
│  • Return patient + records          │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  Patient Records Displayed           │
│  ─────────────────────────────────   │
│  • Full patient profile              │
│  • All medical records               │
│  • Download links                    │
│  • AI summaries                      │
└──────────────────────────────────────┘
```

## Error Handling

```
┌─────────────────────────────────────┐
│  Possible Errors & Responses        │
├─────────────────────────────────────┤
│                                     │
│  ❌ Patient Not Found               │
│  → 404: "Patient not found"         │
│                                     │
│  ❌ Wrong Hospital                  │
│  → 403: "Not registered with        │
│          your hospital"             │
│                                     │
│  ❌ No Email on Record              │
│  → 400: "Patient email not found"   │
│                                     │
│  ❌ Invalid OTP                     │
│  → 401: "Invalid or expired OTP"    │
│                                     │
│  ❌ OTP Expired (>10 min)           │
│  → 401: "Invalid or expired OTP"    │
│                                     │
│  ❌ Too Many Attempts (>3)          │
│  → 401: "Invalid or expired OTP"    │
│                                     │
└─────────────────────────────────────┘
```

## Data Flow

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Frontend   │      │   Backend    │      │   Database   │
│  (Hospital)  │      │   (FastAPI)  │      │  (MongoDB)   │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       │ 1. Send OTP Request │                     │
       ├────────────────────>│                     │
       │                     │ 2. Find Patient     │
       │                     ├────────────────────>│
       │                     │<────────────────────┤
       │                     │ 3. Patient Data     │
       │                     │                     │
       │                     │ 4. Generate OTP     │
       │                     │    Store in Memory  │
       │                     │                     │
       │                     │ 5. Send Email       │
       │                     ├─────────────────────> (SMTP)
       │                     │                     │
       │ 6. OTP Sent         │                     │
       │<────────────────────┤                     │
       │                     │                     │
       │ 7. Verify OTP       │                     │
       ├────────────────────>│                     │
       │                     │ 8. Check OTP        │
       │                     │    (In Memory)      │
       │                     │                     │
       │                     │ 9. Get Records      │
       │                     ├────────────────────>│
       │                     │<────────────────────┤
       │                     │ 10. Records Data    │
       │                     │                     │
       │ 11. Patient+Records │                     │
       │<────────────────────┤                     │
       │                     │                     │
```
