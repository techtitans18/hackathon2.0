# Landing Page Setup Guide

## What's New

A professional landing page has been added to the Healthcare Blockchain system with:
- Hero section with animated floating cards
- Features showcase (6 key features)
- How it works (4-step process)
- Statistics section
- Call-to-action section
- Professional footer
- Google Sign-In integration
- Responsive design for mobile/tablet/desktop

## Files Created

1. **frontend/src/pages/LandingPage.jsx** - Main landing page component
2. **frontend/src/styles/landing.css** - Complete styling with animations
3. **Updated App.jsx** - Added routing for landing page

## How to Access

### Development Mode (React Dev Server)

1. **Start Backend**:
   ```bash
   cd c:\Users\Shekhar Yalmar\Desktop\lib\healthcare_blockchain
   python -m uvicorn main:app --reload
   ```

2. **Start Frontend** (in new terminal):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser**:
   - Landing Page: http://localhost:5173/
   - Direct Login: http://localhost:5173/login

### Routes

- `/` - Landing page (public, shows when not logged in)
- `/login` - Login page (redirects to dashboard if already logged in)
- `/admin` - Admin dashboard (requires admin role)
- `/hospital` - Hospital dashboard (requires hospital role)
- `/patient` - Patient dashboard (requires patient role)
- `/emergency` - Emergency dashboard (requires hospital/emergency role)

## Features

### Landing Page Sections

1. **Hero Section**
   - Eye-catching gradient background
   - Main title with subtitle
   - Description text
   - Two CTA buttons (Sign In, Learn More)
   - Animated floating cards showing key features

2. **Features Grid**
   - 6 feature cards with icons
   - Blockchain Integrity
   - AI Summarization
   - Cross-Hospital Access
   - Emergency Access
   - Role-Based Security
   - OTP Verification

3. **How It Works**
   - 4-step process visualization
   - Connected with visual lines
   - Clear descriptions for each step

4. **Statistics**
   - 4 key metrics displayed
   - Gradient background matching hero
   - Eye-catching numbers

5. **Call to Action**
   - Final sign-in prompt
   - Large CTA button
   - Compelling copy

6. **Footer**
   - 4 columns (About, Features, Technology, Security)
   - Copyright information
   - Professional dark theme

### Sign-In Flow

1. User clicks "Sign In with Google" button
2. Google OAuth popup appears
3. User selects Google account
4. Backend validates credentials
5. JWT token stored in localStorage
6. User redirected to role-specific dashboard:
   - Admin → `/admin`
   - Hospital → `/hospital`
   - Patient → `/patient`

## Design Features

### Animations
- Fade-in-up for hero text elements
- Floating animation for hero cards
- Hover effects on buttons and cards
- Smooth scroll for "Learn More" button

### Responsive Design
- Desktop: Full grid layouts, side-by-side sections
- Tablet: Adjusted grid columns, maintained spacing
- Mobile: Single column, stacked elements, full-width buttons

### Color Scheme
- Primary: Purple gradient (#667eea to #764ba2)
- Accent: Gold (#ffd700)
- Background: Light gray (#f8f9fa)
- Text: Dark gray (#333) and medium gray (#666)
- Footer: Dark navy (#1a1a2e)

### Typography
- Hero Title: 3.5rem (56px), bold
- Section Titles: 2.5rem (40px), bold
- Body Text: 1.2rem (19.2px), regular
- Buttons: 1.1rem (17.6px), semi-bold

## Testing

1. **Landing Page Display**:
   - Visit http://localhost:5173/
   - Should see hero section with gradient background
   - Floating cards should animate
   - All sections should be visible

2. **Sign-In Button**:
   - Click "Sign In with Google"
   - Google popup should appear
   - After login, redirect to appropriate dashboard

3. **Learn More Button**:
   - Click "Learn More"
   - Should smooth scroll to features section

4. **Responsive Design**:
   - Resize browser window
   - Layout should adapt at breakpoints (968px, 640px)
   - Mobile view should show single column

5. **Navigation**:
   - After login, navbar should appear
   - Landing page should not be accessible when logged in
   - Logout should return to landing page

## Customization

### Change Colors
Edit `frontend/src/styles/landing.css`:
```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Accent color */
color: #ffd700;
```

### Change Text
Edit `frontend/src/pages/LandingPage.jsx`:
```jsx
<h1 className="hero-title">
  Your Custom Title
  <span className="hero-subtitle">Your Subtitle</span>
</h1>
```

### Add/Remove Features
Edit the `features-grid` section in LandingPage.jsx:
```jsx
<div className="feature-card">
  <div className="feature-icon your-icon">🎯</div>
  <h3>Your Feature</h3>
  <p>Your description</p>
</div>
```

## Troubleshooting

### Landing Page Not Showing
- Check if frontend dev server is running: `npm run dev`
- Verify you're accessing http://localhost:5173/ (not 8000)
- Clear browser cache and reload

### Sign-In Button Not Working
- Check browser console for errors
- Verify Google Client ID is configured in .env
- Ensure backend is running on port 8000
- Check CORS settings in main.py

### Styling Issues
- Verify landing.css is imported in LandingPage.jsx
- Check browser developer tools for CSS errors
- Clear browser cache

### Routing Issues
- Check App.jsx has correct route configuration
- Verify BrowserRouter is wrapping all routes
- Check for console errors related to react-router-dom

## Production Deployment

For production, you'll need to:

1. Build the React app:
   ```bash
   cd frontend
   npm run build
   ```

2. Serve the built files from FastAPI:
   - Update main.py to serve from `frontend/dist`
   - Configure proper routing for SPA

3. Update CORS origins in main.py:
   ```python
   origins = [
       "https://yourdomain.com",
   ]
   ```

4. Set production environment variables in .env

## Next Steps

Consider adding:
- Testimonials section
- Pricing/plans section
- FAQ section
- Contact form
- Demo video
- Screenshots/mockups
- Blog/news section
- Social media links
