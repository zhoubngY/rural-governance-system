from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, RoleChecker
from app.services.task_service import task_service
from app.schemas.task import TaskCreate, TaskInDB, TaskAssign, TaskUpdate
from app.models.user import User
from app.models.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])

async def enrich_tasks_with_usernames(db: AsyncSession, tasks: List[Task]) -> List[Task]:
    user_ids = set()
    for t in tasks:
        # 只使用 creator_id (因为 assignee_id 已废弃)
        user_ids.add(t.creator_id)
        # 从 extra_data 中提取 assignee_ids 来获取负责人姓名（可选，暂不实现）
    if not user_ids:
        return tasks
    result = await db.execute(select(User).where(User.id.in_(user_ids)))
    users = {u.id: u for u in result.scalars().all()}
    for t in tasks:
        t.creator_name = users[t.creator_id].real_name if t.creator_id in users else None
        t.assignee_name = None  # 暂时不处理多负责人显示
    return tasks

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
        # 注意：原逻辑使用了 assignee_id，现在改为从 extra_data 中查找，但为了快速恢复，暂时只返回创建的任务
        tasks = await task_service.get_by_creator(db, creator_id=current_user.id)
    else:
        tasks = await task_service.get_multi(db)
    tasks = await enrich_tasks_with_usernames(db, tasks)
    return tasks

@router.get("/{task_id}", response_model=TaskInDB)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = await task_service.get_one(db, task_id=task_id)
    if current_user.role == "admin":
        pass
    elif current_user.role == "staff":
        # 临时：只允许创建者查看
        if task.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    elif current_user.role == "villager" and task.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    tasks = await enrich_tasks_with_usernames(db, [task])
    return tasks[0]

@router.put("/{task_id}", response_model=TaskInDB)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin", "staff"]))
):
    task = await task_service.update_task(db, task_id=task_id, obj_in=task_in, user=current_user)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin", "staff"]))
):
    await task_service.delete_task(db, task_id=task_id, user=current_user)