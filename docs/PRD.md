# Product Requirements Document (PRD)
## Investment Growth Calculator App

---

## 1. Product Overview

### 1.1 Vision
A web-based investment calculator application that helps users understand the power of compound interest and plan their investments. The app will be developed incrementally, one feature at a time, starting with a SIP (Systematic Investment Plan) calculator.

### 1.2 Target Audience
- Individual investors planning systematic investments
- People learning about investment growth and compound interest
- Users who want to visualize their long-term investment potential

### 1.3 Core Principles
- **Simplicity First**: Start with essential features, no unnecessary complexity
- **Visual Clarity**: Use clear graphs to demonstrate investment growth
- **Incremental Development**: Build and validate one feature at a time
- **Local-First Development**: Test thoroughly on local machine → Git version control → GitHub push → Vercel deployment

---

## 2. Feature 1: SIP Monthly Calculator with Compound Interest

### 2.1 Feature Description
A calculator that computes the future value of a Systematic Investment Plan (SIP) where users invest a fixed amount monthly, with returns compounded over time.

### 2.2 User Inputs
The calculator will accept the following parameters:

| Input Field | Description | Data Type | Validation |
|------------|-------------|-----------|------------|
| Initial Investment Amount | One-time lump sum invested at the start | Number (decimal) | Must be >= 0, optional (default 0) |
| Monthly Investment Amount | Fixed amount to invest each month | Number (decimal) | Must be > 0 |
| Time Period | Investment duration in years | Number (integer) | Must be > 0, typically 1-50 years |
| Expected Annual Return Rate | Expected annual interest rate (%) | Number (decimal) | Must be >= 0, typically 1-30% |
| Annual Step-Up Rate | Percentage increase in monthly contribution each year | Number (decimal) | Must be >= 0, optional (default 0) |
| Step-Up Contribution Cap | Maximum monthly contribution amount after step-ups | Number (decimal) | Must be > 0, optional (no cap if omitted) |

**Note**: Compounding frequency is fixed to **annual** for this calculator.
**Note**: Dollar amounts are displayed in USD format with comma separators (e.g., $1,234,567.89).
**Note**: When Annual Step-Up Rate is 0 or omitted, the monthly contribution stays constant (original behavior). The Step-Up Contribution Cap is only relevant when a step-up rate is provided.

### 2.3 Calculation Logic

**Core Formula:**
- Future Value (FV) of SIP with annual compounding:
  ```
  FV = Initial × (1 + r)^n + P × 12 × [(1 + r)^n - 1] / r

  Where:
  Initial = One-time initial investment (default 0)
  P = Monthly investment amount
  r = Annual interest rate (as decimal, e.g., 12% = 0.12)
  n = Number of years
  ```

  This formula assumes:
  - All 12 monthly investments in a year are made at the beginning of the year
  - Interest is compounded once per year at the end of each year
  - Simplified calculation for easier understanding

**Alternative (More Accurate) Calculation:**
For month-by-month accuracy with annual compounding:
- Calculate each monthly investment's growth separately
- Each investment compounds based on how many complete years it stays invested
- Sum all individual future values

**Step-Up Contribution Logic:**

When an annual step-up rate is provided, the monthly contribution increases at the start of each new year:

```
For Year 1:
  monthly_contribution = P  (the original monthly investment)

For Year Y (Y > 1):
  monthly_contribution = min(
    previous_year_monthly × (1 + step_up_rate),
    step_up_cap   // if cap is provided
  )
```

Year-by-year calculation with step-up:
1. Year 1 uses the base monthly contribution `P`
2. At the start of Year 2, monthly contribution increases by the step-up rate
3. If a cap is set, the contribution never exceeds the cap amount
4. Each year's invested amount = `monthly_contribution_for_that_year × 12`
5. Compounding still occurs annually on the accumulated balance

**Additional Calculations:**
- Total Amount Invested = Initial Investment + Σ (monthly_contribution_year_i × 12) for each year
- Total Returns = Future Value - Total Amount Invested
- Returns Percentage = (Total Returns / Total Invested) × 100

### 2.4 Output Display

