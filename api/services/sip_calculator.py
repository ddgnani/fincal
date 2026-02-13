"""
SIP Calculator service with annual compounding logic
"""
from typing import List, Dict
from api.models.sip import (
    SIPCalculationRequest,
    SIPCalculationResponse,
    SIPCalculationResults,
    YearlyBreakdown
)


def calculate_sip_with_annual_compounding(request: SIPCalculationRequest) -> SIPCalculationResponse:
    """
    Calculate SIP returns with annual compounding.

    This uses a month-by-month accurate calculation where:
    - Each monthly investment is tracked separately
    - Interest is compounded annually at year-end
    - Each investment grows based on how many complete years it stays invested

    Args:
        request: SIPCalculationRequest with monthly_investment, time_period_years, annual_return_rate

    Returns:
        SIPCalculationResponse with results and yearly breakdown
    """
    monthly_investment = request.monthly_investment
    time_period_years = request.time_period_years
    annual_rate = request.annual_return_rate / 100  # Convert percentage to decimal
    initial_investment = request.initial_investment

    # Initialize tracking variables
    yearly_breakdown = []
    total_invested = initial_investment

    # Calculate month-by-month for accuracy
    # Each monthly investment will compound based on complete years invested
    for year in range(1, time_period_years + 1):
        # Amount invested this year (12 monthly investments + initial in year 1)
        invested_this_year = monthly_investment * 12
        if year == 1:
            invested_this_year += initial_investment
        total_invested += monthly_investment * 12

        # Calculate future value at end of this year
        # We need to consider all investments made up to this year
        future_value = 0

        # Initial investment compounds for the full period
        if initial_investment > 0:
            future_value += initial_investment * ((1 + annual_rate) ** year)

        # Go through each year and calculate the future value of those investments
        for inv_year in range(1, year + 1):
            # 12 monthly investments in inv_year
            year_investment = monthly_investment * 12

            # How many complete years will this investment compound?
            years_to_compound = year - inv_year

            # Future value of this year's investments
            if years_to_compound > 0:
                fv = year_investment * ((1 + annual_rate) ** years_to_compound)
            else:
                # Investments made in the current year don't compound yet
                fv = year_investment

            future_value += fv

        # Add this year to breakdown
        yearly_breakdown.append(YearlyBreakdown(
            year=year,
            invested_this_year=round(invested_this_year, 2),
            cumulative_invested=round(total_invested, 2),
            future_value=round(future_value, 2)
        ))

    # Final calculations
    final_future_value = yearly_breakdown[-1].future_value
    total_returns = final_future_value - total_invested
    returns_percentage = (total_returns / total_invested) * 100 if total_invested > 0 else 0

    # Build response
    results = SIPCalculationResults(
        future_value=round(final_future_value, 2),
        total_invested=round(total_invested, 2),
        total_returns=round(total_returns, 2),
        returns_percentage=round(returns_percentage, 2)
    )

    inputs_dict = {
        "monthly_investment": monthly_investment,
        "time_period_years": time_period_years,
        "annual_return_rate": request.annual_return_rate,
        "initial_investment": initial_investment,
        "compounding_frequency": "annually"
    }

    return SIPCalculationResponse(
        status="success",
        inputs=inputs_dict,
        results=results,
        yearly_breakdown=yearly_breakdown
    )


def format_currency(amount: float) -> str:
    """
    Format amount as currency with commas

    Args:
        amount: Numeric amount

    Returns:
        Formatted string like "$1,234,567.89"
    """
    return f"${amount:,.2f}"


def calculate_simple_future_value(
    monthly_investment: float,
    years: int,
    annual_rate: float
) -> float:
    """
    Simple SIP future value calculation (for reference/testing)
    Uses the standard formula: FV = P × 12 × [(1 + r)^n - 1] / r

    This assumes all 12 monthly investments are made at year start.

    Args:
        monthly_investment: Monthly investment amount
        years: Number of years
        annual_rate: Annual interest rate (as decimal, e.g., 0.12 for 12%)

    Returns:
        Future value
    """
    if annual_rate == 0:
        return monthly_investment * 12 * years

    # Standard SIP formula
    fv = monthly_investment * 12 * (((1 + annual_rate) ** years - 1) / annual_rate)
    return fv
