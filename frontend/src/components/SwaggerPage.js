import React from 'react';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';
import './SwaggerPage.css';

const SwaggerPage = () => {
  return (
    <div className="swagger-page">
      <div className="swagger-header">
        <h2 className="swagger-title">API Documentation</h2>
        <p className="swagger-description">
          A simple FastAPI microservice with a health check endpoint.
        </p>
      </div>
      <div className="swagger-ui-wrapper">
        <SwaggerUI url="/openapi.json" />
      </div>
    </div>
  );
};

export default SwaggerPage;