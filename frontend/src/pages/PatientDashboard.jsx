import { useEffect, useState } from 'react';
import { patientAPI, recordAPI } from '../services/api';
import EHealthCard from '../components/EHealthCard';
import RecordTable from '../components/RecordTable';

export default function PatientDashboard({ user }) {
  const [profile, setProfile] = useState(null);
  const [eHealthCard, setEHealthCard] = useState(null);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPatientData();
  }, []);

  const loadPatientData = async () => {
    setLoading(true);
    try {
      const [profileRes, cardRes] = await Promise.all([
        patientAPI.getProfile(),
        patientAPI.getEHealthCard().catch(() => null),
      ]);

      const patientData = profileRes.data.patient;
      setProfile(patientData);
      
      // Use patient data for e-health card
      if (patientData) {
        setEHealthCard({
          health_id: patientData.HealthID,
          name: patientData.name,
          blood_group: patientData.blood_group,
          phone: patientData.phone,
          dob: patientData.dob,
          photo_url: patientData.photo_url,
          email: patientData.email,
        });
      }

      if (profileRes.data.records) {
        setRecords(profileRes.data.records);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load patient data');
      console.error('Error loading patient data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadFile = async (fileName) => {
    try {
      const response = await recordAPI.downloadFile(fileName);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();
      link.parentElement.removeChild(link);
    } catch (err) {
      alert('Failed to download file');
      console.error('Download error:', err);
    }
  };

  const handleDownloadSummary = async (summaryFileName) => {
    try {
      const response = await recordAPI.downloadSummary(summaryFileName);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', summaryFileName);
      document.body.appendChild(link);
      link.click();
      link.parentElement.removeChild(link);
    } catch (err) {
      alert('Failed to download summary');
      console.error('Download error:', err);
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
      <h2>Patient Dashboard</h2>

      {error && <div className="error-message">{error}</div>}

      {eHealthCard && (
        <div className="ehealth-card-section">
          <h3>e-Health Card</h3>
          <EHealthCard patient={eHealthCard} />
        </div>
      )}

      {profile && (
        <div className="profile-card">
          <h3>Profile Information</h3>
          <div className="info-grid">
            <p><strong>Health ID:</strong> {profile.HealthID}</p>
            <p><strong>Name:</strong> {profile.name}</p>
            <p><strong>Age:</strong> {profile.age}</p>
            <p><strong>Phone:</strong> {profile.phone}</p>
            <p><strong>Email:</strong> {profile.email}</p>
            <p><strong>Blood Group:</strong> {profile.blood_group}</p>
            <p><strong>DOB:</strong> {profile.dob}</p>
          </div>
        </div>
      )}

      <div className="records-section">
        <h3>Medical Records</h3>
        <RecordTable
          records={records}
          onDownload={handleDownloadFile}
          onDownloadSummary={handleDownloadSummary}
        />
      </div>
    </div>
  );
}