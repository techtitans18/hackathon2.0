# Healthcare Blockchain Mobile App - Kivy Development Prompt

## Project Overview
Create a cross-platform mobile application using **Kivy/KivyMD** for the Healthcare Blockchain system. The app should provide role-based access for patients, hospitals, and admins to interact with medical records securely.

---

## Technology Stack

### Core Framework
- **Kivy 2.2.1+**: Cross-platform Python framework
- **KivyMD 1.1.1+**: Material Design components for Kivy
- **Python 3.9+**: Programming language
- **Buildozer**: Android APK packaging
- **Kivy-iOS**: iOS app packaging

### Additional Libraries
- **requests**: HTTP API calls to FastAPI backend
- **cryptography**: Client-side encryption/decryption
- **qrcode**: QR code generation for e-health cards
- **Pillow**: Image processing
- **plyer**: Native device features (camera, notifications, file picker)
- **keyring**: Secure token storage
- **kivymd.uix**: Material Design UI components

---

## App Architecture

### Directory Structure
```
healthcare_mobile/
├── main.py                          # App entry point
├── buildozer.spec                   # Android build configuration
├── requirements.txt                 # Python dependencies
├── assets/                          # Static resources
│   ├── images/
│   │   ├── logo.png
│   │   ├── hospital_icon.png
│   │   ├── patient_icon.png
│   │   └── admin_icon.png
│   ├── fonts/
│   │   └── Roboto-Regular.ttf
│   └── icons/
│       └── app_icon.png
├── screens/                         # UI screens
│   ├── __init__.py
│   ├── login_screen.py              # Google OAuth login
│   ├── patient/
│   │   ├── __init__.py
│   │   ├── dashboard.py             # Patient dashboard
│   │   ├── records_list.py          # View medical records
│   │   ├── record_detail.py         # Record details with download
│   │   └── ehealth_card.py          # Digital health card with QR
│   ├── hospital/
│   │   ├── __init__.py
│   │   ├── dashboard.py             # Hospital dashboard
│   │   ├── register_patient.py      # Register new patient
│   │   ├── add_record.py            # Upload medical record
│   │   ├── patient_access.py        # OTP verification for walk-ins
│   │   ├── emergency_access.py      # Emergency patient lookup
│   │   └── scan_qr.py               # Scan patient QR code
│   └── admin/
│       ├── __init__.py
│       ├── dashboard.py             # Admin dashboard
│       ├── user_management.py       # Manage users
│       ├── hospital_management.py   # Register/update hospitals
│       └── blockchain_viewer.py     # View blockchain
├── services/                        # Business logic
│   ├── __init__.py
│   ├── api_client.py                # HTTP API wrapper
│   ├── auth_service.py              # Authentication & token management
│   ├── encryption_service.py        # File encryption/decryption
│   ├── storage_service.py           # Local file storage
│   └── qr_service.py                # QR code generation/scanning
├── models/                          # Data models
│   ├── __init__.py
│   ├── user.py                      # User model
│   ├── patient.py                   # Patient model
│   ├── record.py                    # Medical record model
│   └── hospital.py                  # Hospital model
├── utils/                           # Utilities
│   ├── __init__.py
│   ├── validators.py                # Input validation
│   ├── formatters.py                # Data formatting
│   └── constants.py                 # App constants
└── kv/                              # Kivy design files
    ├── login.kv
    ├── patient_dashboard.kv
    ├── hospital_dashboard.kv
    ├── admin_dashboard.kv
    └── components.kv                # Reusable UI components
```

---

## Feature Requirements

### 1. Authentication & Authorization

#### Login Screen
```python
# Features:
- Google Sign-In button (OAuth 2.0)
- Automatic role detection (patient/hospital/admin)
- Secure token storage using keyring
- Remember me functionality
- Biometric authentication (fingerprint/face ID)
- Offline mode indicator

# UI Components:
- App logo and branding
- "Sign in with Google" button
- Loading spinner during authentication
- Error messages for failed login
- Terms & privacy policy links
```

#### Session Management
```python
# Features:
- JWT token storage in secure keyring
- Automatic token refresh
- Session timeout (30 minutes inactivity)
- Logout functionality
- Multi-device session management
```

---

### 2. Patient Features

