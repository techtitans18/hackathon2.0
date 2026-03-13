# Healthcare Blockchain System

A comprehensive healthcare management system with blockchain-based record integrity, role-based access control, and AI-powered medical summaries.

## 🏗️ Project Structure

```
healthcare_blockchain/
├── backend/                    # FastAPI Backend
│   ├── app/                   # Application modules
│   │   ├── ai_summary/       # AI medical summary generation
│   │   └── emergency/        # Emergency access features
│   ├── blockchain/           # Blockchain implementation
│   ├── database/             # MongoDB connection & models
│   ├── models/               # Pydantic data models
│   ├── routes/               # API endpoints
│   ├── utils/                # Utilities (encryption, etc.)
│   ├── records/              # Encrypted medical files storage
│   ├── main.py               # FastAPI app entry point
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment configuration
│
├── frontend/                  # React + Vite Frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components (dashboards)
│   │   ├── services/         # API client services
│   │   ├── styles/           # CSS stylesheets
│   │   └── App.jsx           # Main React app
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
│
├── docs/                      # Documentation
│   ├── README.md             # Main documentation
│   ├── FILE_ENCRYPTION.md    # Encryption architecture
│   ├── MOBILE_APP_PROMPT.md  # Mobile app development guide
│   └── *.md                  # Other documentation files
│
├── scripts/                   # Utility scripts
│   ├── test_*.py             # Test scripts
│   └── debug_*.py            # Debug scripts
│
└── .github/                   # GitHub workflows
    └── workflows/
```

## 🚀 Quick Start

### Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI, Google OAuth credentials, etc.

# Generate encryption key
python generate_encryption_key.py
# Add the generated key to .env as FILE_ENCRYPTION_KEY

# Run backend server
python -m uvicorn main:app --reload
```

Backend will run at: `http://127.0.0.1:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run at: `http://localhost:5173`

## 📚 Documentation

- **[Main Documentation](docs/README.md)** - Complete system overview
- **[File Encryption](docs/FILE_ENCRYPTION.md)** - Encryption architecture and security
- **[Mobile App Guide](docs/MOBILE_APP_PROMPT.md)** - Kivy mobile app development
- **[Cross-Hospital Access](docs/CROSS_HOSPITAL_ACCESS.md)** - Multi-hospital features
- **[Email Verification](docs/EMAIL_VERIFICATION_UPDATE.md)** - OTP verification system

## 🔑 Key Features

### Backend (FastAPI)
- ✅ **Blockchain Integrity** - Immutable medical record audit trail
- ✅ **AES-256 Encryption** - Encrypted file storage and transfer
- ✅ **Role-Based Access** - Admin, Hospital, Patient roles
- ✅ **Google OAuth** - Secure authentication
- ✅ **AI Summaries** - Automatic medical report summarization
- ✅ **OTP Verification** - Patient access with email OTP
- ✅ **Emergency Access** - Quick critical information lookup
- ✅ **Cross-Hospital** - Any hospital can access any patient (with consent)

### Frontend (React)
- ✅ **Patient Dashboard** - View records, download files, e-health card
- ✅ **Hospital Dashboard** - Register patients, add records, OTP access
- ✅ **Admin Dashboard** - User management, hospital management, blockchain viewer
- ✅ **E-Health Card** - Digital health card with QR code
- ✅ **Blockchain Viewer** - Search and filter blockchain blocks
- ✅ **Responsive Design** - Mobile-friendly UI

## 🔐 Security

- **Encryption at Rest**: AES-256-GCM for all medical files
- **Encryption in Transit**: HTTPS (production)
- **Authentication**: JWT tokens with Google OAuth
- **Authorization**: Role-based access control (RBAC)
- **Integrity**: SHA-256 hashing + blockchain verification
- **Audit Trail**: Immutable blockchain logs

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database
- **PyTorch + Transformers** - AI medical summaries
- **Cryptography** - AES-256 encryption
- **Google Auth** - OAuth 2.0 authentication

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Axios** - HTTP client
- **QRCode** - QR code generation
- **html2canvas** - Image export

## 📱 Mobile App (Kivy)

Mobile app is now available in `healthcare_mobile/` folder!

- **Framework**: Kivy/KivyMD
- **Platforms**: Android & iOS
- **Features**: All web features + biometric auth, offline mode, QR scanner
- **Documentation**: See `healthcare_mobile/README.md`

### Quick Start
```bash
cd healthcare_mobile
pip install -r requirements.txt
python main.py
```

### Build APK
```bash
cd healthcare_mobile
buildozer -v android debug
```

## 🧪 Testing

```bash
# Run backend tests
cd backend
python -m pytest

# Run test scripts
cd scripts
python test_patient_access_otp.py
python test_pdf_ai_summary.py
```

## 📦 Deployment

### Backend Deployment
```bash
# Production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Docker (optional)
docker build -t healthcare-backend .
docker run -p 8000:8000 healthcare-backend
```

### Frontend Deployment
```bash
# Build for production
cd frontend
npm run build

# Deploy dist/ folder to hosting service
# (Vercel, Netlify, AWS S3, etc.)
```

## 🔧 Configuration

### Backend Environment Variables (.env)
```env
MONGO_URI=mongodb+srv://...
MONGO_DB_NAME=healthcare_blockchain
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
AUTH_SECRET_KEY=your-secret-key-min-32-chars
ADMIN_BOOTSTRAP_EMAILS=admin@example.com
FILE_ENCRYPTION_KEY=base64-encoded-32-byte-key
```

### Frontend Environment Variables
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

For questions or support:
- Email: support@healthcare-blockchain.com
- GitHub Issues: [Create an issue](https://github.com/your-repo/issues)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- MongoDB for flexible data storage
- Hugging Face for AI models
- Google for OAuth authentication
- React team for the UI library

---

**Built with ❤️ for better healthcare management**
