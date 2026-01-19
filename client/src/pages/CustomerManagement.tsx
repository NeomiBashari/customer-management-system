import { useState, useEffect } from 'react';
import { customerApi } from '../services/api';

interface Customer {
  id: number;
  firstname: string;
  lastname: string;
  email: string;
  name?: string;
}

const CustomerManagement = () => {
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    email: '',
  });
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [newCustomerName, setNewCustomerName] = useState('');

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
      const customerName = `${response.firstname || formData.firstname} ${response.lastname || formData.lastname}`;
      setSuccess(`Customer "${customerName}" created successfully!`);
      setNewCustomerName(customerName);
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
      <div className="card">
        <h2>Add New Customer</h2>
        <form onSubmit={handleSubmit}>
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
          {newCustomerName && (
            <div className="success">
              <strong>New Customer Name: {newCustomerName}</strong>
            </div>
          )}
          <button type="submit" className="btn btn-primary">Add Customer</button>
        </form>
      </div>

      <div className="card">
        <h2>All Customers</h2>
        {customers.length === 0 ? (
          <p>No customers found</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd' }}>
                <th style={{ padding: '8px', textAlign: 'left' }}>ID</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>First Name</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>Last Name</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>Email</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.id} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '8px' }}>{customer.id}</td>
                  <td style={{ padding: '8px' }}>{customer.firstname}</td>
                  <td style={{ padding: '8px' }}>{customer.lastname}</td>
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

export default CustomerManagement;

