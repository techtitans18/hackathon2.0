import { useState, useEffect } from 'react';
import { hospitalAPI } from '../services/api';

export default function UpdateHospital({ onHospitalUpdated }) {
  const [hospitals, setHospitals] = useState([]);
  const [selectedHospitalId, setSelectedHospitalId] = useState('');
  const [selectedHospital, setSelectedHospital] = useState(null);
  const [formData, setFormData] = useState({
    hospital_name: '',
    hospital_type: '',
  });
  const [loading, setLoading] = useState(false);
  const [loadingHospitals, setLoadingHospitals] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // Load hospitals on mount
  useEffect(() => {
    loadHospitals();
  }, []);

  // Update form when hospital is selected
  useEffect(() => {
    if (selectedHospitalId) {
      const hospital = hospitals.find((h) => h.hospital_id === selectedHospitalId);
      if (hospital) {
        setSelectedHospital(hospital);
        setFormData({
          hospital_name: hospital.hospital_name,
          hospital_type: hospital.hospital_type,
        });
      }
    } else {
      setSelectedHospital(null);
      setFormData({
        hospital_name: '',
        hospital_type: '',
      });
    }
  }, [selectedHospitalId, hospitals]);

  const loadHospitals = async () => {
    setLoadingHospitals(true);
    try {
      const response = await hospitalAPI.listHospitals();
      setHospitals(response.data.hospitals || []);
      setError(null);
    } catch (err) {
      setError('Failed to load hospitals');
      console.error('Error loading hospitals:', err);
    } finally {
      setLoadingHospitals(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleUpdateHospital = async (e) => {
    e.preventDefault();
    if (!selectedHospitalId) {
      setError('Please select a hospital first');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      await hospitalAPI.updateHospital(selectedHospitalId, formData);
      setSuccessMessage('Hospital updated successfully!');
      onHospitalUpdated({
        hospital_id: selectedHospitalId,
        ...formData,
      });
      setTimeout(() => setSuccessMessage(null), 3000);
      // Reload hospitals to reflect changes
      loadHospitals();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update hospital');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="hospital-form-container">
      <h3>Update Hospital Details</h3>
      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      {loadingHospitals ? (
        <p className="loading-text">Loading hospitals...</p>
      ) : hospitals.length === 0 ? (
        <p className="empty-message">No hospitals registered yet</p>
      ) : (
        <form onSubmit={handleUpdateHospital} className="hospital-form">
          <div className="form-group">
            <label>Select Hospital *</label>
            <select
              value={selectedHospitalId}
              onChange={(e) => setSelectedHospitalId(e.target.value)}
              required
              className="form-select"
            >
              <option value="">-- Choose a Hospital --</option>
              {hospitals.map((hospital) => (
                <option key={hospital.hospital_id} value={hospital.hospital_id}>
                  {hospital.hospital_name} ({hospital.hospital_type})
                </option>
              ))}
            </select>
          </div>

          {selectedHospital && (
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
                {loading ? 'Updating Hospital...' : 'Update Hospital'}
              </button>
            </>
          )}
        </form>
      )}
    </div>
  );
}