#### Patient Dashboard
```python
# Features:
- Welcome message with patient name
- Quick stats (total records, last visit)
- E-Health Card preview with QR code
- Recent medical records list (last 5)
- Quick actions: View All Records, Download Card
- Notifications badge

# UI Layout:
- Top app bar with profile icon
- Card-based design (Material Design)
- Bottom navigation: Dashboard, Records, Card, Profile
- Pull-to-refresh functionality
```

#### Medical Records List
```python
# Features:
- List all medical records (sorted by date)
- Filter by: Date range, Hospital, Record type
- Search by keywords
- Record cards showing:
  - Record type icon
  - Hospital name
  - Date and time
  - Description preview
  - Download button
- Pagination (load more)
- Empty state message

# Actions:
- Tap record to view details
- Download original file
- Download AI summary
- Share record (encrypted)
```

#### Record Detail View
```python
# Features:
- Full record information:
  - Record type
  - Hospital name and ID
  - Date and timestamp
  - Full description
  - File name and size
  - Record hash (for verification)
  - Blockchain verification status
- AI-generated summary
- Download buttons:
  - Original file
  - AI summary
- Share functionality
- Print option

# File Handling:
- Download to device storage
- Open with external apps (PDF viewer, image viewer)
- Progress indicator during download
- Offline access to downloaded files
```

#### E-Health Card
```python
# Features:
- Digital health card (Aadhaar size: 323x204px)
- Patient information:
  - Photo
  - Name
  - Health ID
  - Blood group (color-coded)
  - Phone number
  - Date of birth
  - Email
- QR code containing:
  - Health ID
  - Name
  - Blood group
  - Phone
- Actions:
  - Download as PNG
  - Share card
  - Print card
  - Show QR code fullscreen (for scanning)

# UI Design:
- Card preview (swipeable)
- Zoom functionality
- Brightness boost for QR scanning
```

---

### 3. Hospital Features

#### Hospital Dashboard
```python
# Features:
- Welcome message with hospital name
- Quick stats:
  - Patients registered today
  - Records added today
  - Total patients
- Quick actions:
  - Register Patient
  - Add Record
  - Patient Access (OTP)
  - Emergency Access
  - Scan QR Code
- Recent activity feed

# UI Layout:
- Top app bar with hospital logo
- Grid of action cards
- Bottom navigation: Dashboard, Patients, Records, More
```

#### Register Patient
```python
# Features:
- Form fields:
  - Full name (required)
  - Phone number (required, validated)
  - Age (required, numeric)
  - Email (optional, validated)
  - Date of birth (date picker)
  - Blood group (dropdown)
  - Photo (camera/gallery)
  - Address (optional)
- Real-time validation
- Auto-generate Health ID
- Success message with Health ID
- Option to add first record immediately

# UI Components:
- Material Design text fields
- Date picker dialog
- Dropdown menu for blood group
- Image picker (camera/gallery)
- Submit button with loading state
```

#### Add Medical Record
```python
# Features:
- Search patient by:
  - Health ID
  - Phone number
  - Name
- Patient selection with preview
- Form fields:
  - Record type (dropdown: Lab Report, X-Ray, Prescription, etc.)
  - Description (multiline text)
  - File upload (camera/gallery/file picker)
- File preview before upload
- Upload progress indicator
- AI summary generation (automatic)
- Success message with blockchain confirmation

# File Handling:
- Support formats: PDF, JPG, PNG, DOCX
- Max file size: 10 MB
- Compress images before upload
- Show file size and type
```

#### Patient Access (OTP Verification)
```python
# Features:
- Search patient by:
  - Health ID
  - Phone number
  - Email
- Send OTP button
- OTP input (6-digit)
- Countdown timer (10 minutes)
- Resend OTP option
- Verify and access records
- View patient profile and all records
- Download files
- Cross-hospital access (any hospital can access)

# UI Flow:
1. Search patient
2. Display patient preview
3. Send OTP to patient email
4. Enter OTP code
5. Access granted → Show records
```

