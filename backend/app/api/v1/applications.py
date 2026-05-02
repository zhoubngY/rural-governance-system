from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from app.api.v1.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/applications", tags=["村民申请"], redirect_slashes=False)

@router.post("", response_model=ApplicationResponse, status_code=201)
async def create_application(data: ApplicationCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    app = Application(user_id=user.id, type=data.type, content=data.content, status="pending")
    db.add(app)
    await db.commit()
    await db.refresh(app)
    return app

@router.get("/my", response_model=List[ApplicationResponse])
async def my_applications(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Application).where(Application.user_id == user.id).order_by(Application.created_at.desc()))
    return result.scalars().all()

@router.get("/admin", response_model=List[ApplicationResponse])
async def admin_list_applications(db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin_user)):
    result = await db.execute(select(Application).order_by(Application.created_at.desc()))
    return result.scalars().all()

@router.put("/{app_id}/review")
async def review_application(app_id: int, data: ApplicationUpdate, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin_user)):
    result = await db.execute(select(Application).where(Application.id == app_id))
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(404, "申请不存在")
    app.status = data.status
    app.admin_reply = data.admin_reply
    await db.commit()
    return {"ok": True}