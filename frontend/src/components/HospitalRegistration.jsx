import { useState } from 'react';
import { hospitalAPI } from '../services/api';

export default function HospitalRegistration({ onRegistered }) {
  const [formData, setFormData] = useState({
    hospital_name: '',
    hospital_type: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await hospitalAPI.registerHospital(formData);
      onRegistered(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to register hospital');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="registration-container">
      <h3>Register Hospital</h3>
      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="registration-form">
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

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Registering...' : 'Register Hospital'}
        </button>
      </form>
    </div>
  );
}
