import { useState, useEffect } from 'react';
import { emergencyAPI } from '../services/api';

export default function EmergencyUpdateData({ selectedPatient, onDataUpdated }) {
  const [formData, setFormData] = useState({
    blood_group: '',
    emergency_contact: '',
    allergies: '',
    diseases: '',
    surgeries: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (selectedPatient) {
      setFormData({
        blood_group: selectedPatient.blood_group || '',
        emergency_contact: selectedPatient.emergency_contact || '',
        allergies: selectedPatient.allergies?.join(', ') || '',
        diseases: selectedPatient.diseases?.join(', ') || '',
        surgeries: selectedPatient.surgeries?.join(', ') || '',
      });
    }
  }, [selectedPatient]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const payload = {
        role: 'hospital',
        health_id: selectedPatient.health_id,
        blood_group: formData.blood_group,
        emergency_contact: formData.emergency_contact,
        allergies: formData.allergies.split(',').map(s => s.trim()).filter(Boolean),
        diseases: formData.diseases.split(',').map(s => s.trim()).filter(Boolean),
        surgeries: formData.surgeries.split(',').map(s => s.trim()).filter(Boolean),
      };

      const response = await emergencyAPI.upsertData(payload);
      setSuccess(true);
      onDataUpdated(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update data');
    } finally {
      setLoading(false);
    }
  };

  if (!selectedPatient) {
    return <p>Select a patient to update emergency data</p>;
  }

  return (
    <div className="emergency-update-card">
      <h3>Update Emergency Data</h3>
      <p className="patient-name">Patient: {selectedPatient.name}</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Blood Group:</label>
          <select
            value={formData.blood_group}
            onChange={(e) => setFormData({ ...formData, blood_group: e.target.value })}
            required
          >
            <option value="">Select</option>
            <option value="A+">A+</option>
            <option value="A-">A-</option>
            <option value="B+">B+</option>
            <option value="B-">B-</option>
            <option value="AB+">AB+</option>
            <option value="AB-">AB-</option>
            <option value="O+">O+</option>
            <option value="O-">O-</option>
          </select>
        </div>

        <div className="form-group">
          <label>Emergency Contact:</label>
          <input
            type="text"
            value={formData.emergency_contact}
            onChange={(e) => setFormData({ ...formData, emergency_contact: e.target.value })}
            required
          />
        </div>

        <div className="form-group">
          <label>Allergies (comma-separated):</label>
          <textarea
            value={formData.allergies}
            onChange={(e) => setFormData({ ...formData, allergies: e.target.value })}
            placeholder="e.g., Penicillin, Peanuts"
          />
        </div>

        <div className="form-group">
          <label>Diseases (comma-separated):</label>
          <textarea
            value={formData.diseases}
            onChange={(e) => setFormData({ ...formData, diseases: e.target.value })}
            placeholder="e.g., Diabetes, Hypertension"
          />
        </div>

        <div className="form-group">
          <label>Surgeries (comma-separated):</label>
          <textarea
            value={formData.surgeries}
            onChange={(e) => setFormData({ ...formData, surgeries: e.target.value })}
            placeholder="e.g., Appendectomy, Knee Surgery"
          />
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">Data updated successfully!</div>}

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Updating...' : 'Update Emergency Data'}
        </button>
      </form>
    </div>
  );
}
