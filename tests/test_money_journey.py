"""
Unit tests for Money Journey calculator
"""
import pytest
from api.models.money_journey import MoneyJourneyRequest
from api.services.money_journey import calculate_money_journey


class TestMoneyJourneyAccumulation:
    """Tests that accumulation phase matches SIP calculator output"""

    def test_accumulation_matches_sip(self):
        """Accumulation corpus should match SIP future value for identical inputs"""
        request = MoneyJourneyRequest(
            monthly_investment=5000,
            accumulation_years=10,
            accumulation_return_rate=12.0,
            monthly_withdrawal=50000,
            withdrawal_years=5,
            withdrawal_return_rate=8.0,
        )
        result = calculate_money_journey(request)

        # Import SIP for comparison
        from api.models.sip import SIPCalculationRequest
        from api.services.sip_calculator import calculate_sip_with_annual_compounding

        sip_request = SIPCalculationRequest(
            monthly_investment=5000,
            time_period_years=10,
            annual_return_rate=12.0,
        )
        sip_result = calculate_sip_with_annual_compounding(sip_request)

        assert result.results.corpus_at_retirement == sip_result.results.future_value
        assert result.results.total_contributions == sip_result.results.total_invested

    def test_accumulation_breakdown_phase_label(self):
        """All accumulation years should have phase='accumulation'"""
        request = MoneyJourneyRequest(
            monthly_investment=5000,
            accumulation_years=5,
            accumulation_return_rate=10.0,
            monthly_withdrawal=10000,
            withdrawal_years=3,
            withdrawal_return_rate=8.0,
        )
        result = calculate_money_journey(request)

        accum_entries = [e for e in result.yearly_breakdown if e.phase == "accumulation"]
        assert len(accum_entries) == 5
        for i, entry in enumerate(accum_entries):
            assert entry.year == i + 1


class TestMoneyJourneyWithdrawal:
    """Tests for withdrawal phase math"""

    def test_withdrawal_basic(self):
        """Basic withdrawal: corpus reduces each year"""
        request = MoneyJourneyRequest(
            monthly_investment=10000,
            accumulation_years=10,
            accumulation_return_rate=12.0,
            monthly_withdrawal=20000,
            withdrawal_years=5,
            withdrawal_return_rate=8.0,
        )
        result = calculate_money_journey(request)

        withdrawal_entries = [e for e in result.yearly_breakdown if e.phase == "withdrawal"]
        assert len(withdrawal_entries) == 5
        # Withdrawal years should be numbered continuously
        assert withdrawal_entries[0].year == 11
        assert withdrawal_entries[-1].year == 15

    def test_withdrawal_math_known_values(self):
        """Verify withdrawal math with known inputs"""
        # Use a simple scenario: corpus=1,000,000; withdraw 100,000/yr; 0% return
        request = MoneyJourneyRequest(
            monthly_investment=0.01,  # minimal
            accumulation_years=1,
            accumulation_return_rate=0.0,
            initial_investment=1000000,
            monthly_withdrawal=100000,
            withdrawal_years=3,
            withdrawal_return_rate=0.0,
        )
        result = calculate_money_journey(request)

        # Corpus = 1000000 + 0.01*12 = 1000000.12
        corpus = result.results.corpus_at_retirement
        assert abs(corpus - 1000000.12) < 1

        withdrawal_entries = [e for e in result.yearly_breakdown if e.phase == "withdrawal"]
        # Year 1 withdrawal: 100000*12 = 1,200,000 > corpus → partial withdrawal
        assert result.results.depleted is True
        assert withdrawal_entries[0].balance == 0

    def test_withdrawal_with_returns(self):
        """Withdrawal with positive return rate should preserve corpus longer"""
        request = MoneyJourneyRequest(
            monthly_investment=0.01,
            accumulation_years=1,
            accumulation_return_rate=0.0,
            initial_investment=1000000,
            monthly_withdrawal=5000,
            withdrawal_years=5,
            withdrawal_return_rate=10.0,
        )
        result = calculate_money_journey(request)

        # Annual withdrawal = 60,000; corpus = ~1M; with 10% return should not deplete
        assert result.results.depleted is False
        assert result.results.final_balance > 0

    def test_total_withdrawals_sum(self):
        """total_withdrawals should equal sum of annual withdrawal amounts"""
        request = MoneyJourneyRequest(
            monthly_investment=5000,
            accumulation_years=10,
            accumulation_return_rate=12.0,
            monthly_withdrawal=20000,
            withdrawal_years=5,
            withdrawal_return_rate=8.0,
        )
        result = calculate_money_journey(request)

        withdrawal_entries = [e for e in result.yearly_breakdown if e.phase == "withdrawal"]
        sum_withdrawals = sum(e.annual_amount for e in withdrawal_entries)
        assert abs(result.results.total_withdrawals - sum_withdrawals) < 1


