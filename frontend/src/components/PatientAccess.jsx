import React, { useState } from 'react';
import patientAccessAPI from '../api/patientAccessAPI';

const PatientAccess = () => {
  const [searchType, setSearchType] = useState('health_id');
  const [searchValue, setSearchValue] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [maskedEmail, setMaskedEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [patientData, setPatientData] = useState(null);

  const handleSendOTP = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await patientAccessAPI.sendOTP(searchType, searchValue);
      setOtpSent(true);
      setMaskedEmail(response.data.email_masked);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send OTP');
      setOtpSent(false);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await patientAccessAPI.verifyOTP(searchType, searchValue, otp);
      setPatientData(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid OTP');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSearchValue('');
    setOtp('');
    setOtpSent(false);
    setMaskedEmail('');
    setError('');
    setPatientData(null);
  };

  const downloadFile = (url) => {
    window.open(`http://127.0.0.1:8000${url}`, '_blank');
  };

  if (patientData) {
    return (
      <div className="patient-access-container">
        <div className="patient-access-header">
          <h3>Patient Records Access</h3>
          <button onClick={handleReset} className="btn-secondary">New Search</button>
        </div>

        <div className="patient-profile-card">
          <h4>Patient Information</h4>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Health ID:</span>
              <span className="value">{patientData.patient.health_id}</span>
            </div>
            <div className="info-item">
              <span className="label">Name:</span>
              <span className="value">{patientData.patient.name}</span>
            </div>
            <div className="info-item">
              <span className="label">Age:</span>
              <span className="value">{patientData.patient.age}</span>
            </div>
            <div className="info-item">
              <span className="label">Phone:</span>
              <span className="value">{patientData.patient.phone}</span>
            </div>
            <div className="info-item">
              <span className="label">Email:</span>
              <span className="value">{patientData.patient.email}</span>
            </div>
            <div className="info-item">
              <span className="label">Blood Group:</span>
              <span className="value blood-group">{patientData.patient.blood_group}</span>
            </div>
          </div>
        </div>

        <div className="records-section">
          <h4>Medical Records ({patientData.records.length})</h4>
          {patientData.records.length === 0 ? (
            <p className="no-data">No medical records found</p>
          ) : (
            <div className="records-list">
              {patientData.records.map((record, index) => (
                <div key={index} className="record-card">
                  <div className="record-header">
                    <span className="record-type">{record.record_type}</span>
                    <span className="record-date">
                      {new Date(record.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="record-description">{record.description}</p>
                  <div className="record-actions">
                    {record.download_url && (
                      <button
                        onClick={() => downloadFile(record.download_url)}
                        className="btn-download"
                      >
                        📄 Download File
                      </button>
                    )}
                    {record.summary_download_url && (
                      <button
                        onClick={() => downloadFile(record.summary_download_url)}
                        className="btn-download"
                      >
                        📝 AI Summary
                      </button>
                    )}
                  </div>
                  <div className="record-hash">
                    Hash: {record.record_hash?.substring(0, 16)}...
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="patient-access-container">
      <h3>Patient Access - OTP Verification</h3>
      <p className="access-info">
        Search for a patient and verify access via email OTP (Health ID, Mobile, or Email)
      </p>

      {!otpSent ? (
        <form onSubmit={handleSendOTP} className="access-form">
          <div className="form-group">
            <label>Search By:</label>
            <select
              value={searchType}
              onChange={(e) => setSearchType(e.target.value)}
              className="form-control"
            >
              <option value="health_id">Health ID</option>
              <option value="mobile">Mobile Number</option>
              <option value="email">Email Address</option>
            </select>
          </div>

          <div className="form-group">
            <label>
              {searchType === 'health_id' ? 'Health ID' : searchType === 'mobile' ? 'Mobile Number' : 'Email Address'}:
            </label>
            <input
              type="text"
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              placeholder={
                searchType === 'health_id' 
                  ? 'Enter Health ID' 
                  : searchType === 'mobile' 
                  ? 'Enter Mobile Number'
                  : 'Enter Email Address'
              }
              className="form-control"
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Sending...' : 'Send OTP'}
          </button>
        </form>
      ) : (
        <form onSubmit={handleVerifyOTP} className="access-form">
          <div className="otp-sent-message">
            ✅ OTP sent to {maskedEmail}
          </div>

          <div className="form-group">
            <label>Enter OTP:</label>
            <input
              type="text"
              value={otp}
              onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').substring(0, 6))}
              placeholder="Enter 6-digit OTP"
              className="form-control otp-input"
              maxLength="6"
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="button-group">
            <button type="submit" disabled={loading || otp.length !== 6} className="btn-primary">
              {loading ? 'Verifying...' : 'Verify OTP'}
            </button>
            <button type="button" onClick={handleReset} className="btn-secondary">
              Cancel
            </button>
          </div>

          <div className="resend-link">
            <button type="button" onClick={handleSendOTP} className="link-button">
              Resend OTP
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default PatientAccess;
