import axios from 'axios';

// Determine API base URL based on environment
const API_BASE_URL = import.meta.env.PROD
  ? '/api'  // Production (Vercel)
  : 'http://localhost:8000/api';  // Local development

/**
 * Calculate SIP returns
 * @param {Object} data - Calculation parameters
 * @param {number} data.monthly_investment - Monthly investment amount
 * @param {number} data.time_period_years - Investment period in years
 * @param {number} data.annual_return_rate - Expected annual return rate (%)
 * @returns {Promise<Object>} Calculation results
 */
export const calculateSIP = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/calculate-sip`, data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.message || 'Calculation failed');
    } else if (error.request) {
      // Request made but no response
      throw new Error('Unable to connect to server. Please check if the backend is running.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred');
    }
  }
};
