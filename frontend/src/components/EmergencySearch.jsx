import { useState } from 'react';
import { emergencyAPI } from '../services/api';

export default function EmergencySearch({ onPatientFound }) {
  const [searchType, setSearchType] = useState('health_id');
  const [value, setValue] = useState('');
  const [name, setName] = useState('');
  const [dob, setDob] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const payload = {
        role: 'hospital',
        search_type: searchType,
        value: searchType !== 'name_dob' ? value : null,
        name: searchType === 'name_dob' ? name : null,
        dob: searchType === 'name_dob' ? dob : null,
      };

      const response = await emergencyAPI.searchPatient(payload);
      onPatientFound(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Patient not found');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="emergency-search-card">
      <h3>Search Patient</h3>
      <form onSubmit={handleSearch}>
        <div className="form-group">
          <label>Search By:</label>
          <select value={searchType} onChange={(e) => setSearchType(e.target.value)}>
            <option value="health_id">Health ID</option>
            <option value="phone">Phone Number</option>
            <option value="name_dob">Name + DOB</option>
          </select>
        </div>

        {searchType !== 'name_dob' ? (
          <div className="form-group">
            <label>{searchType === 'health_id' ? 'Health ID' : 'Phone Number'}:</label>
            <input
              type="text"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              required
            />
          </div>
        ) : (
          <>
            <div className="form-group">
              <label>Name:</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Date of Birth (YYYY-MM-DD):</label>
              <input
                type="date"
                value={dob}
                onChange={(e) => setDob(e.target.value)}
                required
              />
            </div>
          </>
        )}

        {error && <div className="error-message">{error}</div>}

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>
    </div>
  );
}
