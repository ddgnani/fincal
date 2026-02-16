"""
Pydantic models for Money Journey API
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class MoneyJourneyRequest(BaseModel):
    """Request model for Money Journey calculation"""
    # Accumulation phase fields
    monthly_investment: float = Field(
        gt=0,
        description="Monthly investment amount during accumulation (must be greater than 0)"
    )
    accumulation_years: int = Field(
        gt=0,
        le=50,
        description="Accumulation period in years (1-50)"
    )
    accumulation_return_rate: float = Field(
        ge=0,
        le=100,
        description="Expected annual return rate during accumulation (%)"
    )
    initial_investment: float = Field(
        ge=0,
        default=0,
        description="One-time initial investment amount (optional, default 0)"
    )
    annual_step_up_rate: float = Field(
        ge=0,
        le=100,
        default=0,
        description="Annual percentage increase in monthly contribution (0-100)"
    )
    step_up_cap: Optional[float] = Field(
        gt=0,
        default=None,
        description="Maximum monthly contribution cap when using step-up (optional)"
    )
    # Withdrawal phase fields
    monthly_withdrawal: float = Field(
        ge=0,
        description="Monthly withdrawal amount (0 for passive growth phase)"
    )
    withdrawal_years: int = Field(
        gt=0,
        le=50,
        description="Withdrawal period in years (1-50)"
    )
    withdrawal_return_rate: float = Field(
        ge=0,
        le=100,
        description="Expected annual return rate during withdrawal (%)"
    )
    withdrawal_step_up_rate: float = Field(
        ge=-50,
        le=100,
        default=0,
        description="Annual percentage change in withdrawal amount (-50 to 100)"
    )
    withdrawal_step_up_cap: Optional[float] = Field(
        gt=0,
        default=None,
        description="Maximum monthly withdrawal cap when using step-up (optional)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "monthly_investment": 5000,
                "accumulation_years": 25,
                "accumulation_return_rate": 12.0,
                "monthly_withdrawal": 50000,
                "withdrawal_years": 20,
                "withdrawal_return_rate": 8.0
            }
        }


class MoneyJourneyYearBreakdown(BaseModel):
    """Yearly breakdown data for money journey"""
    year: int = Field(description="Year number (continuous across both phases)")
    phase: str = Field(description="Phase: 'accumulation' or 'withdrawal'")
    monthly_amount: float = Field(description="Monthly contribution or withdrawal for this year")
    annual_amount: float = Field(description="Total annual contribution or withdrawal")
    balance: float = Field(description="Balance at end of year")


class MoneyJourneyResults(BaseModel):
    """Calculation results for money journey"""
    corpus_at_retirement: float = Field(description="Corpus at end of accumulation phase")
    total_contributions: float = Field(description="Total amount contributed during accumulation")
    total_withdrawals: float = Field(description="Total amount withdrawn during withdrawal phase")
    final_balance: float = Field(description="Balance at end of withdrawal phase")
    depleted: bool = Field(description="Whether the corpus was fully depleted")
    depletion_year: Optional[int] = Field(default=None, description="Year when corpus was depleted (if applicable)")


class MoneyJourneyResponse(BaseModel):
    """Response model for Money Journey calculation"""
    status: str = Field(default="success", description="Response status")
    inputs: dict = Field(description="Input parameters used for calculation")
    results: MoneyJourneyResults = Field(description="Calculation results")
    yearly_breakdown: List[MoneyJourneyYearBreakdown] = Field(description="Year-by-year breakdown")
