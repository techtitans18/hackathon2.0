import { useEffect, useState } from 'react';
import { adminAPI, hospitalAPI } from '../services/api';
import UserManagement from '../components/UserManagement';
import BlockchainViewer from '../components/BlockchainViewer';
import AddHospital from '../components/AddHospital';
import UpdateHospital from '../components/UpdateHospital';

export default function AdminDashboard({ user }) {
  const [users, setUsers] = useState([]);
  const [blockchain, setBlockchain] = useState(null);
  const [activeTab, setActiveTab] = useState('users');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    setLoading(true);
    try {
      const [usersRes, blockchainRes] = await Promise.all([
        adminAPI.listUsers(),
        hospitalAPI.getBlockchain().catch(() => null),
      ]);

      setUsers(usersRes.data.users || []);
      if (blockchainRes?.data) {
        setBlockchain(blockchainRes.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load admin data');
      console.error('Error loading admin data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUserUpdated = () => {
    loadAdminData();
  };

  const handleHospitalAdded = (newHospital) => {
    console.log('Hospital added:', newHospital);
  };

  const handleHospitalUpdated = (updatedHospital) => {
    console.log('Hospital updated:', updatedHospital);
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
      <h2>Admin Dashboard</h2>
      {error && <div className="error-message">{error}</div>}

      <div className="tab-navigation">
        <button
          className={`tab-btn ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          User Management
        </button>
        <button
          className={`tab-btn ${activeTab === 'hospitals' ? 'active' : ''}`}
          onClick={() => setActiveTab('hospitals')}
        >
          Hospital Management
        </button>
        <button
          className={`tab-btn ${activeTab === 'blockchain' ? 'active' : ''}`}
          onClick={() => setActiveTab('blockchain')}
        >
          Blockchain Viewer
        </button>
      </div>

      {activeTab === 'users' && (
        <UserManagement
          users={users}
          onUserUpdated={handleUserUpdated}
        />
      )}

      {activeTab === 'hospitals' && (
        <div className="hospital-management-section">
          <div className="hospital-forms-grid">
            <AddHospital onHospitalAdded={handleHospitalAdded} />
            <UpdateHospital onHospitalUpdated={handleHospitalUpdated} />
          </div>
        </div>
      )}

      {activeTab === 'blockchain' && blockchain && (
        <BlockchainViewer blockchain={blockchain} />
      )}
    </div>
  );
}
