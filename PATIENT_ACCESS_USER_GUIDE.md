# Patient Access OTP - User Guide

## For Hospital Staff

### Step 1: Access the Feature
1. Login to Hospital Dashboard
2. Click on **"Patient Access (OTP)"** tab
3. You'll see the patient search form

### Step 2: Search for Patient
**Option A: Search by Health ID**
- Select "Health ID" from dropdown
- Enter patient's Health ID (e.g., ABC123XYZ)
- Click "Send OTP"

**Option B: Search by Mobile Number**
- Select "Mobile Number" from dropdown
- Enter patient's mobile number (e.g., +1234567890)
- Click "Send OTP"

**Option C: Search by Email Address**
- Select "Email Address" from dropdown
- Enter patient's email (e.g., patient@example.com)
- Click "Send OTP"

### Step 3: OTP Sent Confirmation
After clicking "Send OTP", you'll see:
```
✅ OTP sent to abc***@example.com
```
- Patient's email is masked for privacy
- OTP is valid for 10 minutes
- Patient will receive email with 6-digit code

### Step 4: Get OTP from Patient
Ask the patient to:
1. Check their email inbox
2. Look for email with subject "Healthcare Access OTP"
3. Read the 6-digit OTP code
4. Tell you the code

### Step 5: Enter OTP
- Type the 6-digit OTP in the input field
- The field only accepts numbers
- Maximum 6 digits
- Click "Verify OTP"

### Step 6: View Patient Records
Upon successful verification, you'll see:

**Patient Information Card**
- Health ID
- Full Name
- Age
- Phone Number
- Email Address
- Blood Group (highlighted in red)

**Medical Records Section**
- List of all medical records
- Each record shows:
  - Record type (Lab Report, X-Ray, Prescription, etc.)
  - Description
  - Upload date
  - Download buttons:
    - 📄 Download File (original document)
    - 📝 AI Summary (auto-generated summary)
  - Blockchain hash (for verification)

### Step 7: Download Files
- Click "📄 Download File" to get original medical document
- Click "📝 AI Summary" to get AI-generated summary
- Files open in new tab or download automatically

### Step 8: New Search
- Click "New Search" button to search for another patient
- Form resets and you can start over

## Common Scenarios

### Scenario 1: Patient Forgot Health ID
**Solution**: Use mobile number or email search
1. Select "Mobile Number" or "Email Address"
2. Enter patient's phone number or email
3. Continue with OTP verification

### Scenario 2: OTP Expired
**Symptoms**: Error message "Invalid or expired OTP"
**Solution**: 
1. Click "Resend OTP" link
2. New OTP will be sent
3. Ask patient for new code

### Scenario 3: Wrong OTP Entered
**Symptoms**: Error message "Invalid or expired OTP"
**Solution**:
1. Verify OTP with patient again
2. Re-enter correct OTP
3. Maximum 3 attempts allowed
4. After 3 failed attempts, request new OTP

### Scenario 4: Patient Not Found
**Symptoms**: Error "Patient not found with provided information"
**Possible Causes**:
- Wrong Health ID, mobile number, or email
- Patient not registered with your hospital
- Typo in search value

**Solution**:
1. Verify information with patient
2. Check patient registration records
3. Register patient if not in system

### Scenario 5: Patient Has No Email
**Symptoms**: Error "Patient email not found. Cannot send OTP"
**Solution**:
1. Update patient profile with email address
2. Use alternative access method (Emergency Access tab)

## Tips for Efficient Use

### ✅ Best Practices
1. **Verify Patient Identity**: Always confirm patient identity before searching
2. **Privacy**: Don't share OTP with anyone except the patient
3. **Quick Process**: Complete verification within 10 minutes
4. **Double Check**: Verify Health ID/mobile number before sending OTP
5. **Patient Present**: Ensure patient is present to provide OTP

