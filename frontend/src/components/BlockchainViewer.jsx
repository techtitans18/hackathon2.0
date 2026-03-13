import { useState } from 'react';
import '../styles/blockchain-viewer.css';

export default function BlockchainViewer({ blockchain }) {
  const [searchHealthId, setSearchHealthId] = useState('');
  const [searchHospitalId, setSearchHospitalId] = useState('');
  const [selectedBlock, setSelectedBlock] = useState(null);

  if (!blockchain || !blockchain.chain) {
    return <div className="no-data">No blockchain data available</div>;
  }

  const chain = blockchain.chain || [];
  const integrity = blockchain.integrity || {};

  // Filter blocks
  const filteredBlocks = chain.filter(block => {
    const matchesHealth = !searchHealthId || 
      block.HealthID?.toLowerCase().includes(searchHealthId.toLowerCase());
    const matchesHospital = !searchHospitalId || 
      block.HospitalID?.toLowerCase().includes(searchHospitalId.toLowerCase());
    return matchesHealth && matchesHospital;
  });

  // Get patient statistics
  const getPatientStats = () => {
    const patients = {};
    chain.forEach(block => {
      if (block.HealthID && block.HealthID !== 'GENESIS') {
        if (!patients[block.HealthID]) {
          patients[block.HealthID] = { count: 0, hospitals: new Set() };
        }
        patients[block.HealthID].count++;
        patients[block.HealthID].hospitals.add(block.HospitalID);
      }
    });
    return patients;
  };

  const patientStats = getPatientStats();

  return (
    <div className="blockchain-viewer">
      <div className="blockchain-header">
        <h3>🔗 Blockchain Ledger</h3>
        <div className="blockchain-stats">
          <div className="stat-card">
            <span className="stat-value">{blockchain.length || chain.length}</span>
            <span className="stat-label">Total Blocks</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{Object.keys(patientStats).length}</span>
            <span className="stat-label">Unique Patients</span>
          </div>
          <div className="stat-card">
            <span className={`stat-value ${integrity.valid ? 'valid' : 'invalid'}`}>
              {integrity.valid ? '✓' : '✗'}
            </span>
            <span className="stat-label">Integrity</span>
          </div>
        </div>
      </div>

      {/* Search Filters */}
      <div className="blockchain-filters">
        <div className="filter-group">
          <label>🔍 Search by Health ID:</label>
          <input
            type="text"
            placeholder="Enter Health ID..."
            value={searchHealthId}
            onChange={(e) => setSearchHealthId(e.target.value)}
            className="filter-input"
          />
        </div>
        <div className="filter-group">
          <label>🏥 Search by Hospital ID:</label>
          <input
            type="text"
            placeholder="Enter Hospital ID..."
            value={searchHospitalId}
            onChange={(e) => setSearchHospitalId(e.target.value)}
            className="filter-input"
          />
        </div>
        {(searchHealthId || searchHospitalId) && (
          <button 
            className="clear-filters-btn"
            onClick={() => {
              setSearchHealthId('');
              setSearchHospitalId('');
            }}
          >
            Clear Filters
          </button>
        )}
      </div>

      {/* Patient Statistics */}
      {searchHealthId && patientStats[searchHealthId] && (
        <div className="patient-stats-card">
          <h4>📊 Patient Statistics for {searchHealthId}</h4>
          <p><strong>Total Records:</strong> {patientStats[searchHealthId].count}</p>
          <p><strong>Hospitals:</strong> {Array.from(patientStats[searchHealthId].hospitals).join(', ')}</p>
        </div>
      )}

      {/* Results Count */}
      <div className="results-info">
        Showing {filteredBlocks.length} of {chain.length} blocks
      </div>

      {/* Blockchain Chain */}
      <div className="blockchain-chain">
        {filteredBlocks.length === 0 ? (
          <div className="no-results">No blocks found matching your search criteria</div>
        ) : (
          filteredBlocks.map((block, idx) => (
            <div key={idx} className={`blockchain-block ${block.HealthID === 'GENESIS' ? 'genesis-block' : ''}`}>
              <div className="block-header">
                <span className="block-index">Block #{block.index}</span>
                <span className="block-type">{block.RecordType}</span>
                <button 
                  className="block-expand-btn"
                  onClick={() => setSelectedBlock(selectedBlock === idx ? null : idx)}
                >
                  {selectedBlock === idx ? '▼' : '▶'}
                </button>
              </div>

              <div className="block-content">
                <div className="block-row">
                  <span className="block-label">👤 Health ID:</span>
                  <span className="block-value">{block.HealthID}</span>
                </div>
                <div className="block-row">
                  <span className="block-label">🏥 Hospital ID:</span>
                  <span className="block-value">{block.HospitalID}</span>
                </div>
                <div className="block-row">
                  <span className="block-label">📄 Record Hash:</span>
                  <code className="block-hash">{block.RecordHash?.substring(0, 20)}...</code>
                </div>
                <div className="block-row">
                  <span className="block-label">🕐 Timestamp:</span>
                  <span className="block-value">{new Date(block.timestamp).toLocaleString()}</span>
                </div>

                {/* Expanded Details */}
                {selectedBlock === idx && (
                  <div className="block-expanded">
                    <div className="block-row">
                      <span className="block-label">🔐 Block Hash:</span>
                      <code className="block-hash-full">{block.hash}</code>
                    </div>
                    <div className="block-row">
                      <span className="block-label">⛓️ Previous Hash:</span>
                      <code className="block-hash-full">{block.previous_hash}</code>
                    </div>
                    <div className="block-row">
                      <span className="block-label">📋 Full Record Hash:</span>
                      <code className="block-hash-full">{block.RecordHash}</code>
                    </div>
                  </div>
                )}
              </div>

              {idx < filteredBlocks.length - 1 && <div className="block-connector">↓</div>}
            </div>
          ))
        )}
      </div>
    </div>
  );
}