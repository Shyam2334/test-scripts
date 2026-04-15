import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import SwaggerPage from './components/SwaggerPage';
import './App.css';

function EndpointsList() {
  const [endpoints, setEndpoints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEndpoints = async () => {
      try {
        const response = await fetch('/api/v1/endpoints');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setEndpoints(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchEndpoints();
  }, []);

  if (loading) {
    return (
      <div className="loading">Loading endpoints...</div>
    );
  }

  if (error) {
    return (
      <div className="error">Error: {error}</div>
    );
  }

  return (
    <>
      <header className="App-header">
        <h1>API Endpoints</h1>
        <p className="subtitle">Available endpoints in this application</p>
      </header>
      <main className="App-main">
        {endpoints.length === 0 ? (
          <p className="no-endpoints">No endpoints found.</p>
        ) : (
          <div className="endpoints-container">
            {endpoints.map((endpoint, index) => (
              <div key={index} className="endpoint-card">
                <div className="endpoint-path">
                  <code>{endpoint.path}</code>
                </div>
                <div className="endpoint-details">
                  <div className="methods">
                    {endpoint.methods.map((method, idx) => (
                      <span key={idx} className={`method method-${method.toLowerCase()}`}>
                        {method}
                      </span>
                    ))}
                  </div>
                  {endpoint.tags && endpoint.tags.length > 0 && (
                    <div className="tags">
                      {endpoint.tags.map((tag, idx) => (
                        <span key={idx} className="tag">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                  <div className="endpoint-name">
                    {endpoint.name}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </>
  );
}

function Navigation() {
  const location = useLocation();
  
  return (
    <nav className="app-navigation">
      <ul>
        <li className={location.pathname === '/' ? 'active' : ''}>
          <Link to="/">Endpoints List</Link>
        </li>
        <li className={location.pathname === '/api-docs' ? 'active' : ''}>
          <Link to="/api-docs">Interactive API Docs</Link>
        </li>
      </ul>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/" element={<EndpointsList />} />
          <Route path="/api-docs" element={<SwaggerPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;