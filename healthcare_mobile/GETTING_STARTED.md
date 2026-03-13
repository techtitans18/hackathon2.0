# Getting Started Guide

Welcome to the Healthcare Mobile App! This guide will help you get up and running quickly.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.9 or higher** installed
- **pip** package manager
- **Git** (optional, for version control)
- **Android SDK & NDK** (for Android builds)
- **Xcode** (for iOS builds, macOS only)

## 🚀 Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
cd healthcare_mobile
setup.bat
```

**Linux/Mac:**
```bash
cd healthcare_mobile
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

**Step 1: Create Virtual Environment**
```bash
python -m venv venv
```

**Step 2: Activate Virtual Environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Create Required Directories**
```bash
mkdir cache temp
```

## ⚙️ Configuration

### 1. Configure API Backend

Edit `config.py`:
```python
# Development
API_BASE_URL = 'http://localhost:8000/api'

# Production
API_BASE_URL = 'https://api.yourdomain.com/api'
```

### 2. Environment Variables (Optional)

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your settings.

## 🏃 Running the App

### Desktop (Development)

```bash
python main.py
```

The app will open in a window. You can test all features on desktop before building for mobile.

### Test Credentials

Use these test credentials (configure in your backend):

**Patient:**
- Email: patient@test.com
- Password: Patient123

**Hospital:**
- Email: hospital@test.com
- Password: Hospital123

**Admin:**
- Email: admin@test.com
- Password: Admin123

## 📱 Building for Mobile

### Android

**First Time Setup:**
```bash
# Install Buildozer
pip install buildozer

# Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Initialize buildozer
buildozer init
```

**Build Debug APK:**
```bash
buildozer -v android debug
```

**Build and Install on Device:**
```bash
buildozer android debug deploy run
```

**Build Release APK:**
```bash
buildozer android release
```

The APK will be in `bin/` directory.

### iOS (macOS Only)

**Install Kivy-iOS:**
```bash
pip install kivy-ios
```

**Build Dependencies:**
```bash
toolchain build python3 kivy kivymd
```

**Create Xcode Project:**
```bash
toolchain create HealthcareApp .
```

**Open in Xcode:**
```bash
open HealthcareApp.xcodeproj
```

Build and run from Xcode.

## 🧪 Testing the App

### 1. Test Login Flow

1. Run the app
2. Enter test credentials
3. Verify role-based navigation

### 2. Test Patient Features

1. Login as patient
2. View medical records
3. Generate health card QR code
4. Test offline mode (disconnect internet)

### 3. Test Hospital Features

1. Login as hospital
2. Register a new patient
3. Add a medical record
4. Test camera functionality

### 4. Test Admin Features

1. Login as admin
2. View system statistics
3. Browse users and hospitals

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**2. Buildozer Fails**
```bash
# Solution: Clean and rebuild
buildozer android clean
buildozer -v android debug
```

**3. API Connection Failed**
- Check API_BASE_URL in config.py
- Ensure backend is running
- Check firewall settings
- Verify network connectivity

**4. Camera Not Working**
- Check permissions in buildozer.spec
- Ensure device has camera
- Grant camera permission in app settings

**5. QR Code Not Generating**
```bash
# Solution: Install Pillow dependencies
pip install pillow --upgrade
```

### Getting Help

1. Check `FEATURES.md` for implementation status
2. Review `DEVELOPMENT.md` for coding guidelines
3. See `API_DOCS.md` for API reference
4. Check `DEPLOYMENT.md` for deployment issues

## 📚 Next Steps

### For Developers

1. **Read Documentation**
   - `DEVELOPMENT.md` - Development guidelines
   - `API_DOCS.md` - API reference
   - `FEATURES.md` - Feature checklist

2. **Explore Code**
   - Start with `main.py`
   - Review screen implementations
   - Check service layer

3. **Customize**
   - Update theme colors
   - Add new features
   - Modify UI layouts

### For Deployment

1. **Prepare Backend**
   - Deploy API server
   - Configure database
   - Set up SSL/TLS

2. **Configure App**
   - Update API_BASE_URL
   - Disable debug mode
   - Configure security

3. **Build & Test**
   - Build release version
   - Test on real devices
   - Perform security audit

4. **Deploy**
   - Follow `DEPLOYMENT.md`
   - Submit to app stores
   - Monitor analytics

## 🎯 Development Workflow

### Daily Development

1. **Activate Environment**
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Make Changes**
- Edit Python files for logic
- Edit KV files for UI
- Test changes immediately

3. **Run & Test**
```bash
python main.py
```

4. **Commit Changes**
```bash
git add .
git commit -m "Description of changes"
git push
```

### Adding New Features

1. **Create Screen**
   - Add Python file in `screens/`
   - Add KV file in `kv/`
   - Register in `main.py`

2. **Add API Endpoint**
   - Use `api_client.py`
   - Handle errors
   - Cache if needed

3. **Test**
   - Test on desktop
   - Test on mobile
   - Test offline mode

## 📊 Project Statistics

- **Total Files**: 40+
- **Lines of Code**: 2000+
- **Screens**: 10+
- **Features**: 80+
- **Platforms**: Android, iOS, Desktop

## 🎉 You're Ready!

Your development environment is set up and ready to go!

**Quick Commands:**

```bash
# Run app
python main.py

# Build Android
buildozer android debug

# Install dependencies
pip install -r requirements.txt

# Clean build
buildozer android clean
```

**Important Files:**

- `main.py` - Start here
- `config.py` - Configuration
- `README.md` - Overview
- `FEATURES.md` - Feature list

**Need Help?**

- Check documentation files
- Review code comments
- Test with sample data

Happy coding! 🚀