#### Emergency Access
```python
# Features:
- Quick search by:
  - Health ID
  - Phone number
  - Name + DOB
- Display critical information:
  - Blood group (large, color-coded)
  - Allergies (highlighted)
  - Chronic diseases
  - Previous surgeries
  - Emergency contact
  - Current medications
- Blockchain verification status
- Access logging (audit trail)
- No OTP required (emergency override)

# UI Design:
- Red theme for urgency
- Large, readable text
- Quick access buttons
- Call emergency contact button
```

#### Scan QR Code
```python
# Features:
- Camera view with QR scanner
- Scan patient e-health card QR
- Auto-detect and parse QR data
- Display patient information
- Quick actions:
  - View records (with OTP)
  - Add new record
  - Emergency access
- Flashlight toggle
- Manual Health ID entry fallback

# QR Data Format:
{
  "health_id": "HID123456",
  "name": "John Doe",
  "blood_group": "O+",
  "phone": "+1234567890"
}
```

---

### 4. Admin Features

#### Admin Dashboard
```python
# Features:
- System statistics:
  - Total users
  - Total hospitals
  - Total patients
  - Total records
  - Blockchain blocks
- Recent activity log
- Quick actions:
  - User Management
  - Hospital Management
  - Blockchain Viewer
  - System Settings

# UI Layout:
- Top app bar with admin badge
- Stats cards with icons
- Activity timeline
- Bottom navigation: Dashboard, Users, Hospitals, Blockchain
```

#### User Management
```python
# Features:
- List all users (paginated)
- Filter by role (admin/hospital/patient)
- Search by email/name
- User cards showing:
  - Name and email
  - Role badge
  - Active status
  - Assigned ID (Health ID or Hospital ID)
- Actions:
  - Add new user
  - Edit user (change role, assign ID)
  - Activate/deactivate user
  - Delete user (with confirmation)

# Add/Edit User Form:
- Email (required)
- Role (dropdown)
- Health ID (for patients)
- Hospital ID (for hospitals)
- Active status (toggle)
```

#### Hospital Management
```python
# Features:
- List all hospitals
- Search by name/ID
- Hospital cards showing:
  - Hospital name
  - Hospital type
  - Hospital ID
  - Registration date
- Actions:
  - Register new hospital
  - Update hospital details
  - View hospital statistics

# Register Hospital Form:
- Hospital name (required)
- Hospital type (dropdown: Government, Private, Clinic, etc.)
- Auto-generate Hospital ID (SHA-256 hash)
```

#### Blockchain Viewer
```python
# Features:
- Display all blockchain blocks
- Block cards showing:
  - Block index
  - Health ID
  - Hospital ID
  - Record type
  - Record hash (truncated)
  - Timestamp
  - Block hash (truncated)
- Expandable details (full hashes)
- Search/filter by:
  - Health ID
  - Hospital ID
- Blockchain integrity status
- Patient statistics
- Genesis block highlighted
- Visual chain connectors

# UI Design:
- Vertical timeline layout
- Color-coded blocks (genesis = yellow)
- Integrity badge (green = valid, red = invalid)
- Smooth scrolling
```

---

## API Integration

### API Client Service
```python
# File: services/api_client.py

import requests
from typing import Dict, Any, Optional
from services.auth_service import AuthService

class APIClient:
    BASE_URL = "http://your-backend-url:8000"  # Configure in settings
    
    def __init__(self):
        self.auth_service = AuthService()
        self.session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with JWT token"""
        token = self.auth_service.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    # Auth endpoints
    def google_login(self, credential: str) -> Dict[str, Any]:
        """POST /auth/google"""
        pass
    
    def get_session(self) -> Dict[str, Any]:
        """GET /auth/session"""
        pass
    
    def logout(self) -> None:
        """POST /auth/logout"""
        pass
    
    # Patient endpoints
    def get_patient_profile(self) -> Dict[str, Any]:
        """GET /patient/me"""
        pass
    
    def get_patient_by_id(self, health_id: str) -> Dict[str, Any]:
        """GET /patient/{health_id}"""
        pass
    
    # Hospital endpoints
    def register_patient(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /register_patient"""
        pass
    
    def add_record(self, data: Dict[str, Any], file: bytes) -> Dict[str, Any]:
        """POST /add_record (multipart/form-data)"""
        pass
    
    def send_otp(self, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /patient_access/send_otp"""
        pass
    
    def verify_otp(self, otp_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /patient_access/verify_otp"""
        pass
    
    # Admin endpoints
    def list_users(self) -> Dict[str, Any]:
        """GET /admin/users"""
        pass
    
    def upsert_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /admin/users"""
        pass
    
    def register_hospital(self, hospital_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /register_hospital"""
        pass
    
    def get_blockchain(self) -> Dict[str, Any]:
        """GET /blockchain"""
        pass
    
    # Record endpoints
    def download_file(self, file_name: str) -> bytes:
        """GET /record/file/{file_name}"""
        pass
    
    def download_summary(self, file_name: str) -> str:
        """GET /record/summary/{file_name}"""
        pass
```

