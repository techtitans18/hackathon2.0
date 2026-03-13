# Healthcare Blockchain - Complete Program Structure

## 📁 Project Architecture

```
healthcare_blockchain/
│
├── 🔧 Backend (FastAPI + Python)
│   ├── main.py                    # Application entry point
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables
│   │
│   ├── app/                       # Application modules
│   │   ├── ai_summary/           # AI medical summarization
│   │   │   ├── ai_routes.py      # AI API endpoints
│   │   │   ├── summarizer.py     # BART model integration
│   │   │   └── security_policy.py # AI access control
│   │   │
│   │   └── emergency/            # Emergency access system
│   │       ├── emergency_routes.py    # Emergency endpoints
│   │       ├── emergency_service.py   # Business logic
│   │       ├── emergency_models.py    # Data models
│   │       └── emergency_security.py  # Access control
│   │
│   ├── blockchain/               # Blockchain implementation
│   │   ├── blockchain.py         # Core blockchain logic
│   │   └── verify.py             # Integrity verification
│   │
│   ├── database/                 # MongoDB connection
│   │   └── db.py                 # Database setup & collections
│   │
│   ├── models/                   # Pydantic data models
│   │   ├── patient.py            # Patient schemas
│   │   ├── hospital.py           # Hospital schemas
│   │   └── record.py             # Record schemas
│   │
│   ├── routes/                   # API route handlers
│   │   ├── auth_routes.py        # Authentication (Google OAuth)
│   │   ├── admin_routes.py       # Admin management
│   │   ├── hospital_routes.py    # Hospital operations
│   │   ├── patient_routes.py     # Patient operations
│   │   └── record_routes.py      # Medical records
│   │
│   └── records/                  # Local file storage
│       ├── {uuid}_filename.pdf   # Original files
│       └── {uuid}_summary.txt    # AI summaries
│
└── 🎨 Frontend (React + Vite)
    ├── package.json              # Node dependencies
    ├── vite.config.js            # Vite configuration
    │
    └── src/
        ├── main.jsx              # React entry point
        ├── App.jsx               # Main app component
        │
        ├── pages/                # Dashboard pages
        │   ├── Login.jsx         # Google OAuth login
        │   ├── AdminDashboard.jsx      # Admin panel
        │   ├── HospitalDashboard.jsx   # Hospital panel
        │   ├── PatientDashboard.jsx    # Patient panel
        │   ├── DoctorDashboard.jsx     # Doctor panel
        │   ├── EmergencyDashboard.jsx  # Emergency panel
        │   └── PatientWorkspace.jsx    # Patient workspace
        │
        ├── components/           # Reusable components
        │   ├── Navbar.jsx              # Navigation bar
        │   ├── ErrorBoundary.jsx       # Error handling
        │   ├── UserManagement.jsx      # Admin user CRUD
        │   ├── AddHospital.jsx         # Add hospital form
        │   ├── UpdateHospital.jsx      # Update hospital
        │   ├── HospitalRegistration.jsx # Hospital self-register
        │   ├── PatientRegistration.jsx  # Register patient
        │   ├── UploadRecord.jsx        # Upload medical files
        │   ├── RecordTable.jsx         # Display records
        │   ├── BlockchainViewer.jsx    # View blockchain
        │   ├── EHealthCard.jsx         # Digital health card
        │   ├── EmergencySearch.jsx     # Search patients
        │   ├── EmergencyProfile.jsx    # Emergency data view
        │   └── EmergencyUpdateData.jsx # Update emergency info
        │
        ├── services/             # API integration
        │   └── api.js            # Axios HTTP client
        │
        ├── styles/               # CSS styling
        │   └── styles.css        # Global styles
        │
        └── utils/                # Helper functions
            └── helpers.js        # Utility functions
```

---

## 🔐 Authentication Flow

```
User → Google OAuth → Backend Verification → JWT Token → Role-Based Access
```

### Process:
1. User clicks "Sign in with Google"
2. Google returns credential token
3. Backend verifies with Google API
4. Backend checks user in MongoDB
5. Backend generates JWT token (8-hour expiry)
6. Frontend stores token in localStorage
7. All API calls include JWT in Authorization header

---

## 👥 User Roles & Permissions

### 1. **Admin** 🔑
**Can:**
- Register hospitals (auto-generates HospitalID)
- Create/update user accounts
- Assign roles (admin/hospital/patient)
- View all blockchain records
- Monitor system integrity

**Cannot:**
- Upload medical records
- Register patients

### 2. **Hospital** 🏥
**Can:**
- Register patients (auto-generates HealthID)
- Upload medical records with files
- Search patient records
- View blockchain
- Access emergency data

**Cannot:**
- Create other hospitals
- Manage users
- View other hospitals' patients (unless emergency)

