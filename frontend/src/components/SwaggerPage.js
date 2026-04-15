import React, { useEffect, useState } from 'react';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';
import '../styles/swagger-theme-overrides.css';

const SwaggerPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check if OpenAPI spec is available
    fetch('/openapi.json')
      .then(response => {
        if (!response.ok) {
          throw new Error('OpenAPI specification not found');
        }
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="swagger-container">
        <div className="loading">Loading API documentation...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="swagger-container">
        <div className="error">Error loading API documentation: {error}</div>
      </div>
    );
  }

  return (
    <div className="swagger-container">
      <header className="swagger-header">
        <h1>Interactive API Documentation</h1>
        <p className="subtitle">Test API endpoints directly from your browser</p>
      </header>
      <SwaggerUI 
        url="/openapi.json"
        docExpansion="list"
        defaultModelsExpandDepth={1}
        displayRequestDuration={true}
        filter={true}
        showExtensions={true}
        showCommonExtensions={true}
        tryItOutEnabled={true}
      />
    </div>
  );
};

export default SwaggerPage;