#### 2.4.1 Results Summary (Header Section)
Display prominently at the top:
- **Primary Message**: "In {X} years, you will have ${final_amount}"
- **Key Metrics**:
  - Total Investment: ${total_invested}
  - Future Value: ${future_value}
  - Total Returns: ${returns} (${returns_percentage}%)

#### 2.4.2 Visual Graph
A dual-line chart showing year-by-year progression:

**Chart Specifications:**
- **Chart Type**: Line chart with two series
- **X-Axis**: Years (Year 1, Year 2, ... Year N)
- **Y-Axis**: Amount in currency (with proper formatting, e.g., $1,000,000)
- **Line 1 (Red/Orange)**: Future Value with compound interest
  - Shows exponential growth curve
  - Should be clearly labeled as "Future Value (X%)"
- **Line 2 (Blue/Teal)**: Total Contributions (cumulative invested amount)
  - Shows linear growth
  - Should be clearly labeled as "Total Contributions"
- **Visual Gap**: The area between the two lines represents returns earned
- **Data Points**: Show dots on the lines for each year
- **Hover/Tooltip**: Display exact values when hovering over data points

**Chart Context:**
- Include explanatory text: "The chart below shows an estimate of how much your initial savings will grow over time, according to the interest rate and compounding schedule you specified."
- Include disclaimer: "Please remember that slight adjustments in any of those variables can affect the outcome. Use this calculator and provide different figures to show different scenarios."

#### 2.4.3 Optional: Year-by-Year Breakdown Table
A detailed table showing:
- Year number
- Amount invested that year
- Cumulative investment
- Interest earned that year
- Future value at end of year

*(This can be implemented in a later iteration if needed)*

### 2.5 User Flow
1. User lands on the SIP calculator page
2. User enters:
   - Initial investment amount (optional)
   - Monthly investment amount
   - Time period (years)
   - Expected annual return rate (%)
3. User clicks "Calculate" button
4. App displays:
   - Results summary with final amount
   - Dual-line growth chart
5. User can modify inputs and recalculate

### 2.6 Feature Constraints (V1)
- **No User Authentication**: No login/signup required
- **No Data Persistence**: Calculations are not saved
- **No History**: Previous calculations are not stored
- **Single Currency**: Display in USD ($ symbol) only
- **No Export**: Cannot export results to PDF/Excel (future feature)

---

## 3. Technical Architecture

### 3.1 Technology Stack

#### 3.1.1 Frontend
- **Framework**: React (latest stable version)
- **UI Library**: Material-UI or Tailwind CSS (for styling)
- **Charting Library**:
  - **Recommended**: Recharts (React-specific, simple, responsive)
  - Alternatives: Chart.js with react-chartjs-2, or Victory
- **Form Handling**: React Hook Form (for input validation)
- **HTTP Client**: Axios or Fetch API
- **Build Tool**: Vite or Create React App

#### 3.1.2 Backend
- **Framework**: FastAPI (Python 3.10+)
- **Deployment**: Vercel Serverless Functions (Python runtime)
- **Core Dependencies**:
  - `fastapi` - Web framework
  - `mangum` - ASGI adapter for AWS Lambda/Vercel
  - `pydantic` - Data validation
  - Built-in `math` module for calculations (no numpy needed for Vercel)
- **CORS**: Enable CORS for frontend-backend communication

#### 3.1.3 Development Tools
- **Version Control**: Git
- **Package Management**:
  - Frontend: npm or yarn
  - Backend: pip with requirements.txt or Poetry
- **Code Formatting**:
  - Frontend: Prettier, ESLint
  - Backend: Black, Flake8

### 3.2 System Architecture

