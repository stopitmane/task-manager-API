#!/usr/bin/env python3
"""
Test script to verify deployment configuration.
"""

import os
import sys

def test_environment():
    """Test environment variables and configuration."""
    print("🔍 Testing deployment configuration...")
    
    # Test PORT environment variable
    port = os.getenv("PORT", "8000")
    print(f"✅ PORT: {port}")
    
    # Test other environment variables
    secret_key = os.getenv("SECRET_KEY", "not-set")
    database_url = os.getenv("DATABASE_URL", "not-set")
    
    print(f"✅ SECRET_KEY: {'set' if secret_key != 'not-set' else 'not-set'}")
    print(f"✅ DATABASE_URL: {database_url}")
    
    # Test imports
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        from app.main import app
        print("✅ App imported successfully")
    except ImportError as e:
        print(f"❌ App import failed: {e}")
        return False
    
    print("🎉 All tests passed! Deployment configuration is ready.")
    return True

if __name__ == "__main__":
    success = test_environment()
    sys.exit(0 if success else 1) 