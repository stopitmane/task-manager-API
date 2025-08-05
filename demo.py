#!/usr/bin/env python3
"""
Demo script to showcase the Task Management System API.
This script demonstrates the main features of the API.
"""

import requests
import json
import time
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8001"

def print_response(response, title=""):
    """Print API response in a formatted way."""
    print(f"\n{'='*50}")
    if title:
        print(f"📋 {title}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"{'='*50}")

def demo_api():
    """Run the API demo."""
    print("🚀 Task Management System API Demo")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    
    # Test 2: API Info
    print("\n2️⃣ Getting API Information...")
    response = requests.get(f"{BASE_URL}/info")
    print_response(response, "API Information")
    
    # Test 3: Register User
    print("\n3️⃣ Registering a new user...")
    user_data = {
        "username": "demo_user",
        "email": "demo@example.com",
        "password": "demo_password_123"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print_response(response, "User Registration")
    
    if response.status_code != 200:
        print("❌ User registration failed. Exiting demo.")
        return
    
    # Test 4: Login
    print("\n4️⃣ Logging in...")
    login_data = {
        "username": "demo_user",
        "password": "demo_password_123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print_response(response, "User Login")
    
    if response.status_code != 200:
        print("❌ Login failed. Exiting demo.")
        return
    
    # Get access token
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 5: Get Current User
    print("\n5️⃣ Getting current user information...")
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print_response(response, "Current User")
    
    # Test 6: Create Tasks
    print("\n6️⃣ Creating sample tasks...")
    tasks_data = [
        {
            "title": "Complete project documentation",
            "description": "Write comprehensive documentation for the portfolio project",
            "priority": "high",
            "status": "pending"
        },
        {
            "title": "Set up development environment",
            "description": "Install all required dependencies and configure the development setup",
            "priority": "medium",
            "status": "completed"
        },
        {
            "title": "Write unit tests",
            "description": "Create comprehensive test suite for all API endpoints",
            "priority": "high",
            "status": "in_progress"
        },
        {
            "title": "Deploy to production",
            "description": "Deploy the application to a production environment",
            "priority": "low",
            "status": "pending"
        }
    ]
    
    created_tasks = []
    for i, task_data in enumerate(tasks_data, 1):
        response = requests.post(f"{BASE_URL}/tasks/", json=task_data, headers=headers)
        print_response(response, f"Created Task {i}")
        if response.status_code == 200:
            created_tasks.append(response.json())
    
    # Test 7: Get All Tasks
    print("\n7️⃣ Getting all tasks...")
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print_response(response, "All Tasks")
    
    # Test 8: Get Tasks by Status
    print("\n8️⃣ Getting tasks by status...")
    for status in ["pending", "in_progress", "completed"]:
        response = requests.get(f"{BASE_URL}/tasks/status/{status}", headers=headers)
        print_response(response, f"Tasks with Status: {status}")
    
    # Test 9: Get Tasks by Priority
    print("\n9️⃣ Getting tasks by priority...")
    for priority in ["low", "medium", "high"]:
        response = requests.get(f"{BASE_URL}/tasks/priority/{priority}", headers=headers)
        print_response(response, f"Tasks with Priority: {priority}")
    
    # Test 10: Update a Task
    if created_tasks:
        print("\n🔟 Updating a task...")
        task_id = created_tasks[0]["id"]
        update_data = {
            "title": "Updated: Complete project documentation",
            "status": "in_progress",
            "priority": "high"
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data, headers=headers)
        print_response(response, "Updated Task")
    
    # Test 11: Get Specific Task
    if created_tasks:
        print("\n1️⃣1️⃣ Getting a specific task...")
        task_id = created_tasks[0]["id"]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        print_response(response, "Specific Task")
    
    # Test 12: Delete a Task
    if len(created_tasks) > 1:
        print("\n1️⃣2️⃣ Deleting a task...")
        task_id = created_tasks[1]["id"]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        print_response(response, "Deleted Task")
        
        # Verify deletion
        response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        print_response(response, "Verifying Task Deletion (should be 404)")
    
    print("\n🎉 Demo completed successfully!")
    print("\n📚 You can also visit:")
    print(f"   - API Documentation: {BASE_URL}/docs")
    print(f"   - Alternative Docs: {BASE_URL}/redoc")

if __name__ == "__main__":
    try:
        demo_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("   Make sure the server is running with: python run.py")
    except Exception as e:
        print(f"❌ An error occurred: {e}") 