class TestMoneyJourneyDepletion:
    """Tests for depletion detection"""

    def test_depletion_high_withdrawal(self):
        """High withdrawal should deplete corpus"""
        request = MoneyJourneyRequest(
            monthly_investment=1000,
            accumulation_years=5,
            accumulation_return_rate=10.0,
            monthly_withdrawal=100000,
            withdrawal_years=10,
            withdrawal_return_rate=5.0,
        )
        result = calculate_money_journey(request)

        assert result.results.depleted is True
        assert result.results.depletion_year is not None
        assert result.results.final_balance == 0

    def test_depletion_year_correct(self):
        """Depletion year should be the first year balance hits zero"""
        request = MoneyJourneyRequest(
            monthly_investment=0.01,
            accumulation_years=1,
            accumulation_return_rate=0.0,
            initial_investment=100000,
            monthly_withdrawal=3000,
            withdrawal_years=10,
            withdrawal_return_rate=0.0,
        )
        result = calculate_money_journey(request)

        # Corpus ≈ 100000.12, annual withdrawal = 36000
        # Year 2 (accum=1): 100000.12 - 36000 = 64000.12
        # Year 3: 64000.12 - 36000 = 28000.12
        # Year 4: 28000.12 - 36000 → partial, depleted
        assert result.results.depleted is True
        assert result.results.depletion_year == 4  # accumulation year 1 + withdrawal year 3

    def test_post_depletion_years_zero(self):
        """After depletion, remaining years should have zero balance and withdrawal"""
        request = MoneyJourneyRequest(
            monthly_investment=0.01,
            accumulation_years=1,
            accumulation_return_rate=0.0,
            initial_investment=50000,
            monthly_withdrawal=3000,
            withdrawal_years=5,
            withdrawal_return_rate=0.0,
        )
        result = calculate_money_journey(request)

        withdrawal_entries = [e for e in result.yearly_breakdown if e.phase == "withdrawal"]
        found_depleted = False
        for entry in withdrawal_entries:
            if entry.balance == 0 and found_depleted:
                assert entry.annual_amount == 0
                assert entry.monthly_amount == 0
            if entry.balance == 0:
                found_depleted = True


class TestWithdrawalStepUp:
    """Tests for withdrawal step-up rate"""

    def test_negative_step_up(self):
        """Negative step-up should decrease withdrawal each year"""
        request = MoneyJourneyRequest(
            monthly_investment=0.01,
            accumulation_years=1,
            accumulation_return_rate=0.0,
            initial_investment=1000000,
            monthly_withdrawal=10000,
            withdrawal_years=3,
            withdrawal_return_rate=0.0,
            withdrawal_step_up_rate=-10,
        )
        result = calculate_money_journey(request)

        withdrawal_entries = [e for e in result.yearly_breakdown if e.phase == "withdrawal"]
        # Year 1: 10000, Year 2: 9000, Year 3: 8100
        assert withdrawal_entries[0].monthly_amount == 10000
        assert withdrawal_entries[1].monthly_amount == 9000
        assert withdrawal_entries[2].monthly_amount == 8100

    def test_positive_step_up(self):
        """Positive step-up should increase withdrawal each year"""
        request = MoneyJourneyRequest(
            monthly_investment=0.01,
            accumulation_years=1,
            accumulation_return_rate=0.0,
            initial_investment=5000000,
            monthly_withdrawal=10000,
            withdrawal_years=3,
            withdrawal_return_rate=0.0,
            withdrawal_step_up_rate=10,
        )
        result = calculate_money_journey(request)

        withdrawal_entries = [e for e in result.yearly_breakdown if e.phase == "withdrawal"]
        assert withdrawal_entries[0].monthly_amount == 10000
        assert withdrawal_entries[1].monthly_amount == 11000
        assert withdrawal_entries[2].monthly_amount == 12100

    def test_step_up_with_cap(self):
        """Withdrawal step-up cap should limit the monthly withdrawal"""
        request = MoneyJourneyRequest(
            monthly_investment=0.01,
            accumulation_years=1,
            accumulation_return_rate=0.0,
            initial_investment=5000000,
            monthly_withdrawal=10000,
            withdrawal_years=3,
            withdrawal_return_rate=0.0,
            withdrawal_step_up_rate=20,
            withdrawal_step_up_cap=11000,
        )
        result = calculate_money_journey(request)

        withdrawal_entries = [e for e in result.yearly_breakdown if e.phase == "withdrawal"]
        assert withdrawal_entries[0].monthly_amount == 10000
        # Year 2: min(12000, 11000) = 11000
        assert withdrawal_entries[1].monthly_amount == 11000
        # Year 3: min(11000*1.2=13200, 11000) = 11000
        assert withdrawal_entries[2].monthly_amount == 11000


