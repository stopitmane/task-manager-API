#!/usr/bin/env python3
"""
Test runner script for the Task Management System API.
"""

import pytest
import sys
import os

def main():
    """Run the test suite."""
    # Add the current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Run pytest with verbose output
    args = [
        "tests/",
        "-v",
        "--tb=short",
        "--strict-markers",
        "--disable-warnings"
    ]
    
    # Add coverage if available
    try:
        import coverage
        args.extend(["--cov=app", "--cov-report=term-missing"])
    except ImportError:
        print("Coverage not available. Install with: pip install coverage")
    
    return pytest.main(args)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 