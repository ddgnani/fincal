import { Controller } from 'react-hook-form';
import { formatInputValue, parseInputValue } from '../../utils/formatters';
import './AccumulationForm.css';

const AccumulationForm = ({ register, control, errors }) => {
  return (
    <fieldset className="accumulation-form">
      <legend>Accumulation Phase</legend>

      <div className="form-group">
        <label htmlFor="initial_investment">
          Initial Investment ($) <span className="optional-label">Optional</span>
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
          Monthly Investment ($)
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
        <label htmlFor="accumulation_years">
          Accumulation Period (Years)
        </label>
        <input
          id="accumulation_years"
          type="number"
          {...register('accumulation_years', {
            required: 'Accumulation period is required',
            min: { value: 1, message: 'Must be at least 1 year' },
            max: { value: 50, message: 'Must be 50 years or less' },
          })}
          className={errors.accumulation_years ? 'error' : ''}
        />
        {errors.accumulation_years && (
          <span className="error-message">{errors.accumulation_years.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="accumulation_return_rate">
          Expected Annual Return Rate (%)
        </label>
        <input
          id="accumulation_return_rate"
          type="number"
          step="0.1"
          {...register('accumulation_return_rate', {
            required: 'Return rate is required',
            min: { value: 0, message: 'Must be 0 or greater' },
            max: { value: 100, message: 'Must be 100% or less' },
          })}
          className={errors.accumulation_return_rate ? 'error' : ''}
        />
        {errors.accumulation_return_rate && (
          <span className="error-message">{errors.accumulation_return_rate.message}</span>
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
    </fieldset>
  );
};

export default AccumulationForm;
