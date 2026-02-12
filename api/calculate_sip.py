"""
Vercel Serverless Function for SIP Calculator
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.sip import SIPCalculationRequest
from services.sip_calculator import calculate_sip_with_annual_compounding


class handler(BaseHTTPRequestHandler):
    """Handler for Vercel serverless function"""

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests for SIP calculation"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            # Validate and process request
            request = SIPCalculationRequest(**data)
            result = calculate_sip_with_annual_compounding(request)

            # Convert Pydantic model to dict
            response_data = result.model_dump()

            # Send successful response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response_json = json.dumps(response_data)
            self.wfile.write(response_json.encode('utf-8'))

        except ValueError as e:
            # Handle validation errors
            self.send_error_response(400, f"Validation error: {str(e)}")

        except Exception as e:
            # Handle unexpected errors
            self.send_error_response(500, f"Internal server error: {str(e)}")

    def send_error_response(self, status_code, message):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        error_response = {
            "status": "error",
            "message": message,
            "errors": []
        }

        self.wfile.write(json.dumps(error_response).encode('utf-8'))
