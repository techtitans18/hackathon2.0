import { useState } from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { authAPI } from '../services/api';
import api from '../services/api';

export default function Login({ onLoginSuccess }) {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showEmailLogin, setShowEmailLogin] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleGoogleLoginSuccess = async (credentialResponse) => {
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

  const handleEmailLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await api.post('/auth/login', {
        email,
        password,
      });

      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        onLoginSuccess(response.data.user);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password');
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
        <p>Sign in to access your medical records</p>

        {error && <div className="error-message">{error}</div>}

        {!showEmailLogin ? (
          <>
            <div className="google-login-wrapper">
              {!loading && (
                <GoogleLogin
                  onSuccess={handleGoogleLoginSuccess}
                  onError={handleLoginError}
                />
              )}
              {loading && <p>Signing in...</p>}
            </div>

            <div className="login-divider">
              <span>OR</span>
            </div>

            <button
              className="email-login-btn"
              onClick={() => setShowEmailLogin(true)}
              disabled={loading}
            >
              Sign in with Email
            </button>
          </>
        ) : (
          <>
            <form onSubmit={handleEmailLogin} className="email-login-form">
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                  disabled={loading}
                />
              </div>

              <button
                type="submit"
                className="login-submit-btn"
                disabled={loading}
              >
                {loading ? 'Signing in...' : 'Sign In'}
              </button>
            </form>

            <button
              className="back-to-google-btn"
              onClick={() => setShowEmailLogin(false)}
              disabled={loading}
            >
              ← Back to Google Sign-In
            </button>
          </>
        )}

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
