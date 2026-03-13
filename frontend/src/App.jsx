import { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { authAPI } from './services/api';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import AdminDashboard from './pages/AdminDashboard';
import HospitalDashboard from './pages/HospitalDashboard';
import PatientDashboard from './pages/PatientDashboard';
import DoctorDashboard from './pages/DoctorDashboard';
import EmergencyDashboard from './pages/EmergencyDashboard';
import Navbar from './components/Navbar';
import ErrorBoundary from './components/ErrorBoundary';
import './styles/styles.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkSession();
  }, []);

  const checkSession = async () => {
    try {
      const response = await authAPI.getSession();
      if (response.data.user) {
        setUser(response.data.user);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
    } catch (error) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <ErrorBoundary>
      <BrowserRouter>
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <p>Loading...</p>
          </div>
        ) : (
          <>
            {user && <Navbar user={user} onLogout={handleLogout} />}
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={!user ? <LandingPage /> : <Navigate to={`/${user.role}`} />} />
              <Route path="/login" element={!user ? <Login onLoginSuccess={(userData) => setUser(userData)} /> : <Navigate to={`/${user.role}`} />} />
              
              {/* Protected Routes */}
              {user && user.role === 'admin' && (
                <Route path="/admin" element={<AdminDashboard user={user} />} />
              )}
              {user && user.role === 'hospital' && (
                <Route path="/hospital" element={<HospitalDashboard user={user} />} />
              )}
              {user && user.role === 'patient' && (
                <Route path="/patient" element={<PatientDashboard user={user} />} />
              )}
              {user && user.role === 'doctor' && (
                <Route path="/doctor" element={<DoctorDashboard user={user} />} />
              )}
              {user && (user.role === 'hospital' || user.role === 'emergency') && (
                <Route path="/emergency" element={<EmergencyDashboard user={user} />} />
              )}
              
              {/* Catch all - redirect to home */}
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </>
        )}
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
