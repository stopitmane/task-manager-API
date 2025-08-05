#!/usr/bin/env python3
"""
Railway startup script for Task Management System API.
"""

import os
import sys
import uvicorn
from app.main import app

def main():
    """Start the application with Railway configuration."""
    try:
        # Get port from Railway environment variable with fallback
        port_str = os.environ.get("PORT", "8000")
        port = int(port_str)
        
        print(f"🚀 Starting Task Management System API on port {port}")
        print(f"📊 Environment: PORT={port}")
        print(f"🔧 Host: 0.0.0.0")
        
        # Start the application
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 