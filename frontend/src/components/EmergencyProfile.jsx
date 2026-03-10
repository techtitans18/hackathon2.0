import { useState, useEffect } from 'react';
import { emergencyAPI } from '../services/api';

export default function EmergencyProfile({ selectedPatient, onProfileLoaded }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (selectedPatient?.health_id) {
      loadProfile();
    } else {
      setProfile(null);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedPatient]);

  const loadProfile = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await emergencyAPI.getProfile({
        role: 'hospital',
        health_id: selectedPatient.health_id,
      });
      setProfile(response.data);
      onProfileLoaded(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <p>Loading profile...</p>;
  if (error) return <div className="error-message">{error}</div>;
  if (!profile) return <p>Select a patient to view profile</p>;

  return (
    <div className="emergency-profile-card">
      <h3>Emergency Profile</h3>
      
      <div className="profile-header">
        <h4>{profile.name}</h4>
        <span className={`blockchain-badge ${profile.blockchain_status === 'Verified' ? 'verified' : 'tampered'}`}>
          {profile.blockchain_status}
        </span>
      </div>

      <div className="info-grid">
        <div className="info-item">
          <strong>Health ID:</strong>
          <span>{profile.health_id}</span>
        </div>
        <div className="info-item">
          <strong>Blood Group:</strong>
          <span className="blood-group">{profile.blood_group}</span>
        </div>
        <div className="info-item">
          <strong>Emergency Contact:</strong>
          <span>{profile.emergency_contact}</span>
        </div>
      </div>

      <div className="medical-lists">
        <div className="list-section">
          <strong>Allergies:</strong>
          {profile.allergies.length > 0 ? (
            <ul>
              {profile.allergies.map((item, idx) => (
                <li key={idx} className="allergy-item">{item}</li>
              ))}
            </ul>
          ) : (
            <p>None</p>
          )}
        </div>

        <div className="list-section">
          <strong>Diseases:</strong>
          {profile.diseases.length > 0 ? (
            <ul>
              {profile.diseases.map((item, idx) => (
                <li key={idx} className="disease-item">{item}</li>
              ))}
            </ul>
          ) : (
            <p>None</p>
          )}
        </div>

        <div className="list-section">
          <strong>Surgeries:</strong>
          {profile.surgeries.length > 0 ? (
            <ul>
              {profile.surgeries.map((item, idx) => (
                <li key={idx} className="surgery-item">{item}</li>
              ))}
            </ul>
          ) : (
            <p>None</p>
          )}
        </div>
      </div>
    </div>
  );
}
