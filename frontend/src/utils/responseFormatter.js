/**
 * Utility functions for formatting API responses
 */

/**
 * Clean response text from unwanted HTML and styling
 * @param {string} responseText - The response text that may contain HTML
 * @returns {string} - Cleaned response text
 */
export const cleanResponseBody = (responseText) => {
    if (typeof responseText !== 'string') {
        return responseText;
    }
    
    // Remove all HTML tags and their content
    let cleaned = responseText
        .replace(/<span[^>]*>/g, '')
        .replace(/<\/span>/g, '')
        .replace(/<div[^>]*>/g, '')
        .replace(/<\/div>/g, '')
        .replace(/style="[^"]*"/g, '')
        .replace(/class="[^"]*"/g, '');
    
    // Remove specific patterns that might be debug markers
    cleaned = cleaned
        .replace(/\b\d+\.\s*/g, '') // Remove numbered lists like "1. ", "2. "
        .replace(/^\s*\d+\s*$/gm, ''); // Remove standalone numbers on lines
    
    return cleaned.trim();
};

/**
 * Format JSON response for display
 * @param {any} response - The response data (object, array, or string)
 * @returns {string} - Formatted JSON string
 */
export const formatJsonResponse = (response) => {
    if (typeof response === 'string') {
        try {
            // Try to parse if it's a JSON string
            const parsed = JSON.parse(response);
            return JSON.stringify(parsed, null, 2);
        } catch (e) {
            // If not valid JSON, clean and return
            return cleanResponseBody(response);
        }
    }
    
    // If it's already an object/array, stringify it
    return JSON.stringify(response, null, 2);
};

/**
 * Check if a string contains HTML
 * @param {string} str - String to check
 * @returns {boolean} - True if contains HTML tags
 */
export const containsHtml = (str) => {
    if (typeof str !== 'string') return false;
    return /<[^>]*>/.test(str);
};

/**
 * Extract text content from HTML string
 * @param {string} html - HTML string
 * @returns {string} - Plain text content
 */
export const extractTextFromHtml = (html) => {
    if (typeof html !== 'string') return html;
    
    // Create a temporary element to parse HTML
    const temp = document.createElement('div');
    temp.innerHTML = html;
    
    // Get text content and clean up
    return temp.textContent || temp.innerText || '';
};