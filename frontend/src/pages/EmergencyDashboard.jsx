import { useState, useEffect } from 'react';
import { aiAPI } from '../services/api';
import EmergencySearch from '../components/EmergencySearch';
import EmergencyProfile from '../components/EmergencyProfile';
import EmergencyUpdateData from '../components/EmergencyUpdateData';

export default function EmergencyDashboard({ user }) {
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [aiHealthStatus, setAiHealthStatus] = useState(null);
  const [activeTab, setActiveTab] = useState('search');
  const [loadingAI, setLoadingAI] = useState(true);

  useEffect(() => {
    checkAIHealth();
  }, []);

  const checkAIHealth = async () => {
    try {
      const response = await aiAPI.getHealth();
      setAiHealthStatus(response.data);
    } catch (err) {
      console.error('Failed to check AI health:', err);
      setAiHealthStatus({
        ready: false,
        status: 'error',
        reason: 'Failed to check AI model status',
      });
    } finally {
      setLoadingAI(false);
    }
  };

  const handlePatientFound = (patient) => {
    setSelectedPatient(patient);
    setActiveTab('profile');
  };

  const handleDataUpdated = (updatedData) => {
    setSelectedPatient({
      ...selectedPatient,
      ...updatedData,
    });
  };

  return (
    <div className="dashboard-container">
      <h2>Emergency Access Dashboard</h2>

      {/* AI Health Status */}
      {!loadingAI && aiHealthStatus && (
        <div className={`ai-health-status ${aiHealthStatus.ready ? 'ready' : 'unavailable'}`}>
          <div className="health-status-content">
            <h4>AI Summary Model Status: {aiHealthStatus.status}</h4>
            <p>
              <strong>Model:</strong> {aiHealthStatus.model}
            </p>
            {aiHealthStatus.reason && (
              <p>
                <strong>Note:</strong> {aiHealthStatus.reason}
              </p>
            )}
          </div>
        </div>
      )}

      <div className="tab-navigation">
        <button
          className={`tab-btn ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          Search Patient
        </button>
        <button
          className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
          disabled={!selectedPatient}
        >
          View Profile
        </button>
        <button
          className={`tab-btn ${activeTab === 'update' ? 'active' : ''}`}
          onClick={() => setActiveTab('update')}
          disabled={!selectedPatient}
        >
          Update Data
        </button>
      </div>

      <div className="emergency-content">
        {activeTab === 'search' && (
          <EmergencySearch onPatientFound={handlePatientFound} />
        )}

        {activeTab === 'profile' && (
          <EmergencyProfile
            selectedPatient={selectedPatient}
            onProfileLoaded={() => {}}
          />
        )}

        {activeTab === 'update' && (
          <EmergencyUpdateData
            selectedPatient={selectedPatient}
            onDataUpdated={handleDataUpdated}
          />
        )}
      </div>
    </div>
  );
}
