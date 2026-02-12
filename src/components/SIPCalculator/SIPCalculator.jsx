import { useState } from 'react';
import InputForm from './InputForm';
import ResultsDisplay from './ResultsDisplay';
import GrowthChart from './GrowthChart';
import { calculateSIP } from '../../services/api';
import './SIPCalculator.css';

const SIPCalculator = () => {
  const [results, setResults] = useState(null);
  const [inputs, setInputs] = useState(null);
  const [yearlyBreakdown, setYearlyBreakdown] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCalculate = async (data) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await calculateSIP(data);
      setResults(response.results);
      setInputs(response.inputs);
      setYearlyBreakdown(response.yearly_breakdown || []);
    } catch (err) {
      setError(err.message);
      setResults(null);
      setInputs(null);
      setYearlyBreakdown([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="sip-calculator">
      <div className="calculator-container">
        <header className="calculator-header">
          <h1>Investment Growth Calculator</h1>
          <p className="subtitle">
            Plan your financial future with our SIP calculator
          </p>
        </header>

        <InputForm onCalculate={handleCalculate} isLoading={isLoading} />

        {error && (
          <div className="error-box">
            <strong>Error:</strong> {error}
          </div>
        )}

        {results && inputs && (
          <>
            <ResultsDisplay results={results} inputs={inputs} />
            <GrowthChart
              yearlyBreakdown={yearlyBreakdown}
              inputs={inputs}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default SIPCalculator;
