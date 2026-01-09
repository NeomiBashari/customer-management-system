import { Link } from 'react-router-dom';
import './Landing.css';

const Landing = () => {
  return (
    <div className="landing-container">
      <div className="landing-content">
        <h1>Welcome to Communication_LTD</h1>
        <p className="subtitle">Customer Management System</p>
        <div className="auth-options">
          <Link to="/login" className="auth-button login-button">
            Login
          </Link>
          <Link to="/register" className="auth-button register-button">
            Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Landing;

