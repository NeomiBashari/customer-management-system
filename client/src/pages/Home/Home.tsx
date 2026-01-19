import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useApiMode } from '../../contexts/ApiModeContext';
import CustomerManagement from '../CustomerManagement';
import ChangePassword from '../ChangePassword';
import './Home.css';

const Home = () => {
  const [activeTab, setActiveTab] = useState('customers');
  const { user, logout } = useAuth();
  const { isValidated, toggleApiMode } = useApiMode();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="home-container">
      <div className="home-header">
        <div className="header-content">
          <h1>Communication_LTD</h1>
          <div className="user-info">
            <span>Welcome, {user?.username}</span>
            <button
              onClick={toggleApiMode}
              className={`mode-toggle-button ${isValidated ? 'validated' : 'unvalidated'}`}
              title={`Currently using ${isValidated ? 'validated' : 'unvalidated'} routes. Click to toggle.`}
            >
              {isValidated ? '🔒 Validated' : '🔓 Unvalidated'}
            </button>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="tabs-container">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'customers' ? 'active' : ''}`}
            onClick={() => setActiveTab('customers')}
          >
            Customer Management
          </button>
          <button
            className={`tab ${activeTab === 'change-password' ? 'active' : ''}`}
            onClick={() => setActiveTab('change-password')}
          >
            Change Password
          </button>
        </div>
      </div>

      <div className="tab-content">
        {activeTab === 'customers' && <CustomerManagement />}
        {activeTab === 'change-password' && <ChangePassword />}
      </div>
    </div>
  );
};

export default Home;


