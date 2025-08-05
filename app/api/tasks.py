from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import crud, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    
    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **priority**: Task priority (low, medium, high) - defaults to medium
    - **status**: Task status (pending, in_progress, completed) - defaults to pending
    - **due_date**: Task due date (optional)
    """
    return crud.create_task(db=db, task=task, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of tasks to return"),
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all tasks for the current user.
    
    - **skip**: Number of tasks to skip (for pagination)
    - **limit**: Maximum number of tasks to return (max 100)
    """
    tasks = crud.get_tasks(db, user_id=current_user.id, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
    task_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID.
    
    - **task_id**: ID of the task to retrieve
    """
    task = crud.get_task(db, task_id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a specific task.
    
    - **task_id**: ID of the task to update
    - **task_update**: Task data to update (only provided fields will be updated)
    """
    task = crud.update_task(db, task_id=task_id, task_update=task_update, user_id=current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific task.
    
    - **task_id**: ID of the task to delete
    """
    success = crud.delete_task(db, task_id=task_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}

@router.get("/status/{status}", response_model=List[schemas.Task])
def read_tasks_by_status(
    status: str,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get tasks by status.
    
    - **status**: Task status (pending, in_progress, completed)
    """
    try:
        status_enum = crud.models.StatusEnum(status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status. Must be one of: pending, in_progress, completed"
        )
    
    tasks = crud.get_tasks_by_status(db, user_id=current_user.id, status=status_enum)
    return tasks

@router.get("/priority/{priority}", response_model=List[schemas.Task])
def read_tasks_by_priority(
    priority: str,
    current_user: schemas.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get tasks by priority.
    
    - **priority**: Task priority (low, medium, high)
    """
    try:
        priority_enum = crud.models.PriorityEnum(priority)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid priority. Must be one of: low, medium, high"
        )
    
    tasks = crud.get_tasks_by_priority(db, user_id=current_user.id, priority=priority_enum)
    return tasks 