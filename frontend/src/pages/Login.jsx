import { useState } from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { authAPI } from '../services/api';

export default function Login({ onLoginSuccess }) {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLoginSuccess = async (credentialResponse) => {
    setLoading(true);
    setError(null);

    try {
      const response = await authAPI.googleLogin(
        credentialResponse.credential
      );

      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        onLoginSuccess(response.data.user);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLoginError = () => {
    setError('Google login failed');
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Healthcare Blockchain System</h1>
        <p>Sign in with Google to access your medical records</p>

        {error && <div className="error-message">{error}</div>}

        <div className="google-login-wrapper">
          {!loading && (
            <GoogleLogin
              onSuccess={handleLoginSuccess}
              onError={handleLoginError}
            />
          )}
          {loading && <p>Signing in...</p>}
        </div>

        <div className="login-info">
          <h3>Roles:</h3>
          <ul>
            <li><strong>Admin:</strong> Manage hospitals and users</li>
            <li><strong>Hospital:</strong> Register patients and upload records</li>
            <li><strong>Patient:</strong> View personal medical records</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
