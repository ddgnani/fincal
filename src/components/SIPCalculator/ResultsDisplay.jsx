import { formatCurrency, formatPercentage } from '../../utils/formatters';
import './ResultsDisplay.css';

const ResultsDisplay = ({ results, inputs }) => {
  if (!results) return null;

  const { future_value, total_invested, total_returns, returns_percentage } = results;
  const { time_period_years, annual_return_rate } = inputs;

  return (
    <div className="results-display">
      <div className="results-header">
        <h2>Your Investment Results</h2>
        <p className="primary-message">
          In <strong>{time_period_years} years</strong>, you will have{' '}
          <strong className="highlight">{formatCurrency(future_value)}</strong>
        </p>
      </div>

      <div className="results-grid">
        <div className="result-card">
          <div className="result-label">Total Investment</div>
          <div className="result-value">{formatCurrency(total_invested)}</div>
        </div>

        <div className="result-card">
          <div className="result-label">Future Value</div>
          <div className="result-value highlight">{formatCurrency(future_value)}</div>
        </div>

        <div className="result-card">
          <div className="result-label">Total Returns</div>
          <div className="result-value success">{formatCurrency(total_returns)}</div>
        </div>

        <div className="result-card">
          <div className="result-label">Returns Percentage</div>
          <div className="result-value success">{formatPercentage(returns_percentage)}</div>
        </div>
      </div>

      <div className="results-note">
        <p>
          <strong>Compounding:</strong> Annual &nbsp;|&nbsp;
          <strong>Return Rate:</strong> {annual_return_rate}% per year
        </p>
      </div>
    </div>
  );
};

export default ResultsDisplay;
