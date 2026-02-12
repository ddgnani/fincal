"""
FastAPI application for SIP Calculator (Local Development)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from api.models.sip import (
    SIPCalculationRequest,
    SIPCalculationResponse,
    ErrorResponse
)
from api.services.sip_calculator import calculate_sip_with_annual_compounding

# Initialize FastAPI app
app = FastAPI(
    title="Investment Growth Calculator API",
    description="API for calculating SIP investment returns with compound interest",
    version="1.0.0"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # React default
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Investment Growth Calculator API",
        "version": "1.0.0",
        "endpoints": {
            "calculate_sip": "/api/calculate-sip"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post(
    "/api/calculate-sip",
    response_model=SIPCalculationResponse,
    responses={
        200: {
            "description": "Successful calculation",
            "model": SIPCalculationResponse
        },
        400: {
            "description": "Validation error",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
def calculate_sip(request: SIPCalculationRequest):
    """
    Calculate SIP investment returns with annual compounding

    This endpoint accepts monthly investment amount, time period, and expected
    annual return rate, then calculates the future value with year-by-year breakdown.

    Args:
        request: SIPCalculationRequest with required parameters

    Returns:
        SIPCalculationResponse with calculation results and yearly breakdown

    Raises:
        HTTPException: For validation errors or calculation failures
    """
    try:
        # Perform calculation
        result = calculate_sip_with_annual_compounding(request)
        return result

    except ValidationError as e:
        # Handle Pydantic validation errors
        error_details = []
        for error in e.errors():
            error_details.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"]
            })

        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "Validation error",
                "errors": error_details
            }
        )

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Internal server error: {str(e)}",
                "errors": []
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
