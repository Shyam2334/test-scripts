import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
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
      <div className="App">
        <div className="loading">Loading endpoints...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="App">
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
    </div>
  );
}

export default App;