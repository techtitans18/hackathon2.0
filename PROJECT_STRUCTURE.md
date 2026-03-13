# Healthcare Blockchain - Project Structure

## 📁 Complete Directory Structure

```
healthcare_blockchain/
│
├── 📂 backend/                          # FastAPI Backend Application
│   ├── 📂 app/                         # Application modules
│   │   ├── 📂 ai_summary/              # AI medical summary generation
│   │   │   ├── __init__.py
│   │   │   ├── ai_routes.py            # AI summary API endpoints
│   │   │   ├── security_policy.py      # AI security policies
│   │   │   └── summarizer.py           # BART model summarization
│   │   ├── 📂 emergency/               # Emergency access features
│   │   │   ├── __init__.py
│   │   │   ├── emergency_models.py     # Emergency data models
│   │   │   ├── emergency_routes.py     # Emergency API endpoints
│   │   │   ├── emergency_security.py   # Emergency access security
│   │   │   └── emergency_service.py    # Emergency business logic
│   │   └── __init__.py
│   │
│   ├── 📂 blockchain/                  # Blockchain implementation
│   │   ├── __init__.py
│   │   ├── blockchain.py               # Blockchain class & logic
│   │   └── verify.py                   # Blockchain integrity verification
│   │
│   ├── 📂 database/                    # Database connection & setup
│   │   ├── __init__.py
│   │   └── db.py                       # MongoDB connection & collections
│   │
│   ├── 📂 models/                      # Data models (Pydantic)
│   │   ├── 📂 ai_summary/              # AI model storage
│   │   │   └── facebook-bart-large-cnn/ # BART model files
│   │   ├── __init__.py
│   │   ├── hospital.py                 # Hospital models
│   │   ├── patient.py                  # Patient models
│   │   └── record.py                   # Medical record models
│   │
│   ├── 📂 records/                     # Encrypted medical files storage
│   │   ├── .gitkeep
│   │   └── [encrypted files]           # UUID_filename (encrypted)
│   │
│   ├── 📂 routes/                      # API route handlers
│   │   ├── __init__.py
│   │   ├── admin_routes.py             # Admin endpoints
│   │   ├── auth_routes.py              # Authentication (Google OAuth)
│   │   ├── hospital_routes.py          # Hospital management
│   │   ├── patient_access_routes.py    # OTP patient access
│   │   ├── patient_routes.py           # Patient endpoints
│   │   └── record_routes.py            # Medical record endpoints
│   │
│   ├── 📂 utils/                       # Utility functions
│   │   ├── __init__.py
│   │   └── encryption.py               # AES-256-GCM encryption
│   │
│   ├── .env                            # Environment variables (SECRET)
│   ├── .env.example                    # Environment template
│   ├── generate_encryption_key.py      # Encryption key generator
│   ├── main.py                         # FastAPI app entry point
│   └── requirements.txt                # Python dependencies
│
├── 📂 frontend/                         # React + Vite Frontend
│   ├── 📂 public/                      # Static assets
│   │   └── vite.svg
│   │
│   ├── 📂 src/                         # Source code
│   │   ├── 📂 api/                     # API utilities
│   │   ├── 📂 components/              # Reusable UI components
│   │   │   ├── AddHospital.jsx
│   │   │   ├── BlockchainViewer.jsx
│   │   │   ├── EHealthCard.jsx
│   │   │   ├── LandingNavbar.jsx
│   │   │   ├── UpdateHospital.jsx
│   │   │   └── UserManagement.jsx
│   │   ├── 📂 logic/                   # Business logic
│   │   ├── 📂 pages/                   # Page components
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── HospitalDashboard.jsx
│   │   │   ├── LandingPage.jsx
│   │   │   ├── Login.jsx
│   │   │   └── PatientDashboard.jsx
│   │   ├── 📂 services/                # API client services
│   │   │   └── api.js                  # Axios API client
│   │   ├── 📂 styles/                  # CSS stylesheets
│   │   │   ├── admin.css
│   │   │   ├── blockchain-viewer.css
│   │   │   ├── ehealth-card.css
│   │   │   ├── hospital.css
│   │   │   ├── landing.css
│   │   │   ├── landing-navbar.css
│   │   │   ├── login.css
│   │   │   └── patient.css
│   │   ├── 📂 utils/                   # Utility functions
│   │   ├── App.jsx                     # Main React component
│   │   ├── index.css                   # Global styles
│   │   └── main.jsx                    # React entry point
│   │
│   ├── .env.example                    # Frontend env template
│   ├── .gitignore                      # Git ignore rules
│   ├── eslint.config.js                # ESLint configuration
│   ├── index.html                      # HTML entry point
│   ├── package.json                    # Node dependencies
│   ├── package-lock.json               # Dependency lock file
│   ├── vite.config.js                  # Vite configuration
│   ├── FRONTEND_README.md              # Frontend documentation
│   ├── QUICKSTART.md                   # Quick start guide
│   └── README.md                       # Frontend README
│
├── 📂 healthcare_mobile/                # Kivy Mobile App (Android/iOS)
│   ├── 📂 cache/                       # Local cache storage
│   │
│   ├── 📂 kv/                          # Kivy design files
│   │   ├── add_record.kv               # Add record screen design
│   │   ├── admin_dashboard.kv          # Admin dashboard design
│   │   ├── health_card.kv              # E-health card design
│   │   ├── hospital_dashboard.kv       # Hospital dashboard design
│   │   ├── hospital_management.kv      # Hospital management design
│   │   ├── login_screen.kv             # Login screen design
│   │   ├── patient_dashboard.kv        # Patient dashboard design
│   │   ├── patient_records.kv          # Patient records design
│   │   ├── register_patient.kv         # Register patient design
│   │   └── user_management.kv          # User management design
│   │
│   ├── 📂 models/                      # Data models
│   │   ├── __init__.py
│   │   ├── hospital.py                 # Hospital model
│   │   ├── patient.py                  # Patient model
│   │   └── user.py                     # User model
│   │
│   ├── 📂 screens/                     # Screen components
│   │   ├── 📂 admin/                   # Admin screens
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py            # Admin dashboard
│   │   │   ├── hospital_management.py  # Hospital management
│   │   │   └── user_management.py      # User management
│   │   ├── 📂 hospital/                # Hospital screens
│   │   │   ├── __init__.py
│   │   │   ├── add_record.py           # Add medical record
│   │   │   ├── dashboard.py            # Hospital dashboard
│   │   │   └── register_patient.py     # Register patient
│   │   ├── 📂 patient/                 # Patient screens
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py            # Patient dashboard
│   │   │   ├── health_card.py          # E-health card
│   │   │   └── records.py              # Medical records list
│   │   ├── __init__.py
│   │   └── login_screen.py             # Login screen
│   │
│   ├── 📂 services/                    # Business logic services
│   │   ├── __init__.py
│   │   ├── api_client.py               # API client wrapper
│   │   ├── auth_service.py             # Authentication service
│   │   └── encryption_service.py       # File encryption service
│   │
│   ├── 📂 utils/                       # Utility functions
│   │   ├── __init__.py
│   │   ├── cache_manager.py            # Cache management
│   │   ├── qr_utils.py                 # QR code utilities
│   │   └── validators.py               # Input validators
│   │
│   ├── .env.example                    # Mobile env template
│   ├── .gitignore                      # Git ignore rules
│   ├── API_DOCS.md                     # API documentation
│   ├── ARCHITECTURE.md                 # Architecture overview
│   ├── buildozer.spec                  # Android build config
│   ├── COMPLETION.md                   # Completion status
│   ├── config.py                       # App configuration
│   ├── DEPLOYMENT.md                   # Deployment guide
│   ├── DEVELOPMENT.md                  # Development guide
│   ├── FEATURES.md                     # Features list
│   ├── GETTING_STARTED.md              # Getting started guide
│   ├── INDEX.md                        # Documentation index
│   ├── main.py                         # Kivy app entry point
│   ├── PROJECT_SUMMARY.md              # Project summary
│   ├── README.md                       # Mobile app README
│   ├── requirements.txt                # Python dependencies
│   ├── setup.bat                       # Windows setup script
│   └── setup.sh                        # Linux/Mac setup script
│
├── 📂 docs/                             # Documentation
│   ├── README.md                       # Main documentation
│   ├── COMPLETE_STRUCTURE.md           # Project structure
│   ├── CROSS_HOSPITAL_ACCESS.md        # Cross-hospital features
│   ├── EMAIL_VERIFICATION_UPDATE.md    # OTP verification docs
│   ├── ENCRYPTION_DIAGRAM.md           # Encryption visuals
│   ├── FILE_ENCRYPTION.md              # Encryption architecture
│   └── MOBILE_APP_PROMPT.md            # Mobile app guide
│
├── 📂 scripts/                          # Utility & test scripts
│   ├── check_auth.py                   # Auth testing
│   ├── debug_patient_search.py         # Debug patient search
│   ├── test_all_search_options.py      # Test search features
│   ├── test_direct_file_summary.py     # Test AI summary
│   ├── test_patient_access_otp.py      # Test OTP flow
│   ├── test_pdf_ai_summary.py          # Test PDF summarization
│   ├── test_pdf_extraction.py          # Test PDF text extraction
│   ├── test_summary_input.py           # Test summary input
│   └── sample_kidney_stone_report.txt  # Sample medical report
│
├── 📂 .github/                          # GitHub configuration
│   └── workflows/
│       └── blank.yml                   # GitHub Actions workflow
│
├── .gitignore                          # Git ignore rules (root)
├── PROJECT_STRUCTURE.md                # This file
└── README.md                           # Project README (root)
```

