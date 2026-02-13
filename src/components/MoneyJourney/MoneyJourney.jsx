import { useState } from 'react';
import { useForm } from 'react-hook-form';
import AccumulationForm from './AccumulationForm';
import WithdrawalForm from './WithdrawalForm';
import JourneyResultsDisplay from './JourneyResultsDisplay';
import JourneyChart from './JourneyChart';
import { calculateMoneyJourney } from '../../services/api';
import { parseInputValue } from '../../utils/formatters';
import './MoneyJourney.css';

const MoneyJourney = () => {
  const [results, setResults] = useState(null);
  const [inputs, setInputs] = useState(null);
  const [yearlyBreakdown, setYearlyBreakdown] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const {
    register,
    handleSubmit,
    control,
    watch,
    formState: { errors },
  } = useForm({
    defaultValues: {
      initial_investment: '0',
      monthly_investment: '5,000',
      accumulation_years: 25,
      accumulation_return_rate: 12,
      annual_step_up_rate: 0,
      step_up_cap: '',
      monthly_withdrawal: '50,000',
      withdrawal_years: 20,
      withdrawal_return_rate: 8,
      withdrawal_step_up_rate: 0,
      withdrawal_step_up_cap: '',
    },
  });

  const accumulationReturnRate = watch('accumulation_return_rate');

  const onSubmit = async (data) => {
    setIsLoading(true);
    setError(null);

    const payload = {
      initial_investment: parseInputValue(data.initial_investment),
      monthly_investment: parseInputValue(data.monthly_investment),
      accumulation_years: parseInt(data.accumulation_years),
      accumulation_return_rate: parseFloat(data.accumulation_return_rate),
      annual_step_up_rate: parseFloat(data.annual_step_up_rate) || 0,
      monthly_withdrawal: parseInputValue(data.monthly_withdrawal),
      withdrawal_years: parseInt(data.withdrawal_years),
      withdrawal_return_rate: parseFloat(data.withdrawal_return_rate),
      withdrawal_step_up_rate: parseFloat(data.withdrawal_step_up_rate) || 0,
    };

    const capValue = parseInputValue(data.step_up_cap);
    if (capValue > 0) {
      payload.step_up_cap = capValue;
    }
    const wCapValue = parseInputValue(data.withdrawal_step_up_cap);
    if (wCapValue > 0) {
      payload.withdrawal_step_up_cap = wCapValue;
    }

    try {
      const response = await calculateMoneyJourney(payload);
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
    <div className="money-journey">
      <div className="calculator-container">
        <form onSubmit={handleSubmit(onSubmit)} className="journey-form">
          <h2>Money Journey</h2>
          <p className="form-description">
            Plan your full financial lifecycle — accumulate wealth, then withdraw in retirement.
          </p>

          <AccumulationForm register={register} control={control} errors={errors} />
          <WithdrawalForm
            register={register}
            control={control}
            errors={errors}
            accumulationReturnRate={accumulationReturnRate}
          />

          <button type="submit" disabled={isLoading} className="calculate-button">
            {isLoading ? 'Calculating...' : 'Calculate Journey'}
          </button>
        </form>

        {error && (
          <div className="error-box">
            <strong>Error:</strong> {error}
          </div>
        )}

        {results && inputs && (
          <>
            <JourneyResultsDisplay results={results} inputs={inputs} />
            <JourneyChart yearlyBreakdown={yearlyBreakdown} inputs={inputs} />
          </>
        )}
      </div>
    </div>
  );
};

export default MoneyJourney;
