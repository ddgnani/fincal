"""
Money Journey calculator service — accumulation + withdrawal lifecycle
"""
from api.models.sip import SIPCalculationRequest
from api.models.money_journey import (
    MoneyJourneyRequest,
    MoneyJourneyResponse,
    MoneyJourneyResults,
    MoneyJourneyYearBreakdown,
)
from api.services.sip_calculator import calculate_sip_with_annual_compounding


def calculate_money_journey(request: MoneyJourneyRequest) -> MoneyJourneyResponse:
    """
    Calculate full money journey: accumulation phase then withdrawal phase.

    Accumulation reuses the existing SIP calculator logic.
    Withdrawal applies year-by-year: withdraw at start of year, compound remainder.
    """
    # --- Accumulation phase (reuse SIP logic) ---
    sip_request = SIPCalculationRequest(
        monthly_investment=request.monthly_investment,
        time_period_years=request.accumulation_years,
        annual_return_rate=request.accumulation_return_rate,
        initial_investment=request.initial_investment,
        annual_step_up_rate=request.annual_step_up_rate,
        step_up_cap=request.step_up_cap,
    )
    sip_response = calculate_sip_with_annual_compounding(sip_request)

    corpus_at_retirement = sip_response.results.future_value
    total_contributions = sip_response.results.total_invested

    # Convert SIP yearly breakdown to MoneyJourneyYearBreakdown
    yearly_breakdown = []
    for entry in sip_response.yearly_breakdown:
        yearly_breakdown.append(MoneyJourneyYearBreakdown(
            year=entry.year,
            phase="accumulation",
            monthly_amount=round(entry.monthly_contribution, 2),
            annual_amount=round(entry.invested_this_year, 2),
            balance=round(entry.future_value, 2),
        ))

    # --- Withdrawal phase ---
    balance = corpus_at_retirement
    withdrawal_rate = request.withdrawal_return_rate / 100
    step_up_rate = request.withdrawal_step_up_rate / 100
    current_monthly_withdrawal = request.monthly_withdrawal
    total_withdrawals = 0.0
    depleted = False
    depletion_year = None

    for wy in range(1, request.withdrawal_years + 1):
        year_number = request.accumulation_years + wy

        # Step-up from year 2 onwards
        if wy > 1:
            current_monthly_withdrawal = current_monthly_withdrawal * (1 + step_up_rate)
            if request.withdrawal_step_up_cap is not None:
                current_monthly_withdrawal = min(current_monthly_withdrawal, request.withdrawal_step_up_cap)

        annual_withdrawal = current_monthly_withdrawal * 12

        # Withdraw at start of year
        if balance <= 0:
            # Already depleted
            depleted = True
            if depletion_year is None:
                depletion_year = year_number
            yearly_breakdown.append(MoneyJourneyYearBreakdown(
                year=year_number,
                phase="withdrawal",
                monthly_amount=0,
                annual_amount=0,
                balance=0,
            ))
            continue

        if balance < annual_withdrawal:
            # Partial withdrawal — corpus depleted this year
            total_withdrawals += balance
            depleted = True
            depletion_year = year_number
            yearly_breakdown.append(MoneyJourneyYearBreakdown(
                year=year_number,
                phase="withdrawal",
                monthly_amount=round(balance / 12, 2),
                annual_amount=round(balance, 2),
                balance=0,
            ))
            balance = 0
            continue

        # Full withdrawal, then compound remainder
        balance -= annual_withdrawal
        total_withdrawals += annual_withdrawal
        balance = balance * (1 + withdrawal_rate)

        yearly_breakdown.append(MoneyJourneyYearBreakdown(
            year=year_number,
            phase="withdrawal",
            monthly_amount=round(current_monthly_withdrawal, 2),
            annual_amount=round(annual_withdrawal, 2),
            balance=round(balance, 2),
        ))

    final_balance = round(balance, 2)

    results = MoneyJourneyResults(
        corpus_at_retirement=round(corpus_at_retirement, 2),
        total_contributions=round(total_contributions, 2),
        total_withdrawals=round(total_withdrawals, 2),
        final_balance=final_balance,
        depleted=depleted,
        depletion_year=depletion_year,
    )

    inputs_dict = {
        "monthly_investment": request.monthly_investment,
        "accumulation_years": request.accumulation_years,
        "accumulation_return_rate": request.accumulation_return_rate,
        "initial_investment": request.initial_investment,
        "annual_step_up_rate": request.annual_step_up_rate,
        "step_up_cap": request.step_up_cap,
        "monthly_withdrawal": request.monthly_withdrawal,
        "withdrawal_years": request.withdrawal_years,
        "withdrawal_return_rate": request.withdrawal_return_rate,
        "withdrawal_step_up_rate": request.withdrawal_step_up_rate,
        "withdrawal_step_up_cap": request.withdrawal_step_up_cap,
    }

    return MoneyJourneyResponse(
        status="success",
        inputs=inputs_dict,
        results=results,
        yearly_breakdown=yearly_breakdown,
    )
