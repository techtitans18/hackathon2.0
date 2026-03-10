import { useEffect, useState } from 'react';
import { hospitalAPI, recordAPI } from '../services/api';
import HospitalRegistration from '../components/HospitalRegistration';
import PatientRegistration from '../components/PatientRegistration';
import UploadRecord from '../components/UploadRecord';
import BlockchainViewer from '../components/BlockchainViewer';

export default function HospitalDashboard({ user }) {
  const [hospitalData, setHospitalData] = useState(user.hospital_id ? { HospitalID: user.hospital_id } : null);
  const [blockchain, setBlockchain] = useState(null);
  const [activeTab, setActiveTab] = useState(hospitalData ? 'register-patient' : 'register-hospital');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchHealthId, setSearchHealthId] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);

  useEffect(() => {
    if (hospitalData) {
      loadBlockchain();
    }
  }, [hospitalData]);

  const loadBlockchain = async () => {
    try {
      const response = await hospitalAPI.getBlockchain();
      setBlockchain(response.data);
    } catch (err) {
      console.error('Error loading blockchain:', err);
    }
  };

  const handleHospitalRegistered = (data) => {
    setHospitalData(data);
    setActiveTab('register-patient');
    setError(null);
  };

  const handleRecordUploaded = () => {
    loadBlockchain();
  };

  const handleSearchPatient = async (e) => {
    e.preventDefault();
    if (!searchHealthId.trim()) {
      setError('Please enter a health ID');
      return;
    }

    setSearchLoading(true);
    setError(null);
    try {
      const response = await patientAPI.getPatientByID(searchHealthId);
      setSearchResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Patient not found');
      setSearchResult(null);
    } finally {
      setSearchLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <h2>Hospital Dashboard</h2>

      {error && <div className="error-message">{error}</div>}

      {!hospitalData ? (
        <HospitalRegistration onRegistered={handleHospitalRegistered} />
      ) : (
        <>
          <div className="hospital-info">
            <p><strong>Hospital ID:</strong> {hospitalData.HospitalID}</p>
          </div>

          <div className="tab-navigation">
            <button
              className={`tab-btn ${activeTab === 'register-patient' ? 'active' : ''}`}
              onClick={() => setActiveTab('register-patient')}
            >
              Register Patient
            </button>
            <button
              className={`tab-btn ${activeTab === 'upload-record' ? 'active' : ''}`}
              onClick={() => setActiveTab('upload-record')}
            >
              Upload Record
            </button>
            <button
              className={`tab-btn ${activeTab === 'search-patient' ? 'active' : ''}`}
              onClick={() => setActiveTab('search-patient')}
            >
              Search Patient
            </button>
            <button
              className={`tab-btn ${activeTab === 'blockchain' ? 'active' : ''}`}
              onClick={() => setActiveTab('blockchain')}
            >
              Blockchain
            </button>
          </div>

          {activeTab === 'register-patient' && (
            <PatientRegistration hospitalId={hospitalData.HospitalID} />
          )}

          {activeTab === 'upload-record' && (
            <UploadRecord
              hospitalId={hospitalData.HospitalID}
              onRecordUploaded={handleRecordUploaded}
            />
          )}

          {activeTab === 'search-patient' && (
            <div className="search-patient-section">
              <h3>Search Patient Records</h3>
              <form onSubmit={handleSearchPatient} className="search-form">
                <input
                  type="text"
                  placeholder="Enter patient health ID..."
                  value={searchHealthId}
                  onChange={(e) => setSearchHealthId(e.target.value)}
                />
                <button type="submit" disabled={searchLoading} className="btn-primary">
                  {searchLoading ? 'Searching...' : 'Search'}
                </button>
              </form>

              {searchResult && (
                <div className="search-result-card">
                  <h4>{searchResult.patient?.name}</h4>
                  <div className="info-grid">
                    <p><strong>Health ID:</strong> {searchResult.patient?.HealthID}</p>
                    <p><strong>Age:</strong> {searchResult.patient?.age}</p>
                    <p><strong>Email:</strong> {searchResult.patient?.email}</p>
                    <p><strong>Blood Group:</strong> {searchResult.patient?.blood_group}</p>
                  </div>
                  
                  {searchResult.records && searchResult.records.length > 0 && (
                    <div className="records-section" style={{ marginTop: '2rem' }}>
                      <h4>Medical Records</h4>
                      <table className="records-table">
                        <thead>
                          <tr>
                            <th>Type</th>
                            <th>Description</th>
                            <th>Date</th>
                          </tr>
                        </thead>
                        <tbody>
                          {searchResult.records.map((record, idx) => (
                            <tr key={idx}>
                              <td>{record.record_type}</td>
                              <td>{record.description}</td>
                              <td>{new Date(record.timestamp).toLocaleDateString()}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {activeTab === 'blockchain' && blockchain && (
            <BlockchainViewer blockchain={blockchain} />
          )}
        </>
      )}
    </div>
  );
}