```
┌─────────────────────────────────────────┐
│           React Frontend                │
│  ┌──────────────────────────────────┐  │
│  │  SIP Calculator Component        │  │
│  │  - Input Form                    │  │
│  │  - Results Display               │  │
│  │  - Graph Visualization           │  │
│  └──────────────────────────────────┘  │
│              │ HTTP POST                │
│              │ /api/calculate-sip       │
└──────────────┼──────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│         FastAPI Backend                  │
│  ┌───────────────────────────────────┐  │
│  │  API Endpoint                     │  │
│  │  POST /api/calculate-sip          │  │
│  └───────────┬───────────────────────┘  │
│              │                           │
│  ┌───────────▼───────────────────────┐  │
│  │  Calculation Engine (Python)      │  │
│  │  - SIP calculation logic          │  │
│  │  - Compound interest formula      │  │
│  │  - Year-by-year breakdown         │  │
│  └───────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

### 3.3 API Specification

#### Endpoint: Calculate SIP
- **URL**: `/api/calculate-sip`
- **Method**: `POST`
- **Content-Type**: `application/json`

**Request Body:**
```json
{
  "monthly_investment": 5000,
  "time_period_years": 10,
  "annual_return_rate": 12.0,
  "initial_investment": 0,
  "annual_step_up_rate": 10.0,
  "step_up_cap": 15000
}
```

**Response (Success - 200 OK):**
```json
{
  "status": "success",
  "inputs": {
    "monthly_investment": 5000,
    "time_period_years": 10,
    "annual_return_rate": 12.0,
    "initial_investment": 0,
    "annual_step_up_rate": 10.0,
    "step_up_cap": 15000,
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
      "monthly_contribution": 5000,
      "invested_this_year": 60000,
      "cumulative_invested": 60000,
      "future_value": 67200.00
    },
    {
      "year": 2,
      "monthly_contribution": 5500,
      "invested_this_year": 66000,
      "cumulative_invested": 126000,
      "future_value": 149184.00
    },
    {
      "year": 3,
      "monthly_contribution": 6050,
      "invested_this_year": 72600,
      "cumulative_invested": 198600,
      "future_value": 248686.08
    }
    // ... continues for all years
  ]
}
```

**Note**: Values are illustrative. Actual calculation depends on the formula implemented.

**Response (Error - 400 Bad Request):**
```json
{
  "status": "error",
  "message": "Validation error",
  "errors": [
    {
      "field": "monthly_investment",
      "message": "Must be greater than 0"
    }
  ]
}
```

### 3.4 Data Validation

#### Frontend Validation
- Check all fields are filled
- Ensure numeric inputs are valid numbers
- Show user-friendly error messages
- Disable submit until all inputs are valid

#### Backend Validation (Pydantic Models)
```python
class SIPCalculationRequest(BaseModel):
    monthly_investment: float = Field(gt=0, description="Monthly investment amount")
    time_period_years: int = Field(gt=0, le=50, description="Investment period in years")
    annual_return_rate: float = Field(ge=0, le=100, description="Expected annual return rate in percentage")
    initial_investment: float = Field(ge=0, default=0, description="One-time initial investment amount")
    annual_step_up_rate: float = Field(ge=0, default=0, description="Annual percentage increase in monthly contribution")
    step_up_cap: Optional[float] = Field(gt=0, default=None, description="Maximum monthly contribution after step-ups (no cap if omitted)")
```

### 3.5 Project Structure (Vercel Deployment)

```
fincal/
├── api/                            # Vercel serverless functions (Python)
│   ├── __init__.py
│   ├── calculate_sip.py           # API endpoint as serverless function
│   ├── models/
│   │   ├── __init__.py
│   │   └── sip.py                 # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── sip_calculator.py      # Core calculation logic
│
├── src/                            # React frontend
│   ├── components/
│   │   ├── SIPCalculator/
│   │   │   ├── SIPCalculator.jsx
│   │   │   ├── InputForm.jsx
│   │   │   ├── ResultsDisplay.jsx
│   │   │   └── GrowthChart.jsx
│   │   └── common/
│   ├── services/
│   │   └── api.js                 # API client
│   ├── utils/
│   │   └── formatters.js          # Number/currency formatting
│   ├── App.jsx
│   └── main.jsx
│
├── public/                         # Static assets
│
├── tests/                          # Backend tests
│   ├── __init__.py
│   └── test_sip_calculator.py
│
├── vercel.json                     # Vercel configuration
├── requirements.txt                # Python dependencies for serverless functions
├── package.json                    # Node dependencies for frontend
├── vite.config.js                  # Vite configuration
└── README.md                       # Project overview
```

**Key Structure Notes for Vercel:**
- `api/` folder: Contains Python serverless functions (auto-detected by Vercel)
- `src/` folder: React frontend source code
- `vercel.json`: Configuration for routing and serverless function settings
- Each `.py` file in `api/` becomes an API endpoint

---

## 4. Local Development Setup

### 4.1 Prerequisites
- Python 3.10+ installed
- Node.js 18+ and npm installed
- Git installed
- Code editor (VS Code recommended)

### 4.2 Local Project Initialization

**Step 1: Initialize Git Repository**
```bash
cd /Users/gnani/workspace/training-center/fincal
git init
echo "node_modules/" > .gitignore
echo "dist/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
git add .
git commit -m "Initial commit: Project structure"
```

**Step 2: Backend Local Development**

For local testing, we'll use FastAPI with uvicorn (simpler than Vercel serverless):

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# Run backend locally
uvicorn api.main:app --reload --port 8000
```