class TestMoneyJourneyEndToEnd:
    """End-to-end lifecycle tests"""

    def test_full_lifecycle(self):
        """Full journey should have correct total years in breakdown"""
        request = MoneyJourneyRequest(
            monthly_investment=5000,
            accumulation_years=25,
            accumulation_return_rate=12.0,
            monthly_withdrawal=50000,
            withdrawal_years=20,
            withdrawal_return_rate=8.0,
        )
        result = calculate_money_journey(request)

        assert result.status == "success"
        assert len(result.yearly_breakdown) == 45  # 25 + 20
        assert result.yearly_breakdown[0].phase == "accumulation"
        assert result.yearly_breakdown[24].phase == "accumulation"
        assert result.yearly_breakdown[25].phase == "withdrawal"
        assert result.yearly_breakdown[-1].phase == "withdrawal"

    def test_inputs_preserved(self):
        """Input values should be echoed back in response"""
        request = MoneyJourneyRequest(
            monthly_investment=5000,
            accumulation_years=25,
            accumulation_return_rate=12.0,
            monthly_withdrawal=50000,
            withdrawal_years=20,
            withdrawal_return_rate=8.0,
            withdrawal_step_up_rate=5,
        )
        result = calculate_money_journey(request)

        assert result.inputs["monthly_investment"] == 5000
        assert result.inputs["accumulation_years"] == 25
        assert result.inputs["accumulation_return_rate"] == 12.0
        assert result.inputs["monthly_withdrawal"] == 50000
        assert result.inputs["withdrawal_years"] == 20
        assert result.inputs["withdrawal_return_rate"] == 8.0
        assert result.inputs["withdrawal_step_up_rate"] == 5


class TestMoneyJourneyValidation:
    """Validation rejection tests"""

    def test_negative_monthly_investment(self):
        with pytest.raises(Exception):
            MoneyJourneyRequest(
                monthly_investment=-1000,
                accumulation_years=10,
                accumulation_return_rate=12.0,
                monthly_withdrawal=50000,
                withdrawal_years=20,
                withdrawal_return_rate=8.0,
            )

    def test_zero_monthly_withdrawal_allowed(self):
        """$0 withdrawal is valid — models a passive growth phase."""
        request = MoneyJourneyRequest(
            monthly_investment=5000,
            accumulation_years=10,
            accumulation_return_rate=12.0,
            monthly_withdrawal=0,
            withdrawal_years=20,
            withdrawal_return_rate=8.0,
        )
        assert request.monthly_withdrawal == 0

    def test_accumulation_years_too_high(self):
        with pytest.raises(Exception):
            MoneyJourneyRequest(
                monthly_investment=5000,
                accumulation_years=51,
                accumulation_return_rate=12.0,
                monthly_withdrawal=50000,
                withdrawal_years=20,
                withdrawal_return_rate=8.0,
            )

    def test_withdrawal_step_up_too_low(self):
        with pytest.raises(Exception):
            MoneyJourneyRequest(
                monthly_investment=5000,
                accumulation_years=10,
                accumulation_return_rate=12.0,
                monthly_withdrawal=50000,
                withdrawal_years=20,
                withdrawal_return_rate=8.0,
                withdrawal_step_up_rate=-60,  # below -50 limit
            )

    def test_return_rate_too_high(self):
        with pytest.raises(Exception):
            MoneyJourneyRequest(
                monthly_investment=5000,
                accumulation_years=10,
                accumulation_return_rate=101.0,
                monthly_withdrawal=50000,
                withdrawal_years=20,
                withdrawal_return_rate=8.0,
            )
