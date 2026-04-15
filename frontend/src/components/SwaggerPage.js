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

  // Utility function to format JSON
  const formatJSON = (jsonString) => {
    try {
      const parsed = JSON.parse(jsonString);
      return JSON.stringify(parsed, null, 2);
    } catch (e) {
      console.error("Error parsing JSON:", e);
      return jsonString;
    }
  };

  // Utility function to apply syntax highlighting
  const syntaxHighlight = (json) => {
    if (typeof json !== 'string') {
      json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
      (match) => {
        let cls = 'json-number';
        if (/^"/.test(match)) {
          if (/:$/.test(match)) {
            cls = 'json-key';
          } else {
            cls = 'json-string';
          }
        } else if (/true|false/.test(match)) {
          cls = 'json-boolean';
        } else if (/null/.test(match)) {
          cls = 'json-null';
        }
        return `<span class="${cls}">${match}</span>`;
      });
  };

  // Copy to clipboard function
  const copyToClipboard = (text) => {
    const prettyPrinted = formatJSON(text);
    navigator.clipboard.writeText(prettyPrinted)
      .then(() => alert('Response copied to clipboard!'))
      .catch(err => console.error('Failed to copy: ', err));
  };

  // Toggle fullscreen function
  const toggleFullscreen = (elementId) => {
    const elem = document.getElementById(elementId);
    if (!document.fullscreenElement) {
      elem.requestFullscreen().catch(err => {
        alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
      });
    } else {
      document.exitFullscreen();
    }
  };

  // Custom response interceptor for Swagger UI
  const responseInterceptor = (response) => {
    // Add custom buttons to response containers
    setTimeout(() => {
      const responseContainers = document.querySelectorAll('.response-col_description pre.microlight');
      responseContainers.forEach((container, index) => {
        if (!container.parentElement.querySelector('.response-header')) {
          const responseText = container.textContent;
          const containerId = `response-container-${index}`;
          container.id = containerId;
          
          // Create header with buttons
          const header = document.createElement('div');
          header.className = 'response-header';
          header.innerHTML = `
            <button class="copy-btn" onclick="window.copyResponseToClipboard('${btoa(responseText)}')">
              Copy Response
            </button>
            <button class="expand-btn" onclick="window.toggleResponseFullscreen('${containerId}')">
              Expand
            </button>
          `;
          
          container.parentElement.insertBefore(header, container);
          
          // Apply syntax highlighting if it's JSON
          try {
            const formatted = formatJSON(responseText);
            const highlighted = syntaxHighlight(formatted);
            container.innerHTML = highlighted;
            container.classList.add('response-container');
          } catch (e) {
            // Not JSON, leave as is
            container.classList.add('response-container');
          }
        }
      });
    }, 100);
    
    return response;
  };

  // Make functions available globally for inline onclick handlers
  useEffect(() => {
    window.copyResponseToClipboard = (encodedText) => {
      const text = atob(encodedText);
      copyToClipboard(text);
    };
    
    window.toggleResponseFullscreen = (elementId) => {
      toggleFullscreen(elementId);
    };
    
    return () => {
      delete window.copyResponseToClipboard;
      delete window.toggleResponseFullscreen;
    };
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
        responseInterceptor={responseInterceptor}
      />
    </div>
  );
};

export default SwaggerPage;