**Local Backend Structure** (for development):
```
api/
├── main.py              # FastAPI app for local development
├── calculate_sip.py     # Vercel serverless function (used later)
├── models/
└── services/
```

**Step 3: Frontend Local Development**
```bash
# Create React app with Vite
npm create vite@latest . -- --template react

# Install dependencies
npm install
npm install recharts axios react-hook-form

# Run frontend locally
npm run dev  # Runs on http://localhost:5173
```

**Step 4: Local Testing**
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:5173`
- Frontend calls backend at `http://localhost:8000/api/calculate-sip`

### 4.3 Environment Configuration

**For Local Development**:
- Frontend API URL: `http://localhost:8000`
- Backend CORS: Allow `http://localhost:5173`

**For Production (Vercel)**:
- Frontend API URL: `/api` (relative path, same domain)
- Backend CORS: Allow all origins or specific domain

### 4.4 Git Workflow
1. Develop and test locally
2. Commit changes to local git: `git add . && git commit -m "message"`
3. When ready for deployment: Push to GitHub
4. Deploy to Vercel from GitHub

---

## 5. Implementation Plan

### Phase 1: Backend Development (Local)
**Goal**: Implement the Python calculation engine and test locally with FastAPI

**Tasks**:
1. Initialize git repository and project structure
2. Set up Python virtual environment
3. Install dependencies: `fastapi`, `uvicorn`, `pydantic`, `pytest`
4. Create `api/` folder structure
5. Create Pydantic models in `api/models/sip.py`
   - `SIPCalculationRequest` model with validation
   - `SIPCalculationResponse` model
6. Implement core calculation logic in `api/services/sip_calculator.py`
   - Annual compound interest formula for monthly SIP
   - Year-by-year breakdown generation
   - Helper functions for formatting
7. Create FastAPI app in `api/main.py` for local development
   - POST endpoint `/api/calculate-sip`
   - CORS configuration for local frontend
   - Error handling
8. Write unit tests in `tests/test_sip_calculator.py`
9. Test locally with curl/Postman

**Critical Files**:
- `api/main.py` - FastAPI app for local development
- `api/services/sip_calculator.py` - Core calculation logic
- `api/models/sip.py` - Pydantic models
- `requirements.txt` - Python dependencies
- `tests/test_sip_calculator.py` - Unit tests

**Local Testing Commands**:
```bash
# Run backend
uvicorn api.main:app --reload --port 8000

# Run tests
pytest tests/

# Test API with curl
curl -X POST http://localhost:8000/api/calculate-sip \
  -H "Content-Type: application/json" \
  -d '{"monthly_investment": 5000, "time_period_years": 10, "annual_return_rate": 12.0}'
```

**Git Commit**:
```bash
git add api/ tests/ requirements.txt
git commit -m "feat: Add SIP calculator backend with annual compounding"
```

**Verification**:
- ✅ Backend runs without errors on http://localhost:8000
- ✅ All unit tests pass
- ✅ API returns correct calculations for sample inputs
- ✅ Input validation works (reject invalid inputs)
- ✅ CORS enabled for http://localhost:5173

