#!/usr/bin/env python3
"""
Deployment script for Railway.
"""

import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    print(f"🚀 Starting Task Management System API on {host}:{port}")
    
    # Start the application
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False  # Disable reload in production
    ) 