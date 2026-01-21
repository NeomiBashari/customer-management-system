import { useState, useEffect } from 'react';
import { customerApi } from '../services/api';

interface Customer {
  id: number;
  firstname: string;
  lastname: string;
  email: string;
}

const CustomerManagementVulnerable = () => {
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    email: '',
  });
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [newCustomer, setNewCustomer] = useState<Customer | null>(null);

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      const data = await customerApi.getAll();
      setCustomers(data);
    } catch (err: any) {
      setError('Failed to load customers');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const response = await customerApi.create(formData);
      setSuccess('Customer created successfully!');
      
      // Store the response/form data to show the vulnerable display
      setNewCustomer({
        id: response.res_id || 0,
        firstname: formData.firstname,
        lastname: formData.lastname,
        email: formData.email
      });

      setFormData({
        firstname: '',
        lastname: '',
        email: '',
      });
      loadCustomers();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create customer');
    }
  };

  return (
    <div>
      <div className="card" style={{ border: '2px solid red' }}>
        <h2 style={{ color: 'red' }}>Add New Customer (VULNERABLE - XSS)</h2>
        <p style={{ color: 'red', fontWeight: 'bold' }}>
          WARNING: Unvalidated Mode. This page renders HTML directly.
          <br />
          Try entering: <code>&lt;img src=x onerror=alert('XSS')&gt;</code> in the First Name field.
        </p>
        <form onSubmit={handleSubmit} noValidate>
          <div className="form-group">
            <label>First Name:</label>
            <input
              type="text"
              value={formData.firstname}
              onChange={(e) => setFormData({ ...formData, firstname: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Last Name:</label>
            <input
              type="text"
              value={formData.lastname}
              onChange={(e) => setFormData({ ...formData, lastname: e.target.value })}
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
          {error && <div className="error">{error}</div>}
          {success && <div className="success">{success}</div>}
          
          {newCustomer && (
            <div className="success">
              <strong>New Customer Added: </strong>
              <span dangerouslySetInnerHTML={{ __html: newCustomer.firstname }} />{' '}
              <span dangerouslySetInnerHTML={{ __html: newCustomer.lastname }} />
            </div>
          )}
          
          <button type="submit" className="btn btn-primary" style={{ backgroundColor: '#dc3545' }}>Add Customer (Unvalidated)</button>
        </form>
      </div>

      <div className="card">
        <h2>All Customers (VULNERABLE VIEW)</h2>
        {customers.length === 0 ? (
          <p>No customers found</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd' }}>
                <th style={{ padding: '8px', textAlign: 'left' }}>ID</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>First Name (Unsafe)</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>Last Name (Unsafe)</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>Email</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.id} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '8px' }}>{customer.id}</td>
                  <td style={{ padding: '8px' }} dangerouslySetInnerHTML={{ __html: customer.firstname }} />
                  <td style={{ padding: '8px' }} dangerouslySetInnerHTML={{ __html: customer.lastname }} />
                  <td style={{ padding: '8px' }}>{customer.email}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default CustomerManagementVulnerable;
