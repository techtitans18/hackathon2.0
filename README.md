# Healthcare Blockchain API + Role-Based Frontend

FastAPI backend for healthcare records with:
- MongoDB persistence
- Local file storage for uploaded medical files
- Append-only blockchain metadata chain for record integrity
- Google Sign-In with managed role access (`admin`, `hospital`, `patient`)
- Separate frontend pages per role

## Run
```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Environment Setup
Create `.env` in project root (copy from `.env.example`):

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-host>/?retryWrites=true&w=majority
MONGO_DB_NAME=healthcare_blockchain
GOOGLE_CLIENT_ID=<your-google-oauth-web-client-id>.apps.googleusercontent.com
AUTH_SECRET_KEY=<long-random-secret-at-least-32-characters>
ADMIN_BOOTSTRAP_EMAILS=<first-admin-email@example.com>
```

Notes:
- Use normal MongoDB driver URI (`mongodb+srv://...`), not Atlas SQL endpoint URLs.
- If your MongoDB password contains special characters, URL-encode it.
- Add your current IP to MongoDB Atlas Network Access.
- `GOOGLE_CLIENT_ID` must be a Web client ID from Google Cloud Console.
- `AUTH_SECRET_KEY` must be at least 32 characters.
- `ADMIN_BOOTSTRAP_EMAILS` is a comma-separated list of Google emails allowed to bootstrap the first admin login.

## Role Access Model
- `admin`
  - Register hospitals
  - Provision and manage user access (`/admin/users`)
- `hospital`
  - Register patients (name, phone, age, email)
  - Add medical records for patients
  - **Patient Access (OTP)**: Verify walk-in patients via email OTP to view their records
  - Emergency access to critical patient information
- `patient`
  - View only their own records
  - Download only their own files

## Frontend Routes
- Login: `http://127.0.0.1:8000/app`
- Admin page: `http://127.0.0.1:8000/app/admin`
- Hospital page: `http://127.0.0.1:8000/app/hospital`
- Patient page: `http://127.0.0.1:8000/app/patient`

Static files are served from `/static/*`.

## API Endpoints
- Common auth
  - `POST /auth/google`
  - `GET /auth/google/config`
  - `GET /auth/session`
  - `POST /auth/logout`
- Admin
  - `POST /register_hospital`
  - `GET /admin/users`
  - `POST /admin/users`
- Hospital
  - `POST /register_patient`
  - `POST /add_record` (multipart/form-data)
  - `POST /patient_access/send_otp` (send OTP for patient verification)
  - `POST /patient_access/verify_otp` (verify OTP and access records)
- Patient/Admin read endpoints
  - `GET /patient/{HealthID}`
  - `GET /patient/me` (patient only)
  - `GET /record/file/{stored_file_name}`
  - `GET /record/summary/{summary_stored_file_name}`
- Admin-only read endpoints
  - `GET /record/hash/{record_hash}`
  - `GET /blockchain`

## Features

### 1. Patient Access with OTP Verification
Hospital staff can provide secure access to patient records when patients visit:
- **Cross-Hospital Access**: ANY hospital can access ANY patient (with OTP consent)
- Search by Health ID, Mobile Number, or Email Address
- Email OTP verification (6-digit, 10-minute expiry)
- View complete patient profile and medical records from ALL hospitals
- Download original files and AI summaries
- See [PATIENT_ACCESS_OTP.md](PATIENT_ACCESS_OTP.md) and [CROSS_HOSPITAL_ACCESS.md](CROSS_HOSPITAL_ACCESS.md) for details

### 2. AI-Powered Medical Summaries
- Automatic summarization of uploaded medical reports (PDF/text)
- Uses BART model (facebook/bart-large-cnn) running offline
- Extracts text from PDFs using PyPDF2
- Generates 30-120 word summaries
- Stored as separate downloadable files

### 3. Blockchain Integrity
- Append-only blockchain for record metadata
- SHA-256 hashing for file integrity
- Verification endpoint to check chain validity
- Tamper-proof audit trail

### 4. Emergency Access
- Quick patient lookup by Health ID, Phone, or Name+DOB
- Critical information display (allergies, diseases, surgeries)
- Blockchain verification status
- Access logging for audit compliance
