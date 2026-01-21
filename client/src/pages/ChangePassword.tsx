import { useState } from 'react';
import { authApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { validatePassword, getPasswordRequirements } from '../utils/passwordValidator';
import { useApiMode } from '../contexts/ApiModeContext';

const ChangePassword = () => {
  const { user } = useAuth();
  const { isValidated } = useApiMode();
  const [formData, setFormData] = useState({
    currentPassword: '',
    newPassword: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!user) {
      setError('User not authenticated');
      return;
    }

    if (isValidated) {
      const validation = validatePassword(formData.newPassword);
      if (!validation.isValid) {
        setError(validation.errors.join(', '));
        return;
      }
    }

    try {
      await authApi.changePassword({
        userId: user.id,
        currentPassword: formData.currentPassword,
        newPassword: formData.newPassword,
      });
      setSuccess('Password changed successfully!');
      setFormData({ currentPassword: '', newPassword: '' });
    } catch (err: any) {
      setError(err.response?.data?.error || 'Password change failed');
    }
  };

  return (
    <div className="card">
      <h2>Change Password</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Current Password:</label>
          <input
            type="password"
            value={formData.currentPassword}
            onChange={(e) => setFormData({ ...formData, currentPassword: e.target.value })}
            required
          />
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
        <button type="submit" className="btn btn-primary">Change Password</button>
      </form>
    </div>
  );
};

export default ChangePassword;

