import { Controller } from 'react-hook-form';
import { formatInputValue, parseInputValue } from '../../utils/formatters';
import './WithdrawalForm.css';

const WithdrawalForm = ({ register, control, errors, accumulationReturnRate }) => {
  return (
    <fieldset className="withdrawal-form">
      <legend>Withdrawal Phase</legend>

      <div className="form-group">
        <label htmlFor="monthly_withdrawal">
          Monthly Withdrawal ($)
        </label>
        <Controller
          name="monthly_withdrawal"
          control={control}
          rules={{
            validate: (v) => parseInputValue(v) >= 0 || 'Must be 0 or greater',
          }}
          render={({ field }) => (
            <input
              id="monthly_withdrawal"
              type="text"
              inputMode="decimal"
              value={field.value}
              onChange={(e) => field.onChange(formatInputValue(e.target.value))}
              onBlur={field.onBlur}
              className={errors.monthly_withdrawal ? 'error' : ''}
            />
          )}
        />
        {errors.monthly_withdrawal && (
          <span className="error-message">{errors.monthly_withdrawal.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="withdrawal_step_up_rate">
          Withdrawal Step-Up Rate (%) <span className="optional-label">Optional</span>
        </label>
        <input
          id="withdrawal_step_up_rate"
          type="number"
          step="0.1"
          {...register('withdrawal_step_up_rate', {
            min: { value: -50, message: 'Must be -50% or greater' },
            max: { value: 100, message: 'Must be 100% or less' },
          })}
          className={errors.withdrawal_step_up_rate ? 'error' : ''}
        />
        <span className="field-hint">Negative values decrease withdrawal over time</span>
        {errors.withdrawal_step_up_rate && (
          <span className="error-message">{errors.withdrawal_step_up_rate.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="withdrawal_step_up_cap">
          Withdrawal Step-Up Cap ($) <span className="optional-label">Optional</span>
        </label>
        <Controller
          name="withdrawal_step_up_cap"
          control={control}
          rules={{
            validate: (v) => v === '' || parseInputValue(v) > 0 || 'Must be greater than 0',
          }}
          render={({ field }) => (
            <input
              id="withdrawal_step_up_cap"
              type="text"
              inputMode="decimal"
              placeholder="No cap"
              value={field.value}
              onChange={(e) => field.onChange(formatInputValue(e.target.value))}
              onBlur={field.onBlur}
              className={errors.withdrawal_step_up_cap ? 'error' : ''}
            />
          )}
        />
        {errors.withdrawal_step_up_cap && (
          <span className="error-message">{errors.withdrawal_step_up_cap.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="withdrawal_years">
          Withdrawal Period (Years)
        </label>
        <input
          id="withdrawal_years"
          type="number"
          {...register('withdrawal_years', {
            required: 'Withdrawal period is required',
            min: { value: 1, message: 'Must be at least 1 year' },
            max: { value: 50, message: 'Must be 50 years or less' },
          })}
          className={errors.withdrawal_years ? 'error' : ''}
        />
        {errors.withdrawal_years && (
          <span className="error-message">{errors.withdrawal_years.message}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="withdrawal_return_rate">
          Expected Annual Return Rate (%)
        </label>
        <input
          id="withdrawal_return_rate"
          type="number"
          step="0.1"
          {...register('withdrawal_return_rate', {
            required: 'Return rate is required',
            min: { value: 0, message: 'Must be 0 or greater' },
            max: { value: 100, message: 'Must be 100% or less' },
          })}
          className={errors.withdrawal_return_rate ? 'error' : ''}
        />
        {errors.withdrawal_return_rate && (
          <span className="error-message">{errors.withdrawal_return_rate.message}</span>
        )}
      </div>
    </fieldset>
  );
};

export default WithdrawalForm;