### ⚠️ Security Reminders
1. **Never share** your hospital login credentials
2. **Don't write down** patient OTPs
3. **Verify patient** is the actual person before showing records
4. **Log out** when leaving workstation
5. **Report suspicious** access attempts

## Troubleshooting

### Problem: "Send OTP" button not working
**Check**:
- [ ] Entered Health ID or mobile number
- [ ] Selected correct search type
- [ ] Internet connection active
- [ ] Still logged in (check session)

### Problem: OTP field disabled
**Reason**: OTP must be exactly 6 digits
**Solution**: Enter all 6 digits to enable "Verify OTP" button

### Problem: Can't download files
**Check**:
- [ ] Pop-up blocker disabled
- [ ] Browser allows downloads
- [ ] File exists in system
- [ ] Internet connection stable

### Problem: Records not showing
**Possible Causes**:
- Patient has no medical records yet
- Records from different hospital
- Database connection issue

**Solution**:
1. Verify patient has records in system
2. Check if records uploaded by your hospital
3. Contact IT support if issue persists

## Email Template (What Patient Receives)

```
From: noreply@hospital.com
To: patient@example.com
Subject: Healthcare Access OTP

Dear Patient,

Your healthcare access OTP is: 123456

This code is valid for 10 minutes.

If you did not request this code, please contact the hospital immediately.

Thank you,
Hospital Name
```

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│  PATIENT ACCESS OTP - QUICK GUIDE       │
├─────────────────────────────────────────┤
│                                         │
│  1. Select search type                  │
│     • Health ID                         │
│     • Mobile Number                     │
│     • Email Address                     │
│                                         │
│  2. Enter patient information           │
│                                         │
│  3. Click "Send OTP"                    │
│                                         │
│  4. Patient receives email              │
│     (Valid for 10 minutes)              │
│                                         │
│  5. Get OTP from patient                │
│                                         │
│  6. Enter 6-digit OTP                   │
│                                         │
│  7. Click "Verify OTP"                  │
│                                         │
│  8. View patient records                │
│                                         │
│  9. Download files if needed            │
│                                         │
│  10. Click "New Search" for next        │
│      patient                            │
│                                         │
└─────────────────────────────────────────┘
```

## Support Contact

For technical issues or questions:
- **IT Support**: Contact your hospital IT department
- **System Admin**: Contact system administrator
- **Emergency**: Use "Emergency Access" tab for critical situations

## Training Checklist

Before using Patient Access OTP, ensure you can:
- [ ] Login to Hospital Dashboard
- [ ] Navigate to Patient Access tab
- [ ] Search by Health ID
- [ ] Search by Mobile Number
- [ ] Search by Email Address
- [ ] Understand OTP expiry (10 minutes)
- [ ] Handle OTP verification errors
- [ ] View patient records
- [ ] Download medical files
- [ ] Download AI summaries
- [ ] Start new search
- [ ] Handle common errors
- [ ] Maintain patient privacy
- [ ] Follow security protocols

## Frequently Asked Questions

**Q: How long is the OTP valid?**
A: 10 minutes from the time it's sent.

**Q: How many times can I try entering OTP?**
A: Maximum 3 attempts. After that, request a new OTP.

**Q: Can I access patients from other hospitals?**
A: No, you can only access patients registered with your hospital.

**Q: What if patient doesn't have email?**
A: Update patient profile with email, or use Emergency Access for urgent cases.

**Q: Can I resend OTP?**
A: Yes, click "Resend OTP" link to send a new code.

**Q: Is the OTP sent via SMS?**
A: Currently only email. SMS option may be added in future.

**Q: What if I enter wrong Health ID?**
A: You'll get "Patient not found" error. Verify and try again.

**Q: Can patient access their own records this way?**
A: No, this is for hospital staff. Patients should use Patient Dashboard.

**Q: Are access attempts logged?**
A: Yes, all access is logged for audit and compliance.

**Q: What happens after successful verification?**
A: You can view all patient records and download files. Session remains active until you click "New Search".