### 3. **Patient** 👤
**Can:**
- View own medical records
- Download own files
- View AI summaries
- Access e-health card
- See own emergency data

**Cannot:**
- View other patients' records
- Upload records
- Access blockchain

### 4. **Doctor** 👨‍⚕️
**Can:**
- View blockchain records
- Search by record hash
- View medical data

**Cannot:**
- Upload records
- Register patients

### 5. **Emergency** 🚑
**Can:**
- Search patients (health_id/phone/name+DOB)
- View critical emergency data
- Update emergency information
- All access is audit-logged

**Cannot:**
- View full medical records
- Upload files

---

## 🗄️ Database Structure (MongoDB)

### Collections:

#### 1. **patients**
```javascript
{
  health_id: "ABC123DEF456",        // SHA256(email|dob)
  name: "John Doe",
  age: 35,
  phone: "1234567890",
  email: "john@example.com",
  dob: "1989-05-15",
  blood_group: "O+",
  photo_url: "https://...",
  created_at: ISODate,
  created_by_hospital_id: "HOSP123"
}
```

#### 2. **hospitals**
```javascript
{
  hospital_id: "HOSP123ABC",        // SHA256(name|type)
  hospital_name: "City General Hospital",
  hospital_type: "General",
  created_at: ISODate
}
```

#### 3. **records**
```javascript
{
  health_id: "ABC123DEF456",
  hospital_id: "HOSP123ABC",
  record_type: "X-Ray",
  description: "Chest X-Ray findings...",
  file_name: "xray.pdf",
  stored_file_name: "uuid_xray.pdf",
  summary_stored_file_name: "uuid_summary.txt",
  record_hash: "sha256_of_file",
  timestamp: ISODate
}
```

#### 4. **users**
```javascript
{
  email: "user@example.com",
  subject: "google_oauth_sub",
  name: "User Name",
  role: "hospital",                 // admin/hospital/patient
  health_id: null,                  // if patient
  hospital_id: "HOSP123",           // if hospital
  is_active: true,
  created_at: ISODate,
  last_login_at: ISODate
}
```

#### 5. **emergency_data**
```javascript
{
  health_id: "ABC123DEF456",
  blood_group: "O+",
  allergies: ["Penicillin", "Peanuts"],
  diseases: ["Diabetes", "Hypertension"],
  surgeries: ["Appendectomy"],
  emergency_contact: "9876543210",
  blockchain_hash: "sha256_hash",   // For integrity
  updated_at: ISODate
}
```

#### 6. **emergency_logs**
```javascript
{
  hospital_id: "HOSP123",
  health_id: "ABC123DEF456",
  timestamp: ISODate,
  action: "Emergency Access"
}
```

---

## ⛓️ Blockchain Structure

### Block Format:
```javascript
{
  index: 0,                         // Block number
  timestamp: "2024-01-15T10:30:00Z",
  HealthID: "ABC123DEF456",
  HospitalID: "HOSP123ABC",
  RecordType: "X-Ray",
  RecordHash: "sha256_of_file",     // File integrity
  previous_hash: "hash_of_block_0", // Chain link
  hash: "sha256_of_this_block"      // Block integrity
}
```

### Chain Structure:
```
Genesis Block (index: 0)
    ↓ (previous_hash)
Block 1 (Medical Record 1)
    ↓ (previous_hash)
Block 2 (Medical Record 2)
    ↓ (previous_hash)
Block 3 (Medical Record 3)
```

### Integrity Verification:
- Each block contains hash of previous block
- Tampering breaks the chain
- `/blockchain` endpoint includes integrity check
- Returns: `{ valid: true/false, invalid_blocks: [] }`

---

## 🤖 AI Summarization System

### Model: facebook/bart-large-cnn
**Location:** `models/ai_summary/facebook-bart-large-cnn/`

### Process:
1. Hospital uploads medical file
2. Backend extracts text from file
3. Combines: record_type + description + file_content
4. BART model generates 30-120 word summary
5. Summary saved as `.txt` file
6. Patient can view/download summary

### Security:
- ✅ Runs locally (no external API calls)
- ✅ Offline mode enabled
- ✅ No telemetry
- ✅ Access logged for audit
- ✅ Only hospital/doctor roles can trigger

---

## 🔄 Complete Workflow Example

### Scenario: Hospital uploads patient X-Ray

