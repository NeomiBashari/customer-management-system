import { useState } from 'react';
import { authApi } from '../services/api';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const response = await authApi.forgotPassword({ email });
      setSuccess(response.message || 'Password reset email sent! Check your email for the reset token.');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to send reset email');
    }
  };

  return (
    <div className="card">
      <h2>Forgot Password</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        <button type="submit" className="btn btn-primary">Send Reset Token</button>
      </form>
    </div>
  );
};

export default ForgotPassword;