---

## 🎯 Key Directories Explained

### Backend (`/backend`)
Contains the entire FastAPI backend application with:
- **API routes** for all endpoints
- **Blockchain** implementation for record integrity
- **Database** connection to MongoDB
- **Encryption** utilities for secure file storage
- **AI summarization** using BART model
- **Emergency access** features

### Frontend (`/frontend`)
React-based web application with:
- **Role-based dashboards** (Patient, Hospital, Admin)
- **Material Design** UI components
- **API integration** with backend
- **E-Health Card** with QR code generation
- **Blockchain viewer** for admins

### Mobile App (`/healthcare_mobile`)
Kivy-based mobile application for Android/iOS with:
- **Cross-platform** support (Android & iOS)
- **Role-based screens** (Patient, Hospital, Admin)
- **Offline mode** with local caching
- **QR code** scanning and generation
- **Biometric authentication** support
- **File encryption** for local storage
- **Material Design** UI with KivyMD
- **Complete feature parity** with web app

### Documentation (`/docs`)
Comprehensive documentation including:
- System architecture
- Encryption details
- Mobile app development guide
- Feature specifications

### Scripts (`/scripts`)
Testing and debugging utilities:
- Authentication tests
- OTP verification tests
- AI summary tests
- PDF extraction tests

---

