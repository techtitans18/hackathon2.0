# Healthcare Mobile App

A cross-platform mobile application for managing healthcare records built with Kivy/KivyMD.

## Features

### Patient App
- View medical records
- Download files & AI summaries
- Digital e-health card with QR code
- Offline access to cached data

### Hospital App
- Register new patients
- Add medical records (with camera)
- OTP verification for walk-ins
- QR code scanner
- Emergency access

### Admin App
- User management
- Hospital management
- System statistics
- Blockchain viewer

## Technology Stack
- **Kivy 2.2.1+** - Cross-platform framework
- **KivyMD 1.1.1+** - Material Design UI
- **Python 3.9+** - Programming language
- **Buildozer** - Android packaging
- **Kivy-iOS** - iOS packaging

## Installation

### Prerequisites
```bash
# Install Python 3.9+
python --version

# Install dependencies
pip install -r requirements.txt
```

### Development Setup
```bash
# Clone the repository
cd healthcare_mobile

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

## Building for Mobile

### Android Build
```bash
# Install Buildozer
pip install buildozer

# Initialize buildozer (first time only)
buildozer init

# Build APK
buildozer -v android debug

# Build and deploy to connected device
buildozer android debug deploy run
```

### iOS Build
```bash
# Install Kivy-iOS
pip install kivy-ios

# Create toolchain
toolchain build python3 kivy

# Create Xcode project
toolchain create HealthcareApp /path/to/app

# Open in Xcode and build
open HealthcareApp.xcodeproj
```

## Configuration

Edit `config.py` to configure:
- API base URL
- Timeout settings
- Cache settings
- Debug mode

```python
API_BASE_URL = 'http://your-api-url.com/api'
```

## Project Structure
```
healthcare_mobile/
├── main.py                    # Entry point
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── buildozer.spec            # Android build config
├── screens/                   # UI screens
│   ├── login_screen.py
│   ├── patient/              # Patient features
│   │   ├── dashboard.py
│   │   ├── records.py
│   │   └── health_card.py
│   ├── hospital/             # Hospital features
│   │   ├── dashboard.py
│   │   ├── add_record.py
│   │   └── register_patient.py
│   └── admin/                # Admin features
│       ├── dashboard.py
│       ├── user_management.py
│       └── hospital_management.py
├── services/                  # Business logic
│   ├── api_client.py         # API integration
│   ├── auth_service.py       # Authentication
│   └── encryption_service.py # File encryption
├── models/                    # Data models
│   ├── user.py
│   ├── patient.py
│   └── hospital.py
├── utils/                     # Utilities
│   ├── qr_utils.py
│   ├── validators.py
│   └── cache_manager.py
└── kv/                       # UI design files
    ├── login_screen.kv
    ├── patient_dashboard.kv
    ├── hospital_dashboard.kv
    └── admin_dashboard.kv
```

## Security Features
- Secure token storage (keyring)
- Client-side file encryption
- Input validation
- Certificate pinning (configurable)

## API Integration

The app expects the following API endpoints:

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh token

### Patient
- `GET /api/patient/records` - Get medical records
- `GET /api/patient/profile` - Get patient profile

### Hospital
- `POST /api/hospital/patients` - Register patient
- `POST /api/hospital/records` - Add medical record
- `GET /api/hospital/patients` - List patients

### Admin
- `GET /api/admin/users` - List users
- `GET /api/admin/hospitals` - List hospitals
- `GET /api/admin/statistics` - System statistics

## Testing

```bash
# Run tests (when implemented)
python -m pytest tests/
```

## Troubleshooting

### Common Issues

1. **Buildozer fails on Android**
   - Ensure Android SDK and NDK are installed
   - Check buildozer.spec configuration
   - Run: `buildozer android clean`

2. **Camera not working**
   - Check permissions in buildozer.spec
   - Ensure CAMERA permission is granted

3. **API connection fails**
   - Verify API_BASE_URL in config.py
   - Check network connectivity
   - Ensure backend is running

## License
MIT License

## Support
For issues and questions, please contact support@healthcare.com
