import { useEffect, useState } from 'react';
import { hospitalAPI, patientAPI, emergencyAPI } from '../services/api';
import HospitalRegistration from '../components/HospitalRegistration';
import PatientRegistration from '../components/PatientRegistration';
import UploadRecord from '../components/UploadRecord';
import BlockchainViewer from '../components/BlockchainViewer';
import PatientAccess from '../components/PatientAccess';

export default function HospitalDashboard({ user }) {
  const [hospitalData, setHospitalData] = useState(user.hospital_id ? { HospitalID: user.hospital_id } : null);
  const [blockchain, setBlockchain] = useState(null);
  const [activeTab, setActiveTab] = useState(hospitalData ? 'register-patient' : 'register-hospital');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchHealthId, setSearchHealthId] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [emergencySearchType, setEmergencySearchType] = useState('health_id');
  const [emergencySearchValue, setEmergencySearchValue] = useState('');
  const [emergencySearchName, setEmergencySearchName] = useState('');
  const [emergencySearchDob, setEmergencySearchDob] = useState('');
  const [emergencyProfile, setEmergencyProfile] = useState(null);
  const [emergencyLoading, setEmergencyLoading] = useState(false);

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

  const handleEmergencySearch = async (e) => {
    e.preventDefault();
    setEmergencyLoading(true);
    setError(null);
    setEmergencyProfile(null);

    try {
      const payload = {
        role: 'hospital',
        search_type: emergencySearchType,
        value: emergencySearchType !== 'name_dob' ? emergencySearchValue : null,
        name: emergencySearchType === 'name_dob' ? emergencySearchName : null,
        dob: emergencySearchType === 'name_dob' ? emergencySearchDob : null,
      };

      const searchResponse = await emergencyAPI.searchPatient(payload);
      
      if (searchResponse.data.health_id) {
        const profileResponse = await emergencyAPI.getProfile({
          role: 'hospital',
          health_id: searchResponse.data.health_id,
        });
        setEmergencyProfile(profileResponse.data);
      }
    } catch (err) {
      setError(err.response?.data?.error || err.response?.data?.detail || 'Patient not found');
    } finally {
      setEmergencyLoading(false);
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
              className={`tab-btn ${activeTab === 'patient-access' ? 'active' : ''}`}
              onClick={() => setActiveTab('patient-access')}
            >
              Patient Access (OTP)
            </button>
            <button
              className={`tab-btn ${activeTab === 'emergency-access' ? 'active' : ''}`}
              onClick={() => setActiveTab('emergency-access')}
            >
              Emergency Access
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

          {activeTab === 'patient-access' && (
            <PatientAccess />
          )}

          {activeTab === 'emergency-access' && (
            <div className="emergency-search-section">
              <h3>Emergency Patient Access</h3>
              <p className="info-text">Search for patient using Health ID, Phone, or Name + DOB</p>
              
              <form onSubmit={handleEmergencySearch} className="emergency-form">
                <div className="form-group">
                  <label>Search By:</label>
                  <select 
                    value={emergencySearchType} 
                    onChange={(e) => {
                      setEmergencySearchType(e.target.value);
                      setEmergencySearchValue('');
                      setEmergencySearchName('');
                      setEmergencySearchDob('');
                    }}
                  >
                    <option value="health_id">Health ID</option>
                    <option value="phone">Phone Number</option>
                    <option value="name_dob">Name + Date of Birth</option>
                  </select>
                </div>

                {emergencySearchType !== 'name_dob' ? (
                  <div className="form-group">
                    <label>{emergencySearchType === 'health_id' ? 'Health ID' : 'Phone Number'}:</label>
                    <input
                      type="text"
                      value={emergencySearchValue}
                      onChange={(e) => setEmergencySearchValue(e.target.value)}
                      placeholder={emergencySearchType === 'health_id' ? 'Enter Health ID' : 'Enter Phone Number'}
                      required
                    />
                  </div>
                ) : (
                  <>
                    <div className="form-group">
                      <label>Patient Name:</label>
                      <input
                        type="text"
                        value={emergencySearchName}
                        onChange={(e) => setEmergencySearchName(e.target.value)}
                        placeholder="Enter patient name"
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Date of Birth:</label>
                      <input
                        type="date"
                        value={emergencySearchDob}
                        onChange={(e) => setEmergencySearchDob(e.target.value)}
                        required
                      />
                    </div>
                  </>
                )}

                <button type="submit" disabled={emergencyLoading} className="btn-primary">
                  {emergencyLoading ? 'Searching...' : 'Search Patient'}
                </button>
              </form>

              {emergencyProfile && (
                <div className="emergency-profile-result">
                  <div className="profile-header">
                    <h4>{emergencyProfile.name}</h4>
                    <span className={`blockchain-badge ${emergencyProfile.blockchain_status === 'Verified' ? 'verified' : 'tampered'}`}>
                      {emergencyProfile.blockchain_status}
                    </span>
                  </div>

                  <div className="emergency-info-grid">
                    <div className="info-card">
                      <strong>Health ID:</strong>
                      <span>{emergencyProfile.health_id}</span>
                    </div>
                    <div className="info-card blood-group-card">
                      <strong>Blood Group:</strong>
                      <span className="blood-group">{emergencyProfile.blood_group}</span>
                    </div>
                    <div className="info-card">
                      <strong>Emergency Contact:</strong>
                      <span>{emergencyProfile.emergency_contact}</span>
                    </div>
                  </div>

                  <div className="medical-details">
                    <div className="detail-section">
                      <h5>Allergies</h5>
                      {emergencyProfile.allergies.length > 0 ? (
                        <ul className="medical-list">
                          {emergencyProfile.allergies.map((item, idx) => (
                            <li key={idx} className="allergy-item">{item}</li>
                          ))}
                        </ul>
                      ) : (
                        <p className="no-data">No allergies recorded</p>
                      )}
                    </div>

                    <div className="detail-section">
                      <h5>Diseases</h5>
                      {emergencyProfile.diseases.length > 0 ? (
                        <ul className="medical-list">
                          {emergencyProfile.diseases.map((item, idx) => (
                            <li key={idx} className="disease-item">{item}</li>
                          ))}
                        </ul>
                      ) : (
                        <p className="no-data">No diseases recorded</p>
                      )}
                    </div>

                    <div className="detail-section">
                      <h5>Surgeries</h5>
                      {emergencyProfile.surgeries.length > 0 ? (
                        <ul className="medical-list">
                          {emergencyProfile.surgeries.map((item, idx) => (
                            <li key={idx} className="surgery-item">{item}</li>
                          ))}
                        </ul>
                      ) : (
                        <p className="no-data">No surgeries recorded</p>
                      )}
                    </div>
                  </div>
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