## 🚀 Running the Application

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
Runs at: `http://127.0.0.1:8000`

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs at: `http://localhost:5173`

### 3. Mobile App
```bash
cd healthcare_mobile
pip install -r requirements.txt
python main.py
```

**Build Android APK:**
```bash
cd healthcare_mobile
buildozer -v android debug
```

**Build iOS App:**
```bash
cd healthcare_mobile
toolchain create HealthcareApp .
```

---

## 📦 Key Files

### Backend Entry Point
- `backend/main.py` - FastAPI application initialization

### Frontend Entry Point
- `frontend/src/main.jsx` - React application initialization
- `frontend/index.html` - HTML entry point

### Mobile App Entry Point
- `healthcare_mobile/main.py` - Kivy application initialization
- `healthcare_mobile/buildozer.spec` - Android build configuration

### Configuration Files
- `backend/.env` - Backend environment variables (SECRET)
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node.js dependencies
- `frontend/vite.config.js` - Vite build configuration

### Documentation
- `README.md` - Main project documentation
- `docs/README.md` - Detailed system documentation
- `docs/FILE_ENCRYPTION.md` - Encryption architecture

---

## 🔐 Security Files

### Encryption
- `backend/utils/encryption.py` - AES-256-GCM encryption utilities
- `backend/generate_encryption_key.py` - Key generation script

### Authentication
- `backend/routes/auth_routes.py` - Google OAuth implementation
- `backend/.env` - Contains `AUTH_SECRET_KEY` and `GOOGLE_CLIENT_ID`

### Encrypted Storage
- `backend/records/` - All medical files stored encrypted

---

## 🗄️ Data Storage

### MongoDB Collections
- `patients` - Patient profiles
- `hospitals` - Hospital information
- `records` - Medical record metadata
- `users` - User accounts (admin, hospital, patient)
- `blockchain` - Blockchain blocks (persistent)
- `emergency_data` - Emergency access data
- `emergency_logs` - Emergency access audit logs

### Local File Storage
- `backend/records/` - Encrypted medical files
- `backend/models/ai_summary/` - AI model files (BART)

---

## 🔄 Data Flow

### Upload Medical Record
```
Hospital → Frontend → Backend API → Encrypt File → Save to records/ 
→ Store metadata in MongoDB → Add block to blockchain → Return success
```

### Download Medical Record
```
Patient → Frontend → Backend API → Verify permissions → Read encrypted file 
→ Decrypt file → Send to user → Clean up temp file
```

### View Blockchain
```
Admin → Frontend → Backend API → Load blockchain from MongoDB 
→ Return all blocks → Display in UI with search/filter
```

---

## 📊 Technology Stack Summary

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: MongoDB (PyMongo)
- **AI**: PyTorch + Transformers (BART)
- **Encryption**: Cryptography (AES-256-GCM)
- **Auth**: Google OAuth 2.0

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite 5
- **HTTP Client**: Axios
- **UI**: Custom CSS (Material Design inspired)
- **QR Code**: qrcode.react + html2canvas

---

## 🎨 Design Patterns

### Backend
- **Repository Pattern**: Database access through collection getters
- **Service Layer**: Business logic in separate service modules
- **Dependency Injection**: FastAPI's `Depends()` for auth
- **Singleton**: Blockchain instance shared across app

### Frontend
- **Component-Based**: Reusable React components
- **Service Layer**: API calls abstracted in `services/api.js`
- **State Management**: React hooks (useState, useEffect)
- **Routing**: React Router for navigation

---

## 📝 Notes

### Important Files to Configure
1. `backend/.env` - Add MongoDB URI, Google OAuth, encryption key
2. `frontend/.env` - Add API URL and Google Client ID

### Files to Backup
- `backend/.env` - Contains all secrets
- `backend/records/` - Encrypted medical files
- MongoDB database - All metadata and blockchain

### Files to Ignore in Git
- `backend/.env` - Contains secrets
- `backend/records/*` - Patient data
- `frontend/node_modules/` - Dependencies
- `backend/__pycache__/` - Python cache

---

**This structure ensures clean separation of concerns, easy maintenance, and scalability.**