---

## UI/UX Design Guidelines

### Theme & Colors
```python
# Material Design Color Palette
PRIMARY_COLOR = "#2196F3"      # Blue
SECONDARY_COLOR = "#4CAF50"    # Green
ACCENT_COLOR = "#FF9800"       # Orange
ERROR_COLOR = "#F44336"        # Red
SUCCESS_COLOR = "#4CAF50"      # Green
WARNING_COLOR = "#FFC107"      # Amber

# Role-specific colors
PATIENT_COLOR = "#2196F3"      # Blue
HOSPITAL_COLOR = "#4CAF50"     # Green
ADMIN_COLOR = "#9C27B0"        # Purple

# Blood group colors
BLOOD_A = "#EF5350"            # Red
BLOOD_B = "#42A5F5"            # Blue
BLOOD_AB = "#AB47BC"           # Purple
BLOOD_O = "#FF7043"            # Orange
```

### Typography
```python
# Font sizes (sp - scale-independent pixels)
HEADING_1 = 24
HEADING_2 = 20
HEADING_3 = 18
BODY_1 = 16
BODY_2 = 14
CAPTION = 12
BUTTON = 14

# Font weights
LIGHT = "Light"
REGULAR = "Regular"
MEDIUM = "Medium"
BOLD = "Bold"
```

### Spacing & Layout
```python
# Padding/Margin (dp - density-independent pixels)
SPACING_SMALL = 8
SPACING_MEDIUM = 16
SPACING_LARGE = 24
SPACING_XLARGE = 32

# Component sizes
BUTTON_HEIGHT = 48
INPUT_HEIGHT = 56
CARD_ELEVATION = 2
CARD_RADIUS = 8
```

### Material Design Components
```python
# Use KivyMD components:
- MDCard: Cards for content grouping
- MDTextField: Text input fields
- MDRaisedButton: Primary action buttons
- MDFlatButton: Secondary action buttons
- MDIconButton: Icon-only buttons
- MDList: Scrollable lists
- MDDialog: Modal dialogs
- MDBottomNavigation: Bottom navigation bar
- MDTopAppBar: Top app bar
- MDChip: Tags and filters
- MDProgressBar: Loading indicators
- MDSnackbar: Toast messages
- MDDatePicker: Date selection
- MDDropdownMenu: Dropdown menus
```

---

## Security Requirements

### 1. Secure Token Storage
```python
# Use keyring library for secure storage
import keyring

# Store JWT token
keyring.set_password("healthcare_app", "jwt_token", token)

# Retrieve JWT token
token = keyring.get_password("healthcare_app", "jwt_token")

# Delete token on logout
keyring.delete_password("healthcare_app", "jwt_token")
```

### 2. Biometric Authentication
```python
# Use plyer for biometric auth
from plyer import biometric

# Check if biometric is available
if biometric.is_available():
    # Authenticate user
    biometric.authenticate(
        title="Healthcare App",
        subtitle="Verify your identity",
        callback=on_auth_success
    )
```

### 3. Encrypted File Storage
```python
# Encrypt files before saving locally
from services.encryption_service import EncryptionService

encryption = EncryptionService()

# Encrypt file
encrypted_data = encryption.encrypt_file(file_bytes)

# Save encrypted file
with open(local_path, 'wb') as f:
    f.write(encrypted_data)

# Decrypt when needed
decrypted_data = encryption.decrypt_file(encrypted_data)
```

### 4. Certificate Pinning
```python
# Pin SSL certificate for API calls
import ssl
import certifi

# Use certifi for trusted certificates
session = requests.Session()
session.verify = certifi.where()
```

