import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from app.main import app
from app.database import get_db, Base

# Create in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and clean up after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_headers():
    """Create authenticated user and return headers."""
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_task_success(auth_headers):
    """Test successful task creation."""
    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "high",
            "status": "pending"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["priority"] == "high"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data

def test_create_task_minimal(auth_headers):
    """Test task creation with minimal data."""
    response = client.post(
        "/tasks/",
        json={"title": "Minimal Task"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["priority"] == "medium"  # default
    assert data["status"] == "pending"   # default

def test_create_task_unauthorized():
    """Test task creation without authentication."""
    response = client.post(
        "/tasks/",
        json={"title": "Test Task"}
    )
    assert response.status_code == 401

def test_get_tasks_empty(auth_headers):
    """Test getting tasks when user has no tasks."""
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_get_tasks_with_data(auth_headers):
    """Test getting tasks when user has tasks."""
    # Create a task
    client.post(
        "/tasks/",
        json={"title": "Test Task"},
        headers=auth_headers
    )
    
    # Get tasks
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Task"

def test_get_task_by_id(auth_headers):
    """Test getting a specific task by ID."""
    # Create a task
    create_response = client.post(
        "/tasks/",
        json={"title": "Test Task"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"

def test_get_task_not_found(auth_headers):
    """Test getting a non-existent task."""
    response = client.get("/tasks/999", headers=auth_headers)
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_update_task_success(auth_headers):
    """Test successful task update."""
    # Create a task
    create_response = client.post(
        "/tasks/",
        json={"title": "Original Title"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Update the task
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated Title",
            "status": "in_progress",
            "priority": "high"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"

def test_update_task_not_found(auth_headers):
    """Test updating a non-existent task."""
    response = client.put(
        "/tasks/999",
        json={"title": "Updated Title"},
        headers=auth_headers
    )
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_delete_task_success(auth_headers):
    """Test successful task deletion."""
    # Create a task
    create_response = client.post(
        "/tasks/",
        json={"title": "Task to Delete"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"
    
    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_task_not_found(auth_headers):
    """Test deleting a non-existent task."""
    response = client.delete("/tasks/999", headers=auth_headers)
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_get_tasks_by_status(auth_headers):
    """Test getting tasks filtered by status."""
    # Create tasks with different statuses
    client.post(
        "/tasks/",
        json={"title": "Pending Task", "status": "pending"},
        headers=auth_headers
    )
    client.post(
        "/tasks/",
        json={"title": "In Progress Task", "status": "in_progress"},
        headers=auth_headers
    )
    client.post(
        "/tasks/",
        json={"title": "Completed Task", "status": "completed"},
        headers=auth_headers
    )
    
    # Get pending tasks
    response = client.get("/tasks/status/pending", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Pending Task"

def test_get_tasks_by_priority(auth_headers):
    """Test getting tasks filtered by priority."""
    # Create tasks with different priorities
    client.post(
        "/tasks/",
        json={"title": "Low Priority Task", "priority": "low"},
        headers=auth_headers
    )
    client.post(
        "/tasks/",
        json={"title": "High Priority Task", "priority": "high"},
        headers=auth_headers
    )
    
    # Get high priority tasks
    response = client.get("/tasks/priority/high", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "High Priority Task"

def test_get_tasks_invalid_status(auth_headers):
    """Test getting tasks with invalid status."""
    response = client.get("/tasks/status/invalid", headers=auth_headers)
    assert response.status_code == 400
    assert "Invalid status" in response.json()["detail"]

def test_get_tasks_invalid_priority(auth_headers):
    """Test getting tasks with invalid priority."""
    response = client.get("/tasks/priority/invalid", headers=auth_headers)
    assert response.status_code == 400
    assert "Invalid priority" in response.json()["detail"]

def test_task_isolation_between_users():
    """Test that users can only see their own tasks."""
    # Register two users
    client.post(
        "/auth/register",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "password123"
        }
    )
    client.post(
        "/auth/register",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        }
    )
    
    # Login as user1
    login1_response = client.post(
        "/auth/login",
        data={"username": "user1", "password": "password123"}
    )
    headers1 = {"Authorization": f"Bearer {login1_response.json()['access_token']}"}
    
    # Login as user2
    login2_response = client.post(
        "/auth/login",
        data={"username": "user2", "password": "password123"}
    )
    headers2 = {"Authorization": f"Bearer {login2_response.json()['access_token']}"}
    
    # Create task as user1
    task1_response = client.post(
        "/tasks/",
        json={"title": "User1 Task"},
        headers=headers1
    )
    task1_id = task1_response.json()["id"]
    
    # Create task as user2
    task2_response = client.post(
        "/tasks/",
        json={"title": "User2 Task"},
        headers=headers2
    )
    task2_id = task2_response.json()["id"]
    
    # User1 should only see their own task
    user1_tasks = client.get("/tasks/", headers=headers1)
    assert len(user1_tasks.json()) == 1
    assert user1_tasks.json()[0]["title"] == "User1 Task"
    
    # User2 should only see their own task
    user2_tasks = client.get("/tasks/", headers=headers2)
    assert len(user2_tasks.json()) == 1
    assert user2_tasks.json()[0]["title"] == "User2 Task"
    
    # User1 should not be able to access user2's task
    response = client.get(f"/tasks/{task2_id}", headers=headers1)
    assert response.status_code == 404 