---

### Phase 2: Frontend Development (Local)
**Goal**: Build the React UI and test locally with backend

**Tasks**:
1. Initialize React project with Vite: `npm create vite@latest . -- --template react`
2. Install dependencies:
   ```bash
   npm install recharts axios react-hook-form
   ```
3. Update `.gitignore` for frontend (already includes node_modules, dist)
4. Create folder structure: `src/components/`, `src/services/`, `src/utils/`
5. Create API service in `src/services/api.js`
   - Base URL: `http://localhost:8000` for local development
   - POST function to call `/api/calculate-sip`
   - Error handling
6. Create `src/components/SIPCalculator/InputForm.jsx`
   - Form fields: monthly investment, time period, annual return rate
   - React Hook Form for validation
   - Submit button with loading state
7. Create `src/components/SIPCalculator/ResultsDisplay.jsx`
   - Display future value, total invested, returns
   - Styled header matching reference image
   - Format currency with commas
8. Create `src/components/SIPCalculator/GrowthChart.jsx` using Recharts
   - Dual-line chart (Future Value vs Total Contributions)
   - Red/orange line for future value
   - Blue line for contributions
   - Year-by-year data points
   - Tooltips on hover
   - Styling to match reference image
9. Create `src/components/SIPCalculator/SIPCalculator.jsx`
   - Integrate InputForm, ResultsDisplay, GrowthChart
   - State management for calculation results
   - Loading and error states
10. Create `src/utils/formatters.js` for currency formatting
11. Update `src/App.jsx` to render SIPCalculator
12. Add basic styling (CSS or Tailwind)

**Critical Files**:
- `src/services/api.js` - API client
- `src/components/SIPCalculator/InputForm.jsx` - Input form
- `src/components/SIPCalculator/ResultsDisplay.jsx` - Results display
- `src/components/SIPCalculator/GrowthChart.jsx` - Chart visualization
- `src/components/SIPCalculator/SIPCalculator.jsx` - Main component
- `src/utils/formatters.js` - Utility functions

**Local Testing**:
```bash
# Ensure backend is running on port 8000
# In another terminal:
npm run dev  # Frontend runs on http://localhost:5173
```

**Git Commit**:
```bash
git add src/ package.json package-lock.json
git commit -m "feat: Add React frontend with SIP calculator UI"
```

**Verification**:
- ✅ Frontend runs without errors on http://localhost:5173
- ✅ Form validation works (empty fields, negative numbers)
- ✅ Can submit calculation and receive results from backend
- ✅ Results display correctly with formatted currency
- ✅ Chart renders with correct data (two lines, proper labels)
- ✅ Chart matches reference image style
- ✅ Responsive design works on mobile (test with browser DevTools)
- ✅ Loading spinner shows during API call
- ✅ Error messages display if API fails

---

### Phase 3: Local Integration & Testing
**Goal**: Final integration testing and polish on local machine

**Tasks**:
1. Start both backend and frontend locally
2. Full end-to-end testing:
   - Test with various input values (small, large, edge cases)
   - Test input validation (negative numbers, zero, empty fields)
   - Test with different time periods (1 year, 20 years, 50 years)
   - Test with different return rates (0%, 5%, 15%, 30%)
3. Polish UI:
   - Add explanatory text matching reference image
   - Add disclaimer about calculations
   - Fine-tune chart styling
   - Ensure proper spacing and layout
   - Add page title and favicon
4. Test responsive design:
   - Desktop (1920px, 1440px, 1024px)
   - Tablet (768px)
   - Mobile (375px, 414px)
5. Cross-browser testing (if possible):
   - Chrome
   - Firefox
   - Safari
6. Performance testing:
   - Check calculation speed
   - Check chart rendering speed
7. Code cleanup:
   - Remove console.logs
   - Add comments where needed
   - Format code consistently
8. Manual calculation verification:
   - Pick a few test cases
   - Verify results with manual calculation or Excel

**Git Commit**:
```bash
git add .
git commit -m "feat: Complete SIP calculator with testing and polish"
```