### 5. Input Validation
```python
# Validate all user inputs
from utils.validators import Validators

# Email validation
if not Validators.is_valid_email(email):
    show_error("Invalid email address")

# Phone validation
if not Validators.is_valid_phone(phone):
    show_error("Invalid phone number")

# Health ID validation
if not Validators.is_valid_health_id(health_id):
    show_error("Invalid Health ID format")
```

---

## Offline Mode

### Features
```python
# 1. Cache API responses
- Store recent records locally (SQLite)
- Cache patient profile
- Cache downloaded files

# 2. Offline indicators
- Show "Offline" badge in app bar
- Disable features requiring network
- Queue actions for sync when online

# 3. Sync on reconnect
- Auto-sync queued actions
- Update cached data
- Show sync progress

# 4. Local database (SQLite)
- Store user profile
- Store medical records metadata
- Store downloaded files paths
```

---

## Push Notifications

### Use Cases
```python
# 1. New record added
"New medical record added by [Hospital Name]"

# 2. OTP received
"Your OTP for patient access: 123456"

# 3. Emergency access alert
"Emergency access to your records by [Hospital Name]"

# 4. Session expiry warning
"Your session will expire in 5 minutes"

# 5. System announcements
"System maintenance scheduled for [Date]"
```

### Implementation
```python
# Use Firebase Cloud Messaging (FCM)
from plyer import notification

# Show local notification
notification.notify(
    title="Healthcare App",
    message="New medical record added",
    app_icon="assets/icons/app_icon.png",
    timeout=10
)
```

---

## Testing Requirements

### Unit Tests
```python
# Test API client methods
# Test encryption/decryption
# Test validators
# Test data models
```

### Integration Tests
```python
# Test login flow
# Test record upload
# Test file download
# Test OTP verification
```

### UI Tests
```python
# Test screen navigation
# Test form validation
# Test button actions
# Test list scrolling
```

---

## Build & Deployment

### Android Build (Buildozer)
```bash
# Install buildozer
pip install buildozer

# Initialize buildozer.spec
buildozer init

# Edit buildozer.spec:
# - Set package name: com.healthcare.blockchain
# - Set app name: Healthcare Blockchain
# - Set version: 1.0.0
# - Add permissions: INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE
# - Set requirements: kivy, kivymd, requests, cryptography, qrcode, pillow, plyer

# Build APK
buildozer -v android debug

# Build release APK (signed)
buildozer -v android release
```

### iOS Build (Kivy-iOS)
```bash
# Install kivy-ios
pip install kivy-ios

# Build toolchain
toolchain build python3 kivy

# Create Xcode project
toolchain create HealthcareApp /path/to/app

# Open in Xcode and build
open HealthcareApp.xcodeproj
```

---

## Configuration

### App Settings
```python
# File: utils/constants.py

# API Configuration
API_BASE_URL = "https://your-backend.com"  # Production URL
API_TIMEOUT = 30  # seconds

# App Configuration
APP_NAME = "Healthcare Blockchain"
APP_VERSION = "1.0.0"
APP_PACKAGE = "com.healthcare.blockchain"

# Session Configuration
SESSION_TIMEOUT = 1800  # 30 minutes (seconds)
TOKEN_REFRESH_INTERVAL = 300  # 5 minutes (seconds)

# File Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_FILE_TYPES = [".pdf", ".jpg", ".jpeg", ".png", ".docx"]

# Cache Configuration
CACHE_EXPIRY = 3600  # 1 hour (seconds)
MAX_CACHE_SIZE = 100 * 1024 * 1024  # 100 MB
```

---

## Development Roadmap

### Phase 1: Core Features (Week 1-2)
- [ ] Project setup and structure
- [ ] Login screen with Google OAuth
- [ ] Patient dashboard
- [ ] Medical records list
- [ ] Record detail view
- [ ] API client integration

### Phase 2: Hospital Features (Week 3-4)
- [ ] Hospital dashboard
- [ ] Register patient
- [ ] Add medical record
- [ ] Patient access with OTP
- [ ] QR code scanner

### Phase 3: Admin Features (Week 5)
- [ ] Admin dashboard
- [ ] User management
- [ ] Hospital management
- [ ] Blockchain viewer

