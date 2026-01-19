import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { authApi } from '../services/api';
import { validatePassword, getPasswordRequirements } from '../utils/passwordValidator';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const [formData, setFormData] = useState({
    email: '',
    token: '',
    newPassword: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');
    if (token) {
      setFormData((prev) => ({ ...prev, token }));
    }
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!formData.email) {
      setError('Email is required');
      return;
    }

    const validation = validatePassword(formData.newPassword);
    if (!validation.isValid) {
      setError(validation.errors.join(', '));
      return;
    }

    try {
      const response = await authApi.resetPassword(formData);
      setSuccess(response.message || 'Password reset successfully!');
      setFormData({ email: '', token: '', newPassword: '' });
    } catch (err: any) {
      setError(err.response?.data?.error || 'Password reset failed');
    }
  };

  return (
    <div className="card">
      <h2>Reset Password</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
          />
          <small>Enter your account email address</small>
        </div>
        <div className="form-group">
          <label>Temporary Password / Reset Token:</label>
          <input
            type="text"
            value={formData.token}
            onChange={(e) => setFormData({ ...formData, token: e.target.value })}
            required
          />
          <small>Enter the temporary password you received via email</small>
        </div>
        <div className="form-group">
          <label>New Password:</label>
          <input
            type="password"
            value={formData.newPassword}
            onChange={(e) => setFormData({ ...formData, newPassword: e.target.value })}
            required
          />
          <small>{getPasswordRequirements()}</small>
        </div>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        <button type="submit" className="btn btn-primary">Reset Password</button>
      </form>
    </div>
  );
};

export default ResetPassword;