**Verification**:
- ✅ All features work correctly locally
- ✅ No errors in browser console
- ✅ No errors in backend terminal
- ✅ Calculations are mathematically accurate
- ✅ UI matches reference image design
- ✅ Responsive on all screen sizes
- ✅ Smooth user experience (fast, no bugs)
- ✅ Ready for production deployment

---

### Phase 4: GitHub Push & Vercel Deployment
**Goal**: Push code to GitHub and deploy to Vercel

**Tasks**:

**Part A: Prepare for Vercel Deployment**
1. Create `api/calculate_sip.py` - Vercel serverless function handler
   ```python
   from http.server import BaseHTTPRequestHandler
   import json
   from api.services.sip_calculator import calculate_sip_with_annual_compounding
   from api.models.sip import SIPCalculationRequest

   class handler(BaseHTTPRequestHandler):
       def do_POST(self):
           # Handle POST request
           # Parse body, call calculation, return JSON

       def do_OPTIONS(self):
           # Handle CORS preflight
   ```
2. Create `vercel.json` configuration:
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": "dist",
     "framework": "vite",
     "rewrites": [
       {
         "source": "/api/:path*",
         "destination": "/api/:path*"
       }
     ]
   }
   ```
3. Update `src/services/api.js` to use environment-aware URLs:
   ```javascript
   const API_BASE_URL = import.meta.env.PROD
     ? '/api'  // Production (Vercel)
     : 'http://localhost:8000/api'  // Local development
   ```
4. Update `requirements.txt` to include `mangum` if needed
5. Create `.env.example` file for documentation

**Part B: Push to GitHub**
```bash
# Create GitHub repository (via GitHub website or gh CLI)
gh repo create fincal --public --source=. --remote=origin

# Or manually add remote:
git remote add origin https://github.com/YOUR_USERNAME/fincal.git

# Push code
git branch -M main
git push -u origin main
```

**Part C: Deploy to Vercel**
1. Sign up/login to vercel.com
2. Click "New Project"
3. Import GitHub repository `fincal`
4. Vercel auto-detects React (Vite) and Python
5. Configure if needed (usually auto-detected correctly)
6. Click "Deploy"
7. Wait for deployment (~2-3 minutes)
8. Get deployment URL: `https://fincal.vercel.app`

**Part D: Test Production Deployment**
1. Visit deployed URL
2. Test full calculator functionality
3. Test on mobile device
4. Check browser console for errors
5. Verify API responses in Network tab
6. Test with multiple scenarios

**Critical Files Created**:
- `api/calculate_sip.py` - Serverless function handler
- `vercel.json` - Vercel configuration
- Updated `src/services/api.js` - Environment-aware API URLs

**Git Commits**:
```bash
git add vercel.json api/calculate_sip.py src/services/api.js
git commit -m "feat: Add Vercel deployment configuration"
git push
```

**Verification**:
- ✅ Code pushed to GitHub successfully
- ✅ Vercel deployment succeeds
- ✅ Production app works correctly at vercel.app URL
- ✅ All features work same as local
- ✅ API responses are fast (< 1 second)
- ✅ No errors in production
- ✅ Mobile responsive on actual mobile devices
- ✅ Share URL with others for testing

---

## 6. Future Features (Post-V1)

Features to be added in subsequent iterations:

1. **Goal-Based Planning** (reverse calculation: "I need $X, how much to invest?")
3. **Comparison Tool** (compare multiple scenarios side-by-side)
4. **Inflation Adjustment** (real returns vs nominal returns)
5. **User Authentication & Saved Calculations**
6. **Export to PDF/Excel**
7. **Historical Data Integration** (actual market returns)
8. **Mobile App** (React Native)
10. **Tax Calculations** (capital gains, tax-adjusted returns)

---

## 7. Success Metrics

For the SIP Calculator (V1), success will be measured by:

1. **Functionality**:
   - ✅ Calculator produces mathematically accurate results
   - ✅ All validations work correctly
   - ✅ Graph displays accurate data visualization

2. **User Experience**:
   - ✅ Simple, intuitive interface
   - ✅ Clear, easy-to-understand results
   - ✅ Responsive design works on mobile and desktop

