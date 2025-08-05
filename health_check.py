#!/usr/bin/env python3
"""
Health check script for Railway deployment.
"""

import os
import sys
import requests
import time

def health_check():
    """Check if the application is running."""
    try:
        # Get the port from environment
        port = os.environ.get("PORT", "8000")
        url = f"http://localhost:{port}/health"
        
        print(f"🔍 Checking health at: {url}")
        
        # Wait a moment for the app to start
        time.sleep(2)
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"📊 Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1) 