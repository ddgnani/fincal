"""
Pydantic models for SIP calculator API
"""
from typing import List
from pydantic import BaseModel, Field


class SIPCalculationRequest(BaseModel):
    """Request model for SIP calculation"""
    monthly_investment: float = Field(
        gt=0,
        description="Monthly investment amount (must be greater than 0)"
    )
    time_period_years: int = Field(
        gt=0,
        le=50,
        description="Investment period in years (1-50)"
    )
    annual_return_rate: float = Field(
        ge=0,
        le=100,
        description="Expected annual return rate in percentage (0-100)"
    )
    initial_investment: float = Field(
        ge=0,
        default=0,
        description="One-time initial investment amount (optional, default 0)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "monthly_investment": 5000,
                "time_period_years": 10,
                "annual_return_rate": 12.0,
                "initial_investment": 0
            }
        }


class YearlyBreakdown(BaseModel):
    """Yearly breakdown data"""
    year: int = Field(description="Year number")
    invested_this_year: float = Field(description="Amount invested in this year")
    cumulative_invested: float = Field(description="Total amount invested up to this year")
    future_value: float = Field(description="Future value at the end of this year")


class SIPCalculationResults(BaseModel):
    """Calculation results"""
    future_value: float = Field(description="Total future value of investment")
    total_invested: float = Field(description="Total amount invested")
    total_returns: float = Field(description="Total returns earned")
    returns_percentage: float = Field(description="Returns as percentage of invested amount")


class SIPCalculationResponse(BaseModel):
    """Response model for SIP calculation"""
    status: str = Field(default="success", description="Response status")
    inputs: dict = Field(description="Input parameters used for calculation")
    results: SIPCalculationResults = Field(description="Calculation results")
    yearly_breakdown: List[YearlyBreakdown] = Field(description="Year-by-year breakdown")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "inputs": {
                    "monthly_investment": 5000,
                    "time_period_years": 10,
                    "annual_return_rate": 12.0,
                    "compounding_frequency": "annually"
                },
                "results": {
                    "future_value": 1381128.50,
                    "total_invested": 600000,
                    "total_returns": 781128.50,
                    "returns_percentage": 130.19
                },
                "yearly_breakdown": [
                    {
                        "year": 1,
                        "invested_this_year": 60000,
                        "cumulative_invested": 60000,
                        "future_value": 67200.00
                    }
                ]
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = Field(default="error", description="Response status")
    message: str = Field(description="Error message")
    errors: List[dict] = Field(default=[], description="Detailed errors")
