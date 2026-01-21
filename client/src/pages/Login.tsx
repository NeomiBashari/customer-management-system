import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { useApiMode } from '../contexts/ApiModeContext';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const { login } = useAuth();
  const { isValidated, toggleApiMode } = useApiMode();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await authApi.login(formData);
      login(response.user);
      navigate('/home');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div className="auth-page">
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '1rem' }}>
          <button
              onClick={toggleApiMode}
              className={`mode-toggle-button ${isValidated ? 'validated' : 'unvalidated'}`}
              title={`Currently using ${isValidated ? 'validated' : 'unvalidated'} routes. Click to toggle.`}
            >
              {isValidated ? '🔒 Validated' : '🔓 Unvalidated'}
          </button>
        </div>
        <h2>Login to Communication_LTD</h2>
        <div className="mock-credentials">
          <strong>Valid Example Credentials:</strong>
          <div className="credential-item">
            <span>Email: <code>test@example.com</code></span>
            <span>Password: <code>TestPass123!@#</code></span>
          </div>
          <div className="credential-item">
            <span>Email: <code>user@demo.com</code></span>
            <span>Password: <code>MySecure1!Pass</code></span>
          </div>
          <small style={{ display: 'block', marginTop: '0.5rem', color: '#666' }}>
            Use credentials you registered with, or register a new account
          </small>
        </div>
        <form onSubmit={handleSubmit} noValidate={!isValidated}>
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
            />
          </div>
          {error && <div className="error">{error}</div>}
          <button type="submit" className="btn btn-primary">Login</button>
          <div className="auth-link">
            Don't have an account? <Link to="/register">Sign up</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;

