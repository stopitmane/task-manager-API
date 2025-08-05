#!/usr/bin/env python3
"""
Startup script for the Task Management System API.
Handles environment variables and port configuration.
"""

import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Start the FastAPI application."""
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    print(f"Starting Task Management System API on {host}:{port}")
    
    # Start the application
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False  # Disable reload in production
    )

if __name__ == "__main__":
    main() 