```
1. Admin creates hospital user
   POST /admin/users
   {
     email: "hospital@example.com",
     role: "hospital",
     hospital_name: "City Hospital",
     hospital_type: "General"
   }
   → Backend generates HospitalID: SHA256(name|type)
   → Creates hospital in database
   → Links user to hospital

2. Hospital logs in
   POST /auth/google
   { credential: "google_token" }
   → Backend verifies with Google
   → Returns JWT token
   → Frontend stores in localStorage

3. Hospital registers patient
   POST /register_patient
   {
     name: "John Doe",
     email: "john@example.com",
     dob: "1989-05-15",
     blood_group: "O+",
     allergies: ["Penicillin"],
     ...
   }
   → Backend generates HealthID: SHA256(email|dob)
   → Creates patient record
   → Creates emergency_data record
   → Creates user account for patient

4. Hospital uploads X-Ray
   POST /add_record (multipart/form-data)
   {
     HealthID: "ABC123",
     HospitalID: "HOSP123",
     record_type: "X-Ray",
     description: "Chest X-Ray...",
     file: xray.pdf
   }
   → Backend saves file: records/uuid_xray.pdf
   → Generates SHA256 hash of file
   → AI extracts text and generates summary
   → Saves summary: records/uuid_summary.txt
   → Creates blockchain block
   → Stores metadata in MongoDB

5. Patient logs in and views records
   GET /patient/me
   → Returns patient info + all records
   → Patient downloads file: GET /record/file/{filename}
   → Patient views summary: GET /record/summary/{filename}

6. Emergency access
   POST /emergency/search
   { search_type: "phone", value: "1234567890" }
   → Returns health_id and name
   
   POST /emergency/profile
   { health_id: "ABC123" }
   → Returns critical data (blood group, allergies, etc.)
   → Logs access in emergency_logs
```

---

## 🔐 Security Features

### 1. **Authentication**
- Google OAuth 2.0
- JWT tokens (8-hour expiry)
- Secure secret key (64+ chars)

### 2. **Authorization**
- Role-based access control (RBAC)
- Endpoint-level permissions
- Resource ownership validation

### 3. **Data Protection**
- Local file storage (no cloud)
- SHA-256 hashing for integrity
- Blockchain tamper detection
- Emergency access audit logs

### 4. **Input Validation**
- Pydantic models (backend)
- Form validation (frontend)
- Empty string checks
- Type validation

### 5. **Privacy**
- AI runs offline (no external calls)
- No telemetry
- Minimal data exposure
- Audit trails

---

## 📊 API Endpoints Summary

### Authentication
- `POST /auth/google` - Login with Google
- `GET /auth/google/config` - Get client ID
- `GET /auth/session` - Check session
- `POST /auth/logout` - Logout

### Admin
- `GET /admin/users` - List all users
- `POST /admin/users` - Create/update user
- `POST /register_hospital` - Register hospital
- `GET /hospitals` - List hospitals
- `PUT /hospitals/{id}` - Update hospital

### Hospital
- `POST /register_patient` - Register patient
- `POST /add_record` - Upload medical record
- `GET /blockchain` - View blockchain

### Patient
- `GET /patient/me` - Get own records
- `GET /patient/me/e-healthcard` - Get health card
- `GET /patient/{HealthID}` - Get patient by ID
- `GET /record/file/{filename}` - Download file
- `GET /record/summary/{filename}` - Download summary

### Emergency
- `POST /emergency/search` - Search patient
- `POST /emergency/profile` - Get emergency data
- `POST /emergency/upsert` - Update emergency data

### AI
- `GET /ai/health` - Check AI model status
- `POST /ai/summary` - Generate summary

---

## 🚀 Deployment Checklist

### Backend:
1. Install Python dependencies: `pip install -r requirements.txt`
2. Configure `.env` file
3. Start MongoDB
4. Download AI model (if offline mode)
5. Run: `uvicorn main:app --reload`

### Frontend:
1. Install Node dependencies: `npm install`
2. Configure API base URL
3. Run: `npm run dev`

### Production:
1. Set strong AUTH_SECRET_KEY
2. Configure MongoDB Atlas
3. Set up Google OAuth credentials
4. Enable HTTPS
5. Configure CORS properly
6. Set up backup system

---

## 🎯 Key Features

1. ✅ **Blockchain Integrity** - Tamper-proof medical records
2. ✅ **AI Summaries** - Automated medical report summaries
3. ✅ **Emergency Access** - Quick patient lookup with audit
4. ✅ **Role-Based Access** - Secure multi-user system
5. ✅ **Local Storage** - Privacy-first file storage
6. ✅ **E-Health Card** - Digital patient identification
7. ✅ **Audit Logging** - Complete access tracking
8. ✅ **Deterministic IDs** - SHA-256 based unique IDs

---

## 📈 System Scalability

- **MongoDB** - Horizontal scaling with sharding
- **File Storage** - Can move to S3/MinIO
- **AI Model** - Can deploy on separate GPU server
- **Load Balancing** - Multiple FastAPI instances
- **Caching** - Redis for session management

---

This is your complete Healthcare Blockchain system! 🎉
