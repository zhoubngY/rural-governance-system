from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.core.database import get_db
from app.models.notice import Notice
from app.schemas.notice import NoticeCreate, NoticeUpdate, NoticeResponse

router = APIRouter(prefix="/notices", tags=["notices"], redirect_slashes=False)

@router.get("", response_model=List[NoticeResponse])
async def list_notices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Notice).order_by(Notice.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{notice_id}", response_model=NoticeResponse)
async def get_notice(
    notice_id: int,
    db: AsyncSession = Depends(get_db),
):
    notice = await db.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@router.post("", response_model=NoticeResponse, status_code=201)
async def create_notice(
    notice_in: NoticeCreate,
    db: AsyncSession = Depends(get_db),
):
    notice = Notice(**notice_in.dict())
    db.add(notice)
    await db.commit()
    await db.refresh(notice)
    return notice

@router.put("/{notice_id}", response_model=NoticeResponse)
async def update_notice(
    notice_id: int,
    notice_in: NoticeUpdate,
    db: AsyncSession = Depends(get_db),
):
    notice = await db.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    for key, value in notice_in.dict(exclude_unset=True).items():
        setattr(notice, key, value)
    await db.commit()
    await db.refresh(notice)
    return notice

@router.delete("/{notice_id}", status_code=204)
async def delete_notice(
    notice_id: int,
    db: AsyncSession = Depends(get_db),
):
    notice = await db.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    await db.delete(notice)
    await db.commit()