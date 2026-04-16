import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import { useTheme } from '../context/ThemeContext';
import wellsFargoLogo from '../assets/images/wells-fargo-logo.svg';

const Header = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <img 
            src={wellsFargoLogo} 
            alt="Wells Fargo" 
            className="header-logo"
          />
          <h1 className="header-title">User Management System</h1>
        </div>
        
        <nav className="header-nav">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/users" className="nav-link">Users</Link>
        </nav>
        
        <button 
          className="theme-toggle-button"
          onClick={toggleTheme}
          aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          <span className="theme-icon">
            {theme === 'light' ? '🌙' : '☀️'}
          </span>
          <span className="theme-text">
            {theme === 'light' ? 'Dark' : 'Light'} Mode
          </span>
        </button>
      </div>
    </header>
  );
};

export default Header;