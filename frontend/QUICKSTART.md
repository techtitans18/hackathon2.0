# Quick Start Guide - Healthcare Blockchain Frontend

## Overview
This is a complete React + Vite frontend for the Healthcare Blockchain system. It provides a modern, responsive interface for managing medical records with blockchain integrity verification.

## What Was Built

### ✅ Complete React Frontend
- **Login System** - Google OAuth authentication
- **3 Role-Based Dashboards** - Admin, Hospital, Patient
- **Medical Records Management** - Upload, view, download
- **Blockchain Viewer** - Immutable ledger visualization
- **AI Summaries** - Automatic medical report summarization
- **Emergency Access** - Quick patient profile lookup
- **Responsive Design** - Works on all devices

### ✅ API Integration
- Full REST API integration with backend using Axios
- Automatic token management
- Error handling and user feedback
- File upload/download support

### ✅ User Interface
- Professional dashboard layouts
- Formative forms for patient/hospital registration
- Data tables with sorting and filtering
- Modal dialogs and error messages
- Mobile-responsive CSS

## Installation (If Needed)

```bash
# Go to frontend directory
cd frontend

# Install dependencies
npm install

# Ensure axios is installed
npm install axios

# If upgrading from old version
npm update
```

## Running the Application

### Terminal 1 - Start Backend
```bash
# From project root
python -m uvicorn main:app --reload
```
Backend should run on: `http://127.0.0.1:8000`

### Terminal 2 - Start Frontend
```bash
cd frontend
npm run dev
```
Frontend will run on: `http://localhost:5173`

## First Login

1. Open `http://localhost:5173` in browser
2. Click "Sign in with Google"
3. Authenticate with your Google account
4. System automatically detects your role
5. Redirect to your dashboard

### Test Credentials
- **Google Account**: Any Gmail account with Admin bootstrap configured
- **Default Roles**: Admin, Hospital, or Patient (set via backend)

## Project Files Structure

```
frontend/
├── src/
│   ├── App.jsx                    ← Main routing & session
│   ├── main.jsx                   ← Google OAuth setup
│   ├── index.css                  ← Base styles
│   │
│   ├── pages/
│   │   ├── Login.jsx              ← Google login
│   │   ├── AdminDashboard.jsx     ← Admin panel
│   │   ├── HospitalDashboard.jsx  ← Hospital panel
│   │   ├── PatientDashboard.jsx   ← Patient panel
│   │   ├── DoctorDashboard.jsx    ← Doctor view
│   │   └── PatientWorkspace.jsx   ← Patient workspace
│   │
│   ├── components/
│   │   ├── Navbar.jsx             ← Top navigation
│   │   ├── UserManagement.jsx     ← Admin users
│   │   ├── HospitalRegistration.jsx
│   │   ├── PatientRegistration.jsx
│   │   ├── UploadRecord.jsx       ← File upload
│   │   ├── BlockchainViewer.jsx   ← Blockchain view
│   │   ├── EHealthCard.jsx        ← E-health card
│   │   └── RecordTable.jsx        ← Records table
│   │
│   ├── services/
│   │   └── api.js                 ← API client (Axios)
│   │
│   ├── utils/
│   │   └── helpers.js             ← Utility functions
│   │
│   └── styles/
│       └── styles.css             ← Application styles
│
├── package.json                   ← Dependencies
├── vite.config.js                 ← Vite config
├── index.html                     ← HTML entry point
├── FRONTEND_README.md             ← Full documentation
├── QUICKSTART.md                  ← This file
└── .env.example                   ← Sample env vars
```

## Key Files Explained

### `src/services/api.js`
- Centralized API client with Axios
- Automatic Authorization header
- Response interceptors for error handling
- All endpoints categorized (auth, admin, patient, hospital, etc.)

### `src/App.jsx`
- Main application component
- Session checking on load
- Route-based access control
- Navbar with logout

### `pages/AdminDashboard.jsx`
- User management form
- User list table
- Blockchain viewer tab

### `pages/HospitalDashboard.jsx`
- Hospital registration
- Patient registration form
- Medical record upload
- Blockchain access

### `pages/PatientDashboard.jsx`
- Personal profile
- E-health card
- Medical records download

### `components/UploadRecord.jsx`
- File upload with progress
- Record metadata
- AI summarization

## Features by Role

