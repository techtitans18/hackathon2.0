import { useState } from 'react';
import { hospitalAPI } from '../services/api';

export default function AddHospital({ onHospitalAdded }) {
  const [formData, setFormData] = useState({
    hospital_name: '',
    hospital_type: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleAddHospital = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const response = await hospitalAPI.registerHospital(formData);
      setSuccessMessage('Hospital added successfully!');
      setFormData({
        hospital_name: '',
        hospital_type: '',
      });
      onHospitalAdded(response.data);
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add hospital');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="hospital-form-container">
      <h3>Add New Hospital</h3>
      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      <form onSubmit={handleAddHospital} className="hospital-form">
        <div className="form-group">
          <label>Hospital Name *</label>
          <input
            type="text"
            name="hospital_name"
            value={formData.hospital_name}
            onChange={handleInputChange}
            required
            placeholder="Enter hospital name"
            maxLength="180"
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
            maxLength="120"
          />
        </div>

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Adding Hospital...' : 'Add Hospital'}
        </button>
      </form>
    </div>
  );
}
