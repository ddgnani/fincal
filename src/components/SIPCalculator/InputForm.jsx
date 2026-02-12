import { useForm } from 'react-hook-form';
import './InputForm.css';

const InputForm = ({ onCalculate, isLoading }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      monthly_investment: 5000,
      time_period_years: 10,
      annual_return_rate: 12,
    },
  });

  const onSubmit = (data) => {
    onCalculate({
      monthly_investment: parseFloat(data.monthly_investment),
      time_period_years: parseInt(data.time_period_years),
      annual_return_rate: parseFloat(data.annual_return_rate),
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="input-form">
      <h2>SIP Calculator</h2>
      <p className="form-description">
        Calculate the future value of your Systematic Investment Plan (SIP) with annual compounding.
      </p>

      <div className="form-group">
        <label htmlFor="monthly_investment">
          Monthly Investment Amount ($)
        </label>
        <input
          id="monthly_investment"
          type="number"
          step="0.01"
          {...register('monthly_investment', {
            required: 'Monthly investment is required',
            min: { value: 0.01, message: 'Must be greater than 0' },
          })}
          className={errors.monthly_investment ? 'error' : ''}
        />
        {errors.monthly_investment && (
          <span className="error-message">{errors.monthly_investment.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="time_period_years">
          Time Period (Years)
        </label>
        <input
          id="time_period_years"
          type="number"
          {...register('time_period_years', {
            required: 'Time period is required',
            min: { value: 1, message: 'Must be at least 1 year' },
            max: { value: 50, message: 'Must be 50 years or less' },
          })}
          className={errors.time_period_years ? 'error' : ''}
        />
        {errors.time_period_years && (
          <span className="error-message">{errors.time_period_years.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="annual_return_rate">
          Expected Annual Return Rate (%)
        </label>
        <input
          id="annual_return_rate"
          type="number"
          step="0.1"
          {...register('annual_return_rate', {
            required: 'Return rate is required',
            min: { value: 0, message: 'Must be 0 or greater' },
            max: { value: 100, message: 'Must be 100% or less' },
          })}
          className={errors.annual_return_rate ? 'error' : ''}
        />
        {errors.annual_return_rate && (
          <span className="error-message">{errors.annual_return_rate.message}</span>
        )}
      </div>

      <button type="submit" disabled={isLoading} className="calculate-button">
        {isLoading ? 'Calculating...' : 'Calculate'}
      </button>
    </form>
  );
};

export default InputForm;
