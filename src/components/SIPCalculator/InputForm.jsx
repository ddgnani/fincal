import { useForm, Controller } from 'react-hook-form';
import { formatInputValue, parseInputValue } from '../../utils/formatters';
import './InputForm.css';

const InputForm = ({ onCalculate, isLoading }) => {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm({
    defaultValues: {
      initial_investment: '0',
      monthly_investment: '5,000',
      time_period_years: 10,
      annual_return_rate: 12,
      annual_step_up_rate: 0,
      step_up_cap: '',
    },
  });

  const onSubmit = (data) => {
    const payload = {
      initial_investment: parseInputValue(data.initial_investment),
      monthly_investment: parseInputValue(data.monthly_investment),
      time_period_years: parseInt(data.time_period_years),
      annual_return_rate: parseFloat(data.annual_return_rate),
      annual_step_up_rate: parseFloat(data.annual_step_up_rate) || 0,
    };
    const capValue = parseInputValue(data.step_up_cap);
    if (capValue > 0) {
      payload.step_up_cap = capValue;
    }
    onCalculate(payload);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="input-form">
      <h2>Growth Calculator</h2>
      <p className="form-description">
        Calculate the future value of your investments with annual compounding.
      </p>

      <div className="form-group">
        <label htmlFor="initial_investment">
          Initial Investment Amount ($) <span className="optional-label">Optional</span>
        </label>
        <Controller
          name="initial_investment"
          control={control}
          rules={{
            validate: (v) => parseInputValue(v) >= 0 || 'Must be 0 or greater',
          }}
          render={({ field }) => (
            <input
              id="initial_investment"
              type="text"
              inputMode="decimal"
              value={field.value}
              onChange={(e) => field.onChange(formatInputValue(e.target.value))}
              onBlur={field.onBlur}
              className={errors.initial_investment ? 'error' : ''}
            />
          )}
        />
        {errors.initial_investment && (
          <span className="error-message">{errors.initial_investment.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="monthly_investment">
          Monthly Investment Amount ($)
        </label>
        <Controller
          name="monthly_investment"
          control={control}
          rules={{
            validate: (v) => parseInputValue(v) > 0 || 'Must be greater than 0',
          }}
          render={({ field }) => (
            <input
              id="monthly_investment"
              type="text"
              inputMode="decimal"
              value={field.value}
              onChange={(e) => field.onChange(formatInputValue(e.target.value))}
              onBlur={field.onBlur}
              className={errors.monthly_investment ? 'error' : ''}
            />
          )}
        />
        {errors.monthly_investment && (
          <span className="error-message">{errors.monthly_investment.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="annual_step_up_rate">
          Annual Step-Up Rate (%) <span className="optional-label">Optional</span>
        </label>
        <input
          id="annual_step_up_rate"
          type="number"
          step="0.1"
          {...register('annual_step_up_rate', {
            min: { value: 0, message: 'Must be 0 or greater' },
            max: { value: 100, message: 'Must be 100% or less' },
          })}
          className={errors.annual_step_up_rate ? 'error' : ''}
        />
        {errors.annual_step_up_rate && (
          <span className="error-message">{errors.annual_step_up_rate.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="step_up_cap">
          Step-Up Cap ($) <span className="optional-label">Optional</span>
        </label>
        <Controller
          name="step_up_cap"
          control={control}
          rules={{
            validate: (v) => v === '' || parseInputValue(v) > 0 || 'Must be greater than 0',
          }}
          render={({ field }) => (
            <input
              id="step_up_cap"
              type="text"
              inputMode="decimal"
              placeholder="No cap"
              value={field.value}
              onChange={(e) => field.onChange(formatInputValue(e.target.value))}
              onBlur={field.onBlur}
              className={errors.step_up_cap ? 'error' : ''}
            />
          )}
        />
        {errors.step_up_cap && (
          <span className="error-message">{errors.step_up_cap.message}</span>
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
