# Deployment Guide

## Android Deployment

### Prerequisites
1. Install Java JDK 8 or 11
2. Install Android SDK
3. Install Android NDK
4. Install Buildozer

### Build Steps

1. **Configure buildozer.spec**
```bash
# Update version
version = 1.0.0

# Update package name
package.name = healthcareapp
package.domain = com.healthcare
```

2. **Build Debug APK**
```bash
buildozer -v android debug
```

3. **Build Release APK**
```bash
# Generate keystore (first time only)
keytool -genkey -v -keystore healthcare.keystore -alias healthcare -keyalg RSA -keysize 2048 -validity 10000

# Build release
buildozer android release

# Sign APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore healthcare.keystore bin/*.apk healthcare

# Zipalign
zipalign -v 4 bin/healthcareapp-*.apk bin/healthcareapp-release.apk
```

4. **Deploy to Device**
```bash
buildozer android deploy run
```

### Google Play Store

1. Create developer account
2. Create app listing
3. Upload APK/AAB
4. Complete store listing
5. Submit for review

## iOS Deployment

### Prerequisites
1. macOS with Xcode
2. Apple Developer Account
3. Kivy-iOS toolchain

### Build Steps

1. **Install Kivy-iOS**
```bash
pip install kivy-ios
```

2. **Build Dependencies**
```bash
toolchain build python3 kivy kivymd
```

3. **Create Xcode Project**
```bash
toolchain create HealthcareApp /path/to/healthcare_mobile
```

4. **Configure in Xcode**
- Open HealthcareApp.xcodeproj
- Set bundle identifier
- Configure signing
- Set deployment target

5. **Build and Archive**
- Product > Archive
- Distribute to App Store

### App Store

1. Create app in App Store Connect
2. Upload build via Xcode
3. Complete app information
4. Submit for review

## Backend Configuration

Update `config.py` with production API URL:
```python
API_BASE_URL = 'https://api.healthcare.com/api'
DEBUG_MODE = False
```

## Security Checklist

- [ ] Update API URLs to production
- [ ] Disable debug mode
- [ ] Configure certificate pinning
- [ ] Test all authentication flows
- [ ] Verify encryption is working
- [ ] Test offline functionality
- [ ] Review permissions
- [ ] Test on multiple devices
- [ ] Perform security audit

## Testing Before Release

1. **Functional Testing**
   - Login/logout
   - All user roles
   - API integration
   - Offline mode
   - Camera functionality
   - QR code generation/scanning

2. **Performance Testing**
   - App startup time
   - API response handling
   - Memory usage
   - Battery consumption

3. **Security Testing**
   - Token storage
   - Data encryption
   - Input validation
   - Network security

## Monitoring

Set up monitoring for:
- Crash reports
- API errors
- User analytics
- Performance metrics

## Updates

To release updates:
1. Update version in buildozer.spec
2. Build new APK/IPA
3. Test thoroughly
4. Upload to stores
5. Submit for review
