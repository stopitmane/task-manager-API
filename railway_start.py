#!/usr/bin/env python3
"""
Railway startup script for Task Management System API.
"""

import os
import uvicorn
from app.main import app

def main():
    """Start the application with Railway configuration."""
    # Get port from Railway environment variable
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting Task Management System API on port {port}")
    print(f"📊 Environment: PORT={port}")
    
    # Start the application
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False
    )

if __name__ == "__main__":
    main() 