import React, { useEffect } from 'react';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';
import '../styles/swagger-theme-overrides.css';
import './SwaggerPage.css';

const SwaggerPage = () => {
  useEffect(() => {
    // Apply Wells Fargo theme to Swagger UI after it loads
    const applyTheme = () => {
      const swaggerContainer = document.querySelector('.swagger-ui');
      if (swaggerContainer) {
        swaggerContainer.classList.add('wf-swagger-theme');
      }
    };
    
    // Apply theme after a short delay to ensure Swagger UI is loaded
    const timer = setTimeout(applyTheme, 100);
    
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="swagger-page-container">
      <div className="swagger-page-header">
        <h1>API Documentation</h1>
        <p>Explore and test the User Management API endpoints</p>
      </div>
      <div className="swagger-wrapper">
        <SwaggerUI url="/openapi.json" />
      </div>
    </div>
  );
};

export default SwaggerPage;