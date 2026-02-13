import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { formatCurrency } from '../../utils/formatters';
import './GrowthChart.css';

const GrowthChart = ({ yearlyBreakdown, inputs }) => {
  if (!yearlyBreakdown || yearlyBreakdown.length === 0) return null;

  const { annual_return_rate } = inputs;

  // Format data for Recharts
  const chartData = yearlyBreakdown.map((item) => ({
    year: `Year ${item.year}`,
    futureValue: item.future_value,
    totalInvested: item.cumulative_invested,
    monthlyContribution: item.monthly_contribution,
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{payload[0].payload.year}</p>
          <p className="tooltip-future">
            Future Value: <strong>{formatCurrency(payload[0].value)}</strong>
          </p>
          <p className="tooltip-invested">
            Total Invested: <strong>{formatCurrency(payload[1].value)}</strong>
          </p>
          <p className="tooltip-returns">
            Returns: <strong>{formatCurrency(payload[0].value - payload[1].value)}</strong>
          </p>
          {inputs.annual_step_up_rate > 0 && (
            <p className="tooltip-contribution">
              Monthly Contribution: <strong>{formatCurrency(payload[0].payload.monthlyContribution)}</strong>
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="growth-chart">
      <div className="chart-header">
        <h3>Investment Growth Over Time</h3>
        <p className="chart-description">
          The chart below shows an estimate of how much your investment will grow over time,
          according to the interest rate ({annual_return_rate}%) and compounding schedule (annual) you specified.
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
          <Legend
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="line"
          />
          <Line
            type="monotone"
            dataKey="futureValue"
            stroke="#ff6b6b"
            strokeWidth={3}
            name={`Future Value (${annual_return_rate}%)`}
            dot={{ fill: '#ff6b6b', r: 4 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="totalInvested"
            stroke="#4ecdc4"
            strokeWidth={3}
            name="Total Contributions"
            dot={{ fill: '#4ecdc4', r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="chart-disclaimer">
        <p>
          <strong>Disclaimer:</strong> Please remember that slight adjustments in any of those
          variables can affect the outcome. Use this calculator and provide different figures
          to show different scenarios. Past performance is not indicative of future results.
        </p>
      </div>
    </div>
  );
};

export default GrowthChart;
