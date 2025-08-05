from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text

from .database import engine, get_db
from . import models
from .api import auth, tasks

# Create database tables
def create_tables():
    models.Base.metadata.create_all(bind=engine)

# Startup event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_tables()
    yield

# Create FastAPI app
app = FastAPI(
    title="Task Management System API",
    description="A comprehensive task management system with user authentication and CRUD operations",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Task Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    try:
        # Test database connection
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/info")
async def api_info():
    """
    Get API information and available endpoints.
    """
    return {
        "name": "Task Management System API",
        "version": "1.0.0",
        "description": "A RESTful API for managing tasks with user authentication",
        "features": [
            "User registration and authentication",
            "JWT token-based security",
            "CRUD operations for tasks",
            "Task filtering by status and priority",
            "Pagination support",
            "Input validation",
            "Comprehensive error handling"
        ],
        "endpoints": {
            "authentication": {
                "POST /auth/register": "Register a new user",
                "POST /auth/login": "Login and get access token",
                "GET /auth/me": "Get current user info"
            },
            "tasks": {
                "GET /tasks/": "Get all tasks (paginated)",
                "POST /tasks/": "Create a new task",
                "GET /tasks/{task_id}": "Get a specific task",
                "PUT /tasks/{task_id}": "Update a task",
                "DELETE /tasks/{task_id}": "Delete a task",
                "GET /tasks/status/{status}": "Get tasks by status",
                "GET /tasks/priority/{priority}": "Get tasks by priority"
            }
        }
    } 