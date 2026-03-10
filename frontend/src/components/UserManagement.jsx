import { useState } from 'react';
import { adminAPI } from '../services/api';

export default function UserManagement({ users, onUserUpdated }) {
  const [formData, setFormData] = useState({
    email: '',
    role: 'patient',
    name: '',
    health_id: '',
    hospital_name: '',
    hospital_type: '',
    is_active: true,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);



  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      await adminAPI.upsertUser(formData);
      setSuccess('User created/updated successfully');
      setFormData({
        email: '',
        role: 'patient',
        name: '',
        health_id: '',
        hospital_name: '',
        hospital_type: '',
        is_active: true,
      });
      onUserUpdated();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create/update user');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="user-management">
      <div className="form-section">
        <h3>Create/Update User</h3>
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <form onSubmit={handleSubmit} className="admin-form">
          <div className="form-group">
            <label>Email *</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Role *</label>
            <select
              name="role"
              value={formData.role}
              onChange={handleInputChange}
              required
            >
              <option value="admin">Admin</option>
              <option value="hospital">Hospital</option>
              <option value="patient">Patient</option>
            </select>
          </div>

          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
            />
          </div>

          {formData.role === 'patient' && (
            <div className="form-group">
              <label>Health ID</label>
              <input
                type="text"
                name="health_id"
                value={formData.health_id}
                onChange={handleInputChange}
                placeholder="Leave empty if not registered yet"
              />
            </div>
          )}

          {formData.role === 'hospital' && (
            <>
              <div className="form-group">
                <label>Hospital Name *</label>
                <input
                  type="text"
                  name="hospital_name"
                  value={formData.hospital_name}
                  onChange={handleInputChange}
                  required
                  placeholder="Enter hospital name"
                />
              </div>

              <div className="form-group">
                <label>Hospital Type *</label>
                <input
                  type="text"
                  name="hospital_type"
                  value={formData.hospital_type}
                  onChange={handleInputChange}
                  required
                  placeholder="e.g., General, Specialty, Emergency"
                />
              </div>
              <p className="info-text">Hospital ID will be auto-generated from name and type</p>
            </>
          )}

          <div className="form-group">
            <label>
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleInputChange}
              />
              Active
            </label>
          </div>

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Saving...' : 'Save User'}
          </button>
        </form>
      </div>

      <div className="users-section">
        <h3>Users List</h3>
        <table className="users-table">
          <thead>
            <tr>
              <th>Email</th>
              <th>Role</th>
              <th>Name</th>
              <th>Status</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user, idx) => (
              <tr key={idx}>
                <td>{user.email}</td>
                <td>{user.role}</td>
                <td>{user.name || '-'}</td>
                <td>{user.is_active ? 'Active' : 'Inactive'}</td>
                <td>
                  {user.created_at
                    ? new Date(user.created_at).toLocaleDateString()
                    : '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
