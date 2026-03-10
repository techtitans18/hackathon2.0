import { useEffect, useState } from 'react';
import { patientAPI, aiAPI } from '../services/api';

export default function PatientWorkspace({ user }) {
  const [profile, setProfile] = useState(null);
  const [records, setRecords] = useState([]);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [summarizing, setSummarizing] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPatientData();
  }, []);

  const loadPatientData = async () => {
    setLoading(true);
    try {
      const response = await patientAPI.getProfile();
      setProfile(response.data);
      if (response.data.records) {
        setRecords(response.data.records);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load patient data');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSummary = async (record) => {
    if (!record.summary_file_name) {
      alert('No summary available for this record');
      return;
    }

    setSummarizing(true);
    setSummary(null);

    try {
      const response = await aiAPI.generateSummary({
        user_id: user.email,
        role: user.role,
        health_id: user.health_id,
        report_text: record.description,
      });
      setSummary(response.data.summary);
    } catch (err) {
      alert('Failed to generate summary: ' + (err.response?.data?.error || err.message));
      console.error('Error:', err);
    } finally {
      setSummarizing(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <h2>Patient Workspace</h2>

      {error && <div className="error-message">{error}</div>}

      {profile && (
        <div className="profile-card">
          <h3>Your Information</h3>
          <div className="info-grid">
            <p><strong>Health ID:</strong> {profile.HealthID}</p>
            <p><strong>Name:</strong> {profile.name}</p>
            <p><strong>Email:</strong> {profile.email}</p>
            <p><strong>Blood Group:</strong> {profile.blood_group}</p>
          </div>
        </div>
      )}

      <div className="records-section">
        <h3>My Medical Records</h3>
        {records.length === 0 ? (
          <p>No medical records available</p>
        ) : (
          <div className="records-list">
            {records.map((record, idx) => (
              <div
                key={idx}
                className={`record-item ${selectedRecord === idx ? 'selected' : ''}`}
                onClick={() => {
                  setSelectedRecord(selectedRecord === idx ? null : idx);
                  setSummary(null);
                }}
              >
                <div className="record-header">
                  <h4>{record.record_type}</h4>
                  <span className="record-date">
                    {new Date(record.timestamp).toLocaleDateString()}
                  </span>
                </div>

                {selectedRecord === idx && (
                  <div className="record-details">
                    <p><strong>Description:</strong> {record.description}</p>
                    <p><strong>Hospital:</strong> {record.HospitalID}</p>
                    <p><strong>Record Hash:</strong> <code>{record.record_hash?.substring(0, 16)}...</code></p>

                    {record.summary_file_name && (
                      <button
                        className="btn-small"
                        onClick={() => handleGenerateSummary(record)}
                        disabled={summarizing}
                      >
                        {summarizing ? 'Generating...' : 'Generate Summary'}
                      </button>
                    )}

                    {summary && (
                      <div className="summary-box">
                        <h5>AI-Generated Summary:</h5>
                        <p>{summary}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
