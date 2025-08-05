from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from . import models, schemas
from .auth import get_password_hash

# User CRUD operations
def get_user(db: Session, user_id: int):
    """Get a user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Get a user by username."""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Get a user by email."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users with pagination."""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Task CRUD operations
def get_task(db: Session, task_id: int, user_id: int):
    """Get a task by ID for a specific user."""
    return db.query(models.Task).filter(
        and_(models.Task.id == task_id, models.Task.owner_id == user_id)
    ).first()

def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all tasks for a specific user with pagination."""
    return db.query(models.Task).filter(
        models.Task.owner_id == user_id
    ).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    """Create a new task for a user."""
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, user_id: int):
    """Update a task for a specific user."""
    db_task = get_task(db, task_id=task_id, user_id=user_id)
    if not db_task:
        return None
    
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    """Delete a task for a specific user."""
    db_task = get_task(db, task_id=task_id, user_id=user_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True

def get_tasks_by_status(db: Session, user_id: int, status: models.StatusEnum):
    """Get tasks by status for a specific user."""
    return db.query(models.Task).filter(
        and_(models.Task.owner_id == user_id, models.Task.status == status)
    ).all()

def get_tasks_by_priority(db: Session, user_id: int, priority: models.PriorityEnum):
    """Get tasks by priority for a specific user."""
    return db.query(models.Task).filter(
        and_(models.Task.owner_id == user_id, models.Task.priority == priority)
    ).all() 