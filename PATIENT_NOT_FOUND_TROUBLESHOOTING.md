# Patient Not Found - Troubleshooting Guide

## Common Causes & Solutions

### 1. Hospital ID Mismatch ⚠️ MOST COMMON

**Problem**: Patient registered by different hospital

**Check**:
```python
# In MongoDB, check:
db.patients.findOne({"email": "patient@example.com"})

# Look at:
{
  "health_id": "ABC123",
  "created_by_hospital_id": "HOSP001"  # ← This must match YOUR hospital ID
}
```

**Solution**:
- You can only access patients registered by YOUR hospital
- If patient registered by Hospital A, Hospital B cannot access
- This is by design for security

**Fix**: Register the patient with YOUR hospital account

---

### 2. Wrong Search Value

**Problem**: Typo or format mismatch

**Common Issues**:

**Health ID**:
- Stored: `ABC123XYZ`
- Searching: `abc123xyz` ← Case matters!
- **Fix**: Use exact case as stored

**Phone**:
- Stored: `+1234567890`
- Searching: `1234567890` ← Missing +
- **Fix**: Include country code if stored with it

**Email**:
- Stored: `patient@example.com`
- Searching: `Patient@Example.com` ← Should work (case-insensitive)
- **Fix**: System converts to lowercase automatically

---

### 3. Patient Not Registered Yet

**Problem**: Patient doesn't exist in database

**Check**:
```bash
# Run debug script
python debug_patient_search.py

# Select option 1 to see all patients
```

**Solution**: Register patient first via "Register Patient" tab

---

### 4. Patient Has No Email

**Problem**: Patient registered without email field

**Error**: "Patient email not found. Cannot send OTP."

**Solution**: 
1. Update patient record with email
2. Or re-register patient with email

---

## Quick Debug Steps

### Step 1: Verify Patient Exists
```bash
python debug_patient_search.py
# Select option 1
# This shows ALL patients in database
```

### Step 2: Check Your Hospital ID
```javascript
// In browser console (Hospital Dashboard)
localStorage.getItem('access_token')
// Decode JWT to see your hospital_id
```

### Step 3: Match Hospital IDs
```
Your Hospital ID: HOSP001
Patient's Hospital ID: HOSP001  ✓ Match
```

If they don't match → You cannot access this patient

---

## Testing Checklist

Before searching for patient:

- [ ] Patient is registered in system
- [ ] Patient registered by YOUR hospital
- [ ] You have correct Health ID / Phone / Email
- [ ] Search value matches exact format
- [ ] Patient has email address (for OTP)
- [ ] You're logged in as hospital user

---

## Debug Commands

### Check All Patients
```bash
python debug_patient_search.py
# Option 1: Debug patient search
```

### Check Database Connection
```bash
python -c "from database.db import get_patient_collection; print(get_patient_collection().count_documents({}))"
```

### Check Your Hospital ID
```bash
# In Hospital Dashboard, open browser console:
console.log(JSON.parse(atob(localStorage.getItem('access_token').split('.')[0])))
```

---

## Example Scenarios

### Scenario 1: Hospital ID Mismatch
```
Search: health_id = "ABC123"
Result: ✗ Patient not found

Debug:
- Patient exists: ✓
- Patient's hospital: HOSP002
- Your hospital: HOSP001
- Reason: Hospital mismatch ✗

Solution: This patient belongs to another hospital
```

### Scenario 2: Wrong Phone Format
```
Search: mobile = "1234567890"
Result: ✗ Patient not found

Debug:
- Patient exists: ✓
- Stored phone: "+1234567890"
- Searched: "1234567890"
- Reason: Missing country code ✗

Solution: Search with "+1234567890"
```

### Scenario 3: Case Sensitivity (Health ID)
```
Search: health_id = "abc123xyz"
Result: ✗ Patient not found

Debug:
- Patient exists: ✓
- Stored ID: "ABC123XYZ"
- Searched: "abc123xyz"
- Reason: Case mismatch ✗

Solution: Use "ABC123XYZ" (exact case)
```

---

## API Error Messages Explained

### "Patient not found with provided information"
- Patient doesn't exist in database
- OR wrong search value
- OR hospital ID mismatch

### "Patient is not registered with your hospital"
- Patient exists but belongs to different hospital
- Security feature - cannot access other hospitals' patients

### "Patient email not found. Cannot send OTP"
- Patient record has no email field
- Need to update patient with email address

---

## Quick Fixes

### Fix 1: Register Patient with Your Hospital
```
1. Go to "Register Patient" tab
2. Fill in patient details
3. Include email address
4. Submit
5. Now you can access via OTP
```

### Fix 2: Use Exact Search Values
```
1. Run debug script to see exact values
2. Copy exact Health ID / Phone / Email
3. Paste into search (don't type)
4. Try again
```

### Fix 3: Check Hospital ID
```
1. Verify you're logged in as hospital user
2. Check your hospital_id in JWT token
3. Ensure patient created_by_hospital_id matches
```

---

## Still Not Working?

Run full debug:
```bash
python debug_patient_search.py
# Select option 4 (All of the above)
```

This will:
1. Show all patients in database
2. Let you test search with your values
3. Check hospital ID match
4. Verify email exists
5. Show database indexes
6. List common issues

---

## Contact Support

If issue persists after debugging:

1. Run debug script and save output
2. Note exact error message
3. Provide:
   - Search type used
   - Search value used
   - Your hospital ID
   - Debug script output
