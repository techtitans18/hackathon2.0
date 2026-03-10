import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { authAPI } from './services/api';
import './index.css';

function Root() {
  const [googleClientId, setGoogleClientId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    authAPI.getConfig()
      .then(res => {
        setGoogleClientId(res.data.google_client_id);
      })
      .catch(() => {
        setGoogleClientId('165263253258-ovu9rturd77q38ak6hp72ihsv148kr34.apps.googleusercontent.com');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Loading...</div>;
  }

  if (!googleClientId) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Google OAuth not configured</div>;
  }

  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      <App />
    </GoogleOAuthProvider>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>
);