### Admin
- ✅ View all users
- ✅ Create/update users
- ✅ Assign roles and IDs
- ✅ View full blockchain
- ✅ User management

### Hospital
- ✅ Register hospital
- ✅ Register patients
- ✅ Upload medical records
- ✅ Generate AI summaries
- ✅ View blockchain
- ✅ Emergency patient lookup

### Patient
- ✅ View own profile
- ✅ View e-health card
- ✅ View personal records
- ✅ Download files
- ✅ View AI summaries

## Troubleshooting

### "Cannot reach backend"
```bash
# Check if backend is running
curl http://127.0.0.1:8000/

# Should return: {"message": "Healthcare Blockchain API is running"}
```

### "CORS error"
- Backend must have CORS enabled for `http://localhost:5173`
- Verify in `main.py`: `allow_origins=["http://localhost:5173"]`

### "Login fails"
- Check Google Client ID in `main.jsx`
- Ensure Google OAuth is configured
- Check browser console for error details

### "Files won't download"
- Verify backend creates records correctly
- Check `/records` folder exists on backend
- Try downloading from backend directly

### Clearing Cache
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear browser cache
# DevTools → Application → Clear site data
```

## Development Workflow

### Adding a New API Endpoint

1. Add to `services/api.js`:
```javascript
export const myAPI = {
  getMyData: () => api.get('/my/endpoint'),
};
```

2. Use in component:
```javascript
import { myAPI } from '../services/api';

const MyComponent = () => {
  const loadData = async () => {
    const response = await myAPI.getMyData();
    setData(response.data);
  };
};
```

### Adding a New Component

1. Create in `components/MyComponent.jsx`
2. Import styling from `styles/styles.css`
3. Export as default
4. Use in pages

### Adding New Styles

Add classes to `styles/styles.css` and use in components:
```jsx
<div className="my-custom-class">Content</div>
```

## Build for Production

```bash
# Create optimized build
npm run build

# Preview production build locally
npm run preview

# Deploy `dist/` folder to hosting service
```

## Security Checklist

- ✅ HTTPS in production
- ✅ Environment variables for sensitive data
- ✅ Token stored in localStorage (consider httpOnly for production)
- ✅ CORS properly configured
- ✅ Authorization headers on all requests
- ✅ Input validation on forms
- ✅ Error messages don't expose sensitive info

## Performance Tips

1. **Lazy Load Records** - Don't load all records at once
2. **Paginate Tables** - Limit table rows
3. **Cache API Responses** - Reduce API calls
4. **Optimize Images** - Compress profile photos
5. **Code Splitting** - Use React.lazy() for routes

## Useful Commands

```bash
# Development
npm run dev           # Start dev server
npm run build         # Build for production
npm run preview       # Preview production build
npm run lint          # Run ESLint

# Package
npm install           # Install deps
npm update            # Update deps
npm list              # List installed packages

# Clean
rm -rf node_modules dist .cache
npm install
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## API Response Examples

### Successful Login
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "email": "user@example.com",
    "role": "patient",
    "health_id": "uuid-123",
    "name": "John Doe"
  }
}
```

### List Users Response
```json
{
  "users": [
    {
      "email": "admin@example.com",
      "role": "admin",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### Upload Record Response
```json
{
  "message": "Medical record added successfully.",
  "record_id": "uuid-456",
  "record_hash": "abcd1234...",
  "block": {...},
  "summary_file_name": "report_ai_summary.txt"
}
```

## Next Steps

1. **Test All Features** - Go through each dashboard
2. **Upload Test Records** - Test file upload
3. **View Blockchain** - Verify blocks created
4. **Generate Summaries** - Test AI summarization
5. **Download Files** - Test file downloads

## Support

### Check Logs
- **Backend**: Terminal running uvicorn
- **Frontend**: Browser console (F12)
- **Network**: DevTools Network tab

### Debug Tips
```javascript
// In browser console
localStorage.getItem('access_token')
localStorage.getItem('user')
// Should show your auth data
```

## Summary

✅ **Backend**: Fully functional FastAPI
✅ **Frontend**: Complete React + Vite
✅ **Auth**: Google OAuth integrated
✅ **API**: All endpoints connected
✅ **Styling**: Professional CSS
✅ **UI**: Responsive layouts
✅ **Ready**: Run with `npm run dev`

**Your healthcare blockchain system is ready to use!** 🎉
