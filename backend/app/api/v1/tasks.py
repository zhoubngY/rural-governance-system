from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, RoleChecker
from app.services.task_service import task_service
from app.schemas.task import TaskCreate, TaskInDB, TaskAssign
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = await task_service.create(db, obj_in=task_in, creator=current_user)
    return task

@router.post("/{task_id}/assign", response_model=TaskInDB)
async def assign_task(
    task_id: int,
    assign_data: TaskAssign,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin", "staff"]))
):
    task = await task_service.assign(db, task_id=task_id, assignee_id=assign_data.assignee_id, assigner=current_user)
    return task

@router.post("/{task_id}/start", response_model=TaskInDB)
async def start_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["staff", "admin"]))
):
    task = await task_service.start_process(db, task_id=task_id, worker=current_user)
    return task

@router.post("/{task_id}/complete", response_model=TaskInDB)
async def complete_task(
    task_id: int,
    result_note: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["staff", "admin"]))
):
    task = await task_service.complete(db, task_id=task_id, worker=current_user, result_note=result_note)
    return task

@router.get("/", response_model=List[TaskInDB])
async def read_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "villager":
        tasks = await task_service.get_by_creator(db, creator_id=current_user.id)
    elif current_user.role == "staff":
        tasks = await task_service.get_by_assignee(db, assignee_id=current_user.id)
    else:
        tasks = await task_service.get_multi(db)
    return tasks
