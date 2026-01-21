import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authApi } from '../services/api';
import { validatePassword, getPasswordRequirements } from '../utils/passwordValidator';
import { useApiMode } from '../contexts/ApiModeContext';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { isValidated, toggleApiMode } = useApiMode();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const validation = validatePassword(formData.password);
    if (!validation.isValid) {
      setError(validation.errors.join(', '));
      return;
    }

    try {
      const response = await authApi.register(formData);
      setSuccess(`User ${response.user.username} registered successfully!`);
      setFormData({ username: '', email: '', password: '' });
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Registration failed');
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
        <h2>Register New User</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              required
            />
          </div>
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
            <small>{getPasswordRequirements()}</small>
          </div>
          {error && <div className="error">{error}</div>}
          {success && <div className="success">{success}</div>}
          <button type="submit" className="btn btn-primary">Register</button>
          <div className="auth-link">
            Already have an account? <Link to="/login">Login</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;

