#!/usr/bin/env python3
"""
Simple script to run the Task Management System API.
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    from app.main import get_port
    
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=get_port(),
        reload=os.getenv("DEBUG", "True").lower() == "true"
    ) 