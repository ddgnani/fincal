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

/**
 * Format a raw input value with comma separators for display in money fields.
 * Strips non-numeric chars (except decimal point), adds commas, preserves decimal as typed.
 * @param {string} value - Raw input string
 * @returns {string} Formatted string (e.g., "12,345.67")
 */
export const formatInputValue = (value) => {
  // Strip everything except digits and decimal point
  let cleaned = value.replace(/[^0-9.]/g, '');

  // Only allow one decimal point
  const parts = cleaned.split('.');
  if (parts.length > 2) {
    cleaned = parts[0] + '.' + parts.slice(1).join('');
  }

  // Add comma separators to integer part
  const [intPart, decPart] = cleaned.split('.');
  const withCommas = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

  return decPart !== undefined ? `${withCommas}.${decPart}` : withCommas;
};

/**
 * Parse a formatted input value back to a number.
 * Strips commas and returns a float.
 * @param {string} value - Formatted input string (e.g., "12,345.67")
 * @returns {number} Parsed number (e.g., 12345.67)
 */
export const parseInputValue = (value) => {
  const num = parseFloat(String(value).replace(/,/g, ''));
  return isNaN(num) ? 0 : num;
};
