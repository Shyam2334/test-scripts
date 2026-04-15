import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';
import wellsFargoLogo from '../assets/images/wells-fargo-logo.svg';

const Header = () => {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="wf-header">
      <div className="wf-header-container">
        <div className="wf-header-brand">
          <Link to="/" className="wf-header-logo-link">
            <img 
              src={wellsFargoLogo} 
              alt="Wells Fargo" 
              className="wf-header-logo"
            />
          </Link>
          <div className="wf-header-title">
            <h1>User Management System</h1>
            <p className="wf-header-subtitle">Secure. Simple. Reliable.</p>
          </div>
        </div>
        
        <nav className="wf-header-nav">
          <Link 
            to="/" 
            className={`wf-header-nav-link ${isActive('/') ? 'active' : ''}`}
          >
            Users
          </Link>
          <Link 
            to="/swagger" 
            className={`wf-header-nav-link ${isActive('/swagger') ? 'active' : ''}`}
          >
            API Documentation
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;