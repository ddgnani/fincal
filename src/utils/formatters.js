/**
 * Format number as currency with commas and dollar sign
 * @param {number} amount - The amount to format
 * @returns {string} Formatted currency string (e.g., "$1,234,567.89")
 */
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
};

/**
 * Format number with commas (no currency symbol)
 * @param {number} num - The number to format
 * @returns {string} Formatted number string (e.g., "1,234,567.89")
 */
export const formatNumber = (num) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num);
};

/**
 * Format percentage
 * @param {number} percentage - The percentage to format
 * @returns {string} Formatted percentage string (e.g., "12.50%")
 */
export const formatPercentage = (percentage) => {
  return `${percentage.toFixed(2)}%`;
};
