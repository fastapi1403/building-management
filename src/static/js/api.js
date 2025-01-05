// API Integration
const API_BASE_URL = '/api/v1';

async function fetchData(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
