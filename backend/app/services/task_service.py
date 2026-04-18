from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.task_crud import task_crud
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate
from app.models.user import User
from fastapi import HTTPException, status
from datetime import datetime

class TaskService:
    async def create(self, db: AsyncSession, *, obj_in: TaskCreate, creator: User) -> Task:
        task_data = obj_in.dict()
        task_data["creator_id"] = creator.id
        task_data["status"] = TaskStatus.PENDING
        return await task_crud.create(db, obj_in=task_data)

    async def assign(self, db: AsyncSession, *, task_id: int, assignee_id: int, assigner: User) -> Task:
        task = await task_crud.get(db, id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.status != TaskStatus.PENDING:
            raise HTTPException(status_code=400, detail="Task cannot be assigned")
        # 简单校验，实际应检查assignee是否存在
        task.assignee_id = assignee_id
        task.assigned_by_id = assigner.id
        task.status = TaskStatus.ASSIGNED
        task.assigned_at = datetime.utcnow()
        await db.commit()
        await db.refresh(task)
        return task

    async def start_process(self, db: AsyncSession, *, task_id: int, worker: User) -> Task:
        task = await task_crud.get(db, id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.assignee_id != worker.id:
            raise HTTPException(status_code=403, detail="Not assigned to you")
        if task.status != TaskStatus.ASSIGNED:
            raise HTTPException(status_code=400, detail="Task not in assigned state")
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.utcnow()
        await db.commit()
        await db.refresh(task)
        return task

    async def complete(self, db: AsyncSession, *, task_id: int, worker: User, result_note: str = None) -> Task:
        task = await task_crud.get(db, id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.assignee_id != worker.id:
            raise HTTPException(status_code=403, detail="Not assigned to you")
        if task.status != TaskStatus.IN_PROGRESS:
            raise HTTPException(status_code=400, detail="Task not in progress")
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        task.result_note = result_note
        await db.commit()
        await db.refresh(task)
        return task

    async def get_by_creator(self, db: AsyncSession, *, creator_id: int):
        result = await db.execute(select(Task).where(Task.creator_id == creator_id))
        return result.scalars().all()

    async def get_by_assignee(self, db: AsyncSession, *, assignee_id: int):
        result = await db.execute(select(Task).where(Task.assignee_id == assignee_id))
        return result.scalars().all()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100):
        return await task_crud.get_multi(db, skip=skip, limit=limit)

task_service = TaskService()
