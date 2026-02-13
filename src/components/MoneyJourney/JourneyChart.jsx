import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
} from 'recharts';
import { formatCurrency } from '../../utils/formatters';
import './JourneyChart.css';

const JourneyChart = ({ yearlyBreakdown, inputs }) => {
  if (!yearlyBreakdown || yearlyBreakdown.length === 0) return null;

  const chartData = yearlyBreakdown.map((item) => ({
    year: `Year ${item.year}`,
    balance: item.balance,
    phase: item.phase,
    monthlyAmount: item.monthly_amount,
  }));

  const transitionYear = `Year ${inputs.accumulation_years}`;

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="journey-tooltip">
          <p className="tooltip-label">{data.year}</p>
          <p className="tooltip-phase">
            Phase: <strong>{data.phase === 'accumulation' ? 'Accumulation' : 'Withdrawal'}</strong>
          </p>
          <p className="tooltip-balance">
            Balance: <strong>{formatCurrency(data.balance)}</strong>
          </p>
          <p className="tooltip-amount">
            Monthly {data.phase === 'accumulation' ? 'Contribution' : 'Withdrawal'}:{' '}
            <strong>{formatCurrency(data.monthlyAmount)}</strong>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="journey-chart">
      <div className="chart-header">
        <h3>Money Journey Over Time</h3>
        <p className="chart-description">
          Your balance grows during the accumulation phase ({inputs.accumulation_return_rate}% return)
          and draws down during withdrawal ({inputs.withdrawal_return_rate}% return).
        </p>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="year"
            tick={{ fill: '#666', fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            tick={{ fill: '#666', fontSize: 12 }}
            tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
          />
          <Tooltip content={<CustomTooltip />} />
          <ReferenceLine
            x={transitionYear}
            stroke="#ff9800"
            strokeDasharray="5 5"
            strokeWidth={2}
            label={{ value: 'Withdrawal Begins', position: 'top', fill: '#ff9800', fontSize: 12 }}
          />
          <Line
            type="monotone"
            dataKey="balance"
            stroke="#667eea"
            strokeWidth={3}
            name="Balance"
            dot={{ fill: '#667eea', r: 3 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="chart-disclaimer">
        <p>
          <strong>Disclaimer:</strong> This projection is an estimate based on the inputs provided.
          Actual returns may vary. Past performance is not indicative of future results.
        </p>
      </div>
    </div>
  );
};

export default JourneyChart;
