import React from 'react';
import './Header.css';
import wellsFargoLogo from '../assets/images/wells-fargo-logo.svg';
import { useTheme } from '../context/ThemeContext';

function Header() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <img src={wellsFargoLogo} alt="Wells Fargo Logo" className="header-logo" />
          <h1 className="header-title">API Explorer</h1>
        </div>
        <button
          className="theme-toggle-button"
          onClick={toggleTheme}
          aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          {theme === 'light' ? (
            <>
              <span className="theme-icon">🌙</span>
              <span className="theme-text">Dark Mode</span>
            </>
          ) : (
            <>
              <span className="theme-icon">☀️</span>
              <span className="theme-text">Light Mode</span>
            </>
          )}
        </button>
      </div>
    </header>
  );
}

export default Header;