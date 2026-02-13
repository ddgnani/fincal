import { formatCurrency } from '../../utils/formatters';
import './JourneyResultsDisplay.css';

const JourneyResultsDisplay = ({ results, inputs }) => {
  if (!results) return null;

  const {
    corpus_at_retirement,
    total_contributions,
    total_withdrawals,
    final_balance,
    depleted,
    depletion_year,
  } = results;

  return (
    <div className="journey-results-display">
      <div className="results-header">
        <h2>Your Money Journey Results</h2>
      </div>

      {depleted && (
        <div className="depletion-warning">
          <strong>Warning:</strong> Your corpus was fully depleted
          {depletion_year && ` in year ${depletion_year}`}. Consider reducing withdrawals
          or increasing your accumulation period.
        </div>
      )}

      <div className="results-grid">
        <div className="result-card">
          <div className="result-label">Corpus at Retirement</div>
          <div className="result-value highlight">{formatCurrency(corpus_at_retirement)}</div>
        </div>

        <div className="result-card">
          <div className="result-label">Total Contributions</div>
          <div className="result-value">{formatCurrency(total_contributions)}</div>
        </div>

        <div className="result-card">
          <div className="result-label">Total Withdrawals</div>
          <div className="result-value">{formatCurrency(total_withdrawals)}</div>
        </div>

        <div className="result-card">
          <div className="result-label">Final Balance</div>
          <div className={`result-value ${final_balance > 0 ? 'success' : 'depleted'}`}>
            {formatCurrency(final_balance)}
          </div>
        </div>
      </div>

      <div className="results-note">
        <p>
          <strong>Accumulation:</strong> {inputs.accumulation_years} years at {inputs.accumulation_return_rate}% &nbsp;|&nbsp;
          <strong>Withdrawal:</strong> {inputs.withdrawal_years} years at {inputs.withdrawal_return_rate}%
        </p>
      </div>
    </div>
  );
};

export default JourneyResultsDisplay;
