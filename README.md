# Investment Growth Calculator

A web-based SIP (Systematic Investment Plan) calculator that helps users understand the power of compound interest and plan their investments.

## Features

- **SIP Calculator**: Calculate future value of monthly investments with annual compounding
- **Visual Growth Chart**: Interactive dual-line chart showing investment growth over time
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Calculations**: Instant results with detailed year-by-year breakdown

## Tech Stack

### Frontend
- **React** - UI framework
- **Vite** - Build tool and dev server
- **Recharts** - Data visualization
- **React Hook Form** - Form validation
- **Axios** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **Pydantic** - Data validation
- **Vercel Serverless Functions** - Deployment platform

## Local Development

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd fincal
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Run backend server
   uvicorn api.main:app --reload --port 8000
   ```

3. **Frontend Setup**
   ```bash
   # Install dependencies
   npm install

   # Run development server
   npm run dev
   ```

4. **Access the app**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Deployment

The app is configured for deployment on Vercel:

1. Push code to GitHub
2. Connect repository to Vercel
3. Vercel auto-detects configuration and deploys

### Environment Variables
No environment variables required for basic functionality.

## Project Structure

```
fincal/
├── api/                        # Backend (Python/FastAPI)
│   ├── models/                # Pydantic models
│   ├── services/              # Business logic
│   ├── main.py               # FastAPI app (local dev)
│   └── calculate_sip.py      # Vercel serverless function
├── src/                       # Frontend (React)
│   ├── components/           # React components
│   ├── services/             # API client
│   └── utils/                # Helper functions
├── tests/                     # Backend tests
├── docs/                      # Documentation
└── public/                    # Static assets
```

## API Endpoint

### POST /api/calculate-sip

Calculate SIP investment returns with annual compounding.

**Request Body:**
```json
{
  "monthly_investment": 5000,
  "time_period_years": 10,
  "annual_return_rate": 12.0
}
```

**Response:**
```json
{
  "status": "success",
  "inputs": { ... },
  "results": {
    "future_value": 1052924.1,
    "total_invested": 600000.0,
    "total_returns": 452924.1,
    "returns_percentage": 75.49
  },
  "yearly_breakdown": [ ... ]
}
```

## Testing

### Backend Tests
```bash
pytest tests/ -v
```

### Manual Testing
1. Enter investment parameters in the form
2. Click "Calculate"
3. Verify results display correctly
4. Check chart renders with proper data

## Future Features

- Lump sum calculator
- Goal-based planning
- Comparison tool
- Inflation adjustment
- User authentication
- Export to PDF/Excel

## License

ISC

## Author

Built with Claude Code