### Phase 4: Advanced Features (Week 6-7)
- [ ] E-Health card with QR
- [ ] Emergency access
- [ ] File encryption/decryption
- [ ] Offline mode
- [ ] Push notifications

### Phase 5: Testing & Polish (Week 8)
- [ ] Unit tests
- [ ] Integration tests
- [ ] UI/UX improvements
- [ ] Performance optimization
- [ ] Bug fixes

### Phase 6: Deployment (Week 9-10)
- [ ] Android APK build
- [ ] iOS app build
- [ ] Play Store submission
- [ ] App Store submission
- [ ] Documentation

---

## Sample Code Snippets

### Main App Entry Point
```python
# File: main.py

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens.login_screen import LoginScreen
from screens.patient.dashboard import PatientDashboard
from screens.hospital.dashboard import HospitalDashboard
from screens.admin.dashboard import AdminDashboard

class HealthcareApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(PatientDashboard(name='patient_dashboard'))
        sm.add_widget(HospitalDashboard(name='hospital_dashboard'))
        sm.add_widget(AdminDashboard(name='admin_dashboard'))
        
        return sm

if __name__ == '__main__':
    HealthcareApp().run()
```

### Login Screen
```python
# File: screens/login_screen.py

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from services.auth_service import AuthService

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()
        
    def on_google_login(self):
        # Implement Google OAuth flow
        credential = self.get_google_credential()
        result = self.auth_service.login(credential)
        
        if result['success']:
            role = result['user']['role']
            if role == 'patient':
                self.manager.current = 'patient_dashboard'
            elif role == 'hospital':
                self.manager.current = 'hospital_dashboard'
            elif role == 'admin':
                self.manager.current = 'admin_dashboard'
        else:
            self.show_error(result['error'])
```

### Patient Dashboard
```python
# File: screens/patient/dashboard.py

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from services.api_client import APIClient

class PatientDashboard(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        
    def on_enter(self):
        # Load patient data when screen is displayed
        self.load_patient_data()
        
    def load_patient_data(self):
        try:
            profile = self.api_client.get_patient_profile()
            self.display_profile(profile)
            
            records = profile.get('records', [])
            self.display_recent_records(records[:5])
        except Exception as e:
            self.show_error(str(e))
```

---

## Additional Resources

### Documentation Links
- Kivy Documentation: https://kivy.org/doc/stable/
- KivyMD Documentation: https://kivymd.readthedocs.io/
- Buildozer Documentation: https://buildozer.readthedocs.io/
- Plyer Documentation: https://plyer.readthedocs.io/

### Design Resources
- Material Design Guidelines: https://material.io/design
- Material Icons: https://materialdesignicons.com/
- Color Tool: https://material.io/resources/color/

### Testing Tools
- pytest: Unit testing
- pytest-kivy: Kivy-specific testing
- Appium: Mobile UI testing

---

## Success Criteria

### Functional Requirements
- ✅ Users can login with Google OAuth
- ✅ Patients can view their medical records
- ✅ Patients can download files and summaries
- ✅ Patients can view e-health card with QR
- ✅ Hospitals can register patients
- ✅ Hospitals can add medical records
- ✅ Hospitals can verify patients with OTP
- ✅ Hospitals can scan QR codes
- ✅ Admins can manage users and hospitals
- ✅ Admins can view blockchain
- ✅ App works offline (cached data)
- ✅ Files are encrypted locally

### Non-Functional Requirements
- ✅ App loads in < 3 seconds
- ✅ API calls complete in < 5 seconds
- ✅ Smooth 60 FPS animations
- ✅ Works on Android 8.0+ and iOS 12+
- ✅ APK size < 50 MB
- ✅ Battery efficient (< 5% per hour)
- ✅ Secure (encrypted storage, HTTPS)
- ✅ Accessible (screen reader support)

---

## Contact & Support

For questions or issues during development:
- Backend API: http://127.0.0.1:8000/docs
- GitHub Issues: [Your repo URL]
- Email: support@healthcare-blockchain.com

---

**This prompt provides a complete blueprint for building the Healthcare Blockchain mobile app using Kivy. Follow the structure, implement features incrementally, and test thoroughly before deployment.**
