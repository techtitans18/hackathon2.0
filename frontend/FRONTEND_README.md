# Healthcare Blockchain Frontend

React + Vite frontend for the Healthcare Blockchain system. A modern, responsive web application for managing medical records with blockchain integrity verification.

## Features

- **Google OAuth Authentication** - Secure login with Google accounts
- **Role-Based Access Control** - Separate dashboards for Admin, Hospital, and Patient roles
- **Medical Record Management** - Upload, view, and download medical records
- **Blockchain Viewer** - View immutable blockchain ledger of medical records
- **AI-Powered Summaries** - Automatic medical record summarization
- **Emergency Access** - Quick patient emergency profile access
- **Responsive Design** - Works seamlessly on desktop and mobile devices

## Tech Stack

- **React 19** - UI framework
- **Vite** - Build tool and development server
- **React Router v7** - Client-side routing
- **Axios** - HTTP client for API calls
- **@react-oauth/google** - Google OAuth integration
- **CSS3** - Custom styling

## Prerequisites

- Node.js 16+ and npm
- Backend server running at `http://127.0.0.1:8000`
- Google OAuth Client ID configured in environment

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Verify Backend Connection

Confirm the backend FastAPI server is running:

```bash
# In another terminal
cd ../
python -m uvicorn main:app --reload
```

Backend should be accessible at `http://127.0.0.1:8000`

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Project Structure

```
src/
├── App.jsx                 # Main app component with routing
├── main.jsx               # Entry point with Google OAuth provider
├── index.css              # Base styles
├── pages/
│   ├── Login.jsx          # Google login page
│   ├── AdminDashboard.jsx # Admin interface
│   ├── HospitalDashboard.jsx # Hospital interface
│   ├── PatientDashboard.jsx  # Patient interface
│   ├── DoctorDashboard.jsx   # Doctor view (read-only)
│   └── PatientWorkspace.jsx  # Patient record workspace
├── components/
│   ├── Navbar.jsx         # Top navigation bar
│   ├── UserManagement.jsx # Admin user management
│   ├── HospitalRegistration.jsx
│   ├── PatientRegistration.jsx
│   ├── UploadRecord.jsx   # Medical record upload
│   ├── BlockchainViewer.jsx # Blockchain visualization
│   ├── EHealthCard.jsx    # E-health card display
│   └── RecordTable.jsx    # Medical records table
├── services/
│   └── api.js             # API client with Axios
└── styles/
    └── styles.css         # Application styles
```

## API Integration

The frontend connects to these backend endpoints:

### Authentication
- `GET /auth/google/config` - Get Google OAuth config
- `POST /auth/google` - Login with Google credential
- `GET /auth/session` - Check current session
- `POST /auth/logout` - Logout user

### Admin
- `GET /admin/users` - List all users
- `POST /admin/users` - Create/update user

### Patient
- `POST /register_patient` - Register patient
- `GET /patient/me` - Get own profile
- `GET /patient/me/e-healthcard` - Get e-health card
- `GET /patient/{HealthID}` - Get patient details

### Hospital
- `POST /register_hospital` - Register hospital
- `POST /add_record` - Upload medical record

### Records
- `GET /blockchain` - View blockchain
- `GET /record/hash/{hash}` - Get record by hash
- `GET /record/file/{name}` - Download file
- `GET /record/summary/{name}` - Download summary

### AI & Emergency
- `GET /ai/health` - Check AI service status
- `POST /ai/summary` - Generate AI summary
- `POST /emergency/search` - Search patient
- `POST /emergency/profile` - Get emergency profile
- `POST /emergency/upsert` - Update emergency data

## Authentication Flow

1. **Login Page** - User clicks "Sign in with Google"
2. **Google OAuth** - User authenticates with Google account
3. **Token Exchange** - Frontend sends credential to backend
4. **Session Creation** - Backend returns access token and user role
5. **Token Storage** - Token stored in localStorage
6. **Dashboard Routing** - User redirected to role-based dashboard
7. **API Requests** - All subsequent API calls include Authorization header with token

## Component Details

### Login.jsx
- Google Sign-In button
- Error handling
- Role information display

### AdminDashboard.jsx
- User management form
- User list table
- Blockchain viewer

### HospitalDashboard.jsx
- Hospital registration
- Patient registration form
- Medical record upload
- Blockchain access

### PatientDashboard.jsx
- Personal profile display
- E-health card
- Medical records list with download options

### UploadRecord.jsx
- File upload with progress
- Record metadata input
- AI summarization trigger

### BlockchainViewer.jsx
- Block chain visualization
- Block details display
- Hash verification

## Styling

The application uses a custom CSS stylesheet with:
- **Grid Layout System** - Responsive container configuration
- **Color Scheme** - Professional blue/teal palette
- **Typography** - Clear hierarchy with Segoe UI
- **Responsive Design** - Mobile-first approach
- **Accessibility** - WCAG-compliant color contrast

### Key CSS Classes
- `.dashboard-container` - Main page wrapper
- `.navbar` - Top navigation
- `.tab-navigation` - Tabbed interface
- `.form-group` - Form field styling
- `.records-table` - Medical records table
- `.blockchain-block` - Blockchain block display
- `.error-message` / `.success-message` - Alerts

## Building for Production

```bash
npm run build
```

Output will be in the `dist/` folder, ready to deploy to a static hosting service.

## Environment Variables

The following are configured in `main.jsx`:
- `GOOGLE_CLIENT_ID` - Google OAuth 2.0 Client ID (hardcoded for demo, should be in .env)
- Backend API URL is set to `http://127.0.0.1:8000` in `services/api.js`

For deployment, create a `.env` file:
```
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
VITE_API_BASE_URL=https://your-backend-url.com
```

## Debugging

### Check Backend Connection
```javascript
// In browser console
fetch('http://127.0.0.1:8000/').then(r => r.json())
```

### View Network Requests
- Open DevTools (F12) → Network tab
- Check for 401 errors (not authenticated)
- Verify Authorization header with token

### Common Issues

| Issue | Solution |
|-------|----------|
| CORS errors | Ensure backend has correct CORS origin: `http://localhost:5173` |
| 401 errors | Token expired, user needs to logout and login again |
| Files won't download | Check file path and permissions on backend |
| Google login fails | Verify Google Client ID matches OAuth config |

## Security Notes

- **Token Storage** - Access tokens stored in localStorage (consider httpOnly cookies for production)
- **HTTPS** - Deploy with HTTPS in production
- **CORS** - Frontend restricted to specific backend origin
- **API Authorization** - All API calls include Bearer token

## Performance Tips

- Records and blockchain paginate to avoid loading large datasets
- File downloads use streaming responses
- Lazy loading of blockchain blocks for large chains
- Debounced search inputs

## Contributing

1. Follow React best practices
2. Keep components modular and reusable
3. Update styles in `styles/styles.css`
4. Test API integration with backend
5. Ensure responsive design on mobile

## License

This project is part of the Healthcare Blockchain system.

## Support

For issues or questions:
1. Check backend logs for API errors
2. Review browser console for client-side errors
3. Verify CORS and authentication configuration
4. Test API endpoints directly with curl or Postman
