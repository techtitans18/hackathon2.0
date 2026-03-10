import { useState } from 'react';
import { authAPI } from '../services/api';

export default function Navbar({ user, onLogout }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    }
    onLogout();
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>Healthcare Blockchain</h1>
      </div>

      <div className="navbar-content">
        <span className="role-badge">{user.role.toUpperCase()}</span>
        <span className="user-email">{user.email}</span>

        <div className="dropdown">
          <button
            className="dropdown-toggle"
            onClick={() => setDropdownOpen(!dropdownOpen)}
          >
            ☰
          </button>

          {dropdownOpen && (
            <div className="dropdown-menu">
              <div className="dropdown-item">
                <strong>{user.name}</strong>
              </div>
              <div className="dropdown-item">
                {user.role === 'patient' && user.health_id && (
                  <p>Health ID: {user.health_id}</p>
                )}
                {user.role === 'hospital' && user.hospital_id && (
                  <p>Hospital ID: {user.hospital_id}</p>
                )}
              </div>
              <button
                className="logout-btn"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
