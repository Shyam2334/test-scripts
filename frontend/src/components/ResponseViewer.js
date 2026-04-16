import React from 'react';
import { formatJsonResponse, containsHtml, cleanResponseBody } from '../utils/responseFormatter';
import './ResponseViewer.css';

/**
 * Component for displaying API responses with proper formatting
 */
const ResponseViewer = ({ response, className = '' }) => {
    if (!response) {
        return (
            <pre className={`response-viewer response-body ${className}`}>
                No response data
            </pre>
        );
    }

    let displayContent;
    
    // Check if response needs cleaning
    if (typeof response === 'string' && containsHtml(response)) {
        displayContent = cleanResponseBody(response);
    } else {
        displayContent = formatJsonResponse(response);
    }

    return (
        <pre className={`response-viewer response-body ${className}`}>
            {displayContent}
        </pre>
    );
};

export default ResponseViewer;