import { useState, useEffect } from 'react';
import { customerApi } from '../services/api';

interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string;
  address: string;
  sector: string;
  packageId: number;
}

const CustomerManagementVulnerable = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    sector: '',
    packageId: 1,
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
      setSuccess(`Customer "${response.customer.name}" created successfully!`);
      setNewCustomerName(response.customer.name);
      setFormData({
        name: '',
        email: '',
        phone: '',
        address: '',
        sector: '',
        packageId: 1,
      });
      loadCustomers();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create customer');
    }
  };

  return (
    <div>
      <div className="card">
        <h2>Add New Customer (VULNERABLE - XSS)</h2>
        <p style={{ color: 'red', fontWeight: 'bold' }}>
          WARNING: This page is vulnerable to XSS attacks. Try entering: &lt;script&gt;alert('XSS')&lt;/script&gt; in the name field
        </p>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name:</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
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
            <label>Phone:</label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Address:</label>
            <textarea
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Sector:</label>
            <input
              type="text"
              value={formData.sector}
              onChange={(e) => setFormData({ ...formData, sector: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Package ID:</label>
            <select
              value={formData.packageId}
              onChange={(e) => setFormData({ ...formData, packageId: parseInt(e.target.value) })}
              required
            >
              <option value={1}>1 - Basic</option>
              <option value={2}>2 - Standard</option>
              <option value={3}>3 - Premium</option>
              <option value={4}>4 - Ultra</option>
            </select>
          </div>
          {error && <div className="error">{error}</div>}
          {success && <div className="success">{success}</div>}
          {newCustomerName && (
            <div className="success">
              <strong>New Customer Name: <span dangerouslySetInnerHTML={{ __html: newCustomerName }} /></strong>
            </div>
          )}
          <button type="submit" className="btn btn-primary">Add Customer</button>
        </form>
      </div>

      <div className="card">
        <h2>All Customers (VULNERABLE - XSS)</h2>
        {customers.length === 0 ? (
          <p>No customers found</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd' }}>
                <th style={{ padding: '8px', textAlign: 'left' }}>ID</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>Name</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>Email</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>Phone</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>Sector</th>
                <th style={{ padding: '8px', textAlign: 'left' }}>Package</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.id} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '8px' }}>{customer.id}</td>
                  <td style={{ padding: '8px' }} dangerouslySetInnerHTML={{ __html: customer.name }} />
                  <td style={{ padding: '8px' }}>{customer.email}</td>
                  <td style={{ padding: '8px' }}>{customer.phone}</td>
                  <td style={{ padding: '8px' }}>{customer.sector}</td>
                  <td style={{ padding: '8px' }}>{customer.packageId}</td>
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