3. **Technical**:
   - ✅ API response time < 500ms
   - ✅ No errors in console
   - ✅ Clean, maintainable code structure

---

## 8. Deployment on Vercel (Free Tier)

**Note**: This section is reference documentation for Phase 4 deployment. Complete Phases 1-3 locally first.

### 8.1 Why Vercel?
- **Unified Platform**: Deploy both frontend (React) and backend (Python serverless functions) together
- **Free Tier**: Generous limits for hobby projects
  - 100 GB bandwidth per month
  - Serverless function execution included
  - Automatic HTTPS
  - Global CDN
- **Zero Config**: Automatic detection of React and Python serverless functions
- **Git Integration**: Auto-deploy on push to main branch

### 8.2 Vercel Configuration

**vercel.json**:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/:path*"
    }
  ]
}
```

### 8.3 Python Serverless Function Structure

Each Python file in `/api` directory becomes an endpoint:
- `/api/calculate_sip.py` → `https://your-app.vercel.app/api/calculate_sip`

**Example: `api/calculate_sip.py`**:
```python
from http.server import BaseHTTPRequestHandler
import json
from api.services.sip_calculator import calculate_sip
from api.models.sip import SIPCalculationRequest

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        # Process calculation
        request = SIPCalculationRequest(**data)
        result = calculate_sip(request)

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
```

### 8.4 Deployment Steps

1. **Prerequisites**:
   - GitHub account
   - Vercel account (sign up at vercel.com with GitHub)
   - Project pushed to GitHub repository

2. **Deploy via Vercel Dashboard**:
   - Go to vercel.com/new
   - Import your GitHub repository
   - Vercel auto-detects React (Vite) and Python
   - Click "Deploy"
   - Done! App is live at `https://your-app.vercel.app`

3. **Deploy via Vercel CLI** (Alternative):
   ```bash
   npm install -g vercel
   vercel login
   vercel --prod
   ```

### 8.5 Environment Variables (if needed later)
- Set in Vercel Dashboard → Project Settings → Environment Variables
- Access in Python: `os.environ.get('VARIABLE_NAME')`

### 8.6 Free Tier Limits
- ✅ Unlimited deployments
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ 100 GB bandwidth/month
- ✅ Serverless functions: 100 GB-hours/month
- ⚠️ Serverless function timeout: 10 seconds (sufficient for calculations)
- ⚠️ Max serverless function size: 50 MB (more than enough)

### 8.7 Custom Domain (Optional)
- Add custom domain in Vercel Dashboard
- Update DNS records as instructed
- Automatic HTTPS certificate provisioning

---

## 9. Notes & Assumptions

- Currency is displayed in USD with $ symbol
- **Compounding**: Annual compounding (interest calculated once per year)
- **Investment Frequency**: Monthly (12 investments per year)
- Returns are shown pre-tax
- No consideration for fees or expense ratios in V1
- Graph shows year-by-year progression (not month-by-month)
- No authentication means no user tracking/analytics in V1
- **Deployment**: Entire app (frontend + backend) deployed on Vercel free tier
- **Step-Up Timing**: Annual step-up increases take effect at the start of each new year (Year 2 onward). Year 1 always uses the base monthly contribution.

---

**Document Version**: 1.4
**Last Updated**: 2026-02-12
**Status**: Ready for Development - Phase 1 (Backend Local Development)

### Changelog:
- v1.4: Added Step-Up SIP feature (annual contribution increase with optional cap); Updated Sections 2.2, 2.3, 3.3, 3.4, 9; Removed Step-Up SIP from future features; Added USD formatting note
- v1.3: Added optional initial investment amount (lump sum at time 0); Updated formula, API spec, validation, and user flow; Removed "Lump Sum Investment Calculator" from future features
- v1.2: Added local-first development workflow; Split implementation into 4 phases (local backend, local frontend, local integration, GitHub + Vercel deployment); Added comprehensive local development setup section
- v1.1: Updated compounding frequency to annual; Added Vercel deployment configuration
- v1.0: Initial PRD creation
