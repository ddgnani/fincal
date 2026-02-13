"""
Unit tests for SIP calculator
"""
import pytest
from api.models.sip import SIPCalculationRequest
from api.services.sip_calculator import (
    calculate_sip_with_annual_compounding,
    calculate_simple_future_value,
    format_currency
)


class TestSIPCalculator:
    """Test suite for SIP calculator functionality"""

    def test_basic_calculation(self):
        """Test basic SIP calculation with standard inputs"""
        request = SIPCalculationRequest(
            monthly_investment=5000,
            time_period_years=10,
            annual_return_rate=12.0
        )

        result = calculate_sip_with_annual_compounding(request)

        assert result.status == "success"
        assert result.results.total_invested == 600000  # 5000 * 12 * 10
        assert result.results.future_value > result.results.total_invested
        assert result.results.total_returns > 0
        assert len(result.yearly_breakdown) == 10

    def test_zero_return_rate(self):
        """Test calculation with 0% return rate"""
        request = SIPCalculationRequest(
            monthly_investment=1000,
            time_period_years=5,
            annual_return_rate=0.0
        )

        result = calculate_sip_with_annual_compounding(request)

        # With 0% return, future value should equal total invested
        assert result.results.future_value == 60000  # 1000 * 12 * 5
        assert result.results.total_invested == 60000
        assert result.results.total_returns == 0
        assert result.results.returns_percentage == 0

    def test_single_year_investment(self):
        """Test calculation for single year"""
        request = SIPCalculationRequest(
            monthly_investment=10000,
            time_period_years=1,
            annual_return_rate=10.0
        )

        result = calculate_sip_with_annual_compounding(request)

        assert result.results.total_invested == 120000  # 10000 * 12
        assert len(result.yearly_breakdown) == 1
        # In first year, no compounding happens yet
        assert result.results.future_value == 120000

    def test_high_return_rate(self):
        """Test calculation with high return rate"""
        request = SIPCalculationRequest(
            monthly_investment=1000,
            time_period_years=20,
            annual_return_rate=15.0
        )

        result = calculate_sip_with_annual_compounding(request)

        assert result.results.total_invested == 240000  # 1000 * 12 * 20
        # Future value should be significantly higher with 15% return
        assert result.results.future_value > 500000
        assert result.results.returns_percentage > 100

    def test_yearly_breakdown_structure(self):
        """Test yearly breakdown has correct structure"""
        request = SIPCalculationRequest(
            monthly_investment=5000,
            time_period_years=3,
            annual_return_rate=10.0
        )

        result = calculate_sip_with_annual_compounding(request)

        assert len(result.yearly_breakdown) == 3

        # Check first year
        year1 = result.yearly_breakdown[0]
        assert year1.year == 1
        assert year1.invested_this_year == 60000  # 5000 * 12
        assert year1.cumulative_invested == 60000
        assert year1.future_value == 60000  # No compounding in first year

        # Check second year
        year2 = result.yearly_breakdown[1]
        assert year2.year == 2
        assert year2.invested_this_year == 60000
        assert year2.cumulative_invested == 120000
        # Year 1 investments compound for 1 year, year 2 investments don't compound
        expected_fv_year2 = 60000 * 1.10 + 60000
        assert abs(year2.future_value - expected_fv_year2) < 1  # Allow small rounding diff

        # Check third year
        year3 = result.yearly_breakdown[2]
        assert year3.year == 3
        assert year3.invested_this_year == 60000
        assert year3.cumulative_invested == 180000

    def test_cumulative_invested_progression(self):
        """Test that cumulative invested increases linearly"""
        request = SIPCalculationRequest(
            monthly_investment=1000,
            time_period_years=5,
            annual_return_rate=8.0
        )

        result = calculate_sip_with_annual_compounding(request)

        for i, breakdown in enumerate(result.yearly_breakdown):
            expected_cumulative = 12000 * (i + 1)  # 1000 * 12 * year
            assert breakdown.cumulative_invested == expected_cumulative

    def test_validation_negative_investment(self):
        """Test validation rejects negative investment"""
        with pytest.raises(Exception):
            SIPCalculationRequest(
                monthly_investment=-1000,
                time_period_years=10,
                annual_return_rate=12.0
            )

    def test_validation_zero_investment(self):
        """Test validation rejects zero investment"""
        with pytest.raises(Exception):
            SIPCalculationRequest(
                monthly_investment=0,
                time_period_years=10,
                annual_return_rate=12.0
            )

    def test_validation_negative_years(self):
        """Test validation rejects negative years"""
        with pytest.raises(Exception):
            SIPCalculationRequest(
                monthly_investment=5000,
                time_period_years=-5,
                annual_return_rate=12.0
            )

    def test_validation_years_too_high(self):
        """Test validation rejects years > 50"""
        with pytest.raises(Exception):
            SIPCalculationRequest(
                monthly_investment=5000,
                time_period_years=51,
                annual_return_rate=12.0
            )

    def test_validation_negative_return_rate(self):
        """Test validation rejects negative return rate"""
        with pytest.raises(Exception):
            SIPCalculationRequest(
                monthly_investment=5000,
                time_period_years=10,
                annual_return_rate=-5.0
            )

    def test_validation_return_rate_too_high(self):
        """Test validation rejects return rate > 100%"""
        with pytest.raises(Exception):
            SIPCalculationRequest(
                monthly_investment=5000,
                time_period_years=10,
                annual_return_rate=101.0
            )

    def test_format_currency(self):
        """Test currency formatting utility"""
        assert format_currency(1000) == "$1,000.00"
        assert format_currency(1234567.89) == "$1,234,567.89"
        assert format_currency(0) == "$0.00"
        assert format_currency(99.99) == "$99.99"

    def test_simple_future_value_formula(self):
        """Test the simple FV formula for reference"""
        # Test with 0% return
        fv = calculate_simple_future_value(1000, 10, 0)
        assert fv == 120000  # 1000 * 12 * 10

        # Test with non-zero return
        fv = calculate_simple_future_value(5000, 10, 0.12)
        assert fv > 600000  # Should be greater than total invested

    def test_inputs_preserved_in_response(self):
        """Test that input values are preserved in response"""
        request = SIPCalculationRequest(
            monthly_investment=7500,
            time_period_years=15,
            annual_return_rate=14.5
        )

        result = calculate_sip_with_annual_compounding(request)

        assert result.inputs["monthly_investment"] == 7500
        assert result.inputs["time_period_years"] == 15
        assert result.inputs["annual_return_rate"] == 14.5
        assert result.inputs["compounding_frequency"] == "annually"

    def test_initial_investment_basic(self):
        """Test initial investment compounds correctly over the full period"""
        request = SIPCalculationRequest(
            monthly_investment=5000,
            time_period_years=3,
            annual_return_rate=10.0,
            initial_investment=100000
        )

        result = calculate_sip_with_annual_compounding(request)

        # Total invested = 100000 + 5000 * 12 * 3 = 280000
        assert result.results.total_invested == 280000

        # Year 3 future value:
        # Initial: 100000 * 1.1^3 = 133100
        # SIP year 1: 60000 * 1.1^2 = 72600
        # SIP year 2: 60000 * 1.1^1 = 66000
        # SIP year 3: 60000 * 1.1^0 = 60000
        # Total = 133100 + 72600 + 66000 + 60000 = 331700
        assert abs(result.results.future_value - 331700) < 1

    def test_initial_investment_zero(self):
        """Test that default 0 initial investment produces same results as before"""
        request_without = SIPCalculationRequest(
            monthly_investment=5000,
            time_period_years=10,
            annual_return_rate=12.0
        )
        request_with_zero = SIPCalculationRequest(
            monthly_investment=5000,
            time_period_years=10,
            annual_return_rate=12.0,
            initial_investment=0
        )

        result_without = calculate_sip_with_annual_compounding(request_without)
        result_with_zero = calculate_sip_with_annual_compounding(request_with_zero)

        assert result_without.results.future_value == result_with_zero.results.future_value
        assert result_without.results.total_invested == result_with_zero.results.total_invested

    def test_initial_investment_only(self):
        """Test initial investment with minimal monthly contribution"""
        request = SIPCalculationRequest(
            monthly_investment=0.01,
            time_period_years=5,
            annual_return_rate=10.0,
            initial_investment=100000
        )

        result = calculate_sip_with_annual_compounding(request)

        # Initial investment should dominate: 100000 * 1.1^5 = 161051.00
        # Monthly contributions are negligible (0.01 * 12 * 5 = 0.60)
        assert result.results.future_value > 161050
        assert result.results.total_invested == 100000 + 0.01 * 12 * 5

    def test_initial_investment_in_yearly_breakdown(self):
        """Test that year 1 includes initial investment in invested_this_year and cumulative_invested"""
        request = SIPCalculationRequest(
            monthly_investment=1000,
            time_period_years=3,
            annual_return_rate=10.0,
            initial_investment=50000
        )

        result = calculate_sip_with_annual_compounding(request)

        year1 = result.yearly_breakdown[0]
        assert year1.invested_this_year == 50000 + 1000 * 12  # initial + monthly
        assert year1.cumulative_invested == 50000 + 1000 * 12

        year2 = result.yearly_breakdown[1]
        assert year2.invested_this_year == 1000 * 12  # only monthly
        assert year2.cumulative_invested == 50000 + 1000 * 12 * 2

    def test_initial_investment_in_inputs(self):
        """Test that the response echoes back the initial investment"""
        request = SIPCalculationRequest(
            monthly_investment=5000,
            time_period_years=10,
            annual_return_rate=12.0,
            initial_investment=25000
        )

        result = calculate_sip_with_annual_compounding(request)

        assert result.inputs["initial_investment"] == 25000

    def test_returns_calculation(self):
        """Test that returns are calculated correctly"""
        request = SIPCalculationRequest(
            monthly_investment=2000,
            time_period_years=5,
            annual_return_rate=10.0
        )

        result = calculate_sip_with_annual_compounding(request)

        # Verify returns calculation
        calculated_returns = result.results.future_value - result.results.total_invested
        assert abs(result.results.total_returns - calculated_returns) < 0.01

        # Verify returns percentage
        calculated_percentage = (calculated_returns / result.results.total_invested) * 100
        assert abs(result.results.returns_percentage - calculated_percentage) < 0.01
