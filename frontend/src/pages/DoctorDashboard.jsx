import { useEffect, useState } from 'react';
import { hospitalAPI, recordAPI } from '../services/api';

export default function DoctorDashboard({ user }) {
  const [blockchain, setBlockchain] = useState(null);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedHash, setSelectedHash] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const response = await hospitalAPI.getBlockchain();
      setBlockchain(response.data);
      if (response.data.chain) {
        // Filter non-genesis blocks
        const filtered = response.data.chain.filter((b) => b.RecordType !== 'GENESIS');
        setRecords(filtered);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load blockchain');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchByHash = async (e) => {
    e.preventDefault();
    if (!selectedHash.trim()) return;

    setLoading(true);
    try {
      const response = await recordAPI.getRecordByHash(selectedHash);
      setRecords(response.data.records || []);
    } catch (err) {
      setError('Record not found or error occurred');
      setRecords([]);
    } finally {
      setLoading(false);
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
      <h2>Doctor Dashboard</h2>

      {error && <div className="error-message">{error}</div>}

      <div className="search-section">
        <form onSubmit={handleSearchByHash} className="search-form">
          <input
            type="text"
            placeholder="Search by record hash..."
            value={selectedHash}
            onChange={(e) => setSelectedHash(e.target.value)}
          />
          <button type="submit" className="btn-primary">
            Search
          </button>
        </form>
      </div>

      <div className="records-section">
        <h3>Medical Records</h3>
        {records.length === 0 ? (
          <p>No records found</p>
        ) : (
          <table className="records-table">
            <thead>
              <tr>
                <th>Patient ID</th>
                <th>Hospital ID</th>
                <th>Type</th>
                <th>Hash</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {records.map((record, idx) => (
                <tr key={idx}>
                  <td>{record.HealthID || record.health_id}</td>
                  <td>{record.HospitalID || record.hospital_id}</td>
                  <td>{record.record_type || record.RecordType}</td>
                  <td>
                    <code>{(record.record_hash || record.RecordHash)?.substring(0, 12)}...</code>
                  </td>
                  <td>{new Date(record.timestamp).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
