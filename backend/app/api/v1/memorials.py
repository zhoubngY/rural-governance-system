from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.memorial import Memorial
from app.schemas.memorial import MemorialCreate, MemorialUpdate, MemorialResponse

router = APIRouter(prefix="/memorials", tags=["大事记"], redirect_slashes=False)

@router.get("", response_model=List[MemorialResponse])
async def list_memorials(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    result = await db.execute(select(Memorial).order_by(Memorial.happened_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("", response_model=MemorialResponse, status_code=201)
async def create_memorial(data: MemorialCreate, db: AsyncSession = Depends(get_db)):
    memorial = Memorial(**data.dict())
    db.add(memorial)
    await db.commit()
    await db.refresh(memorial)
    return memorial

@router.put("/{memorial_id}", response_model=MemorialResponse)
async def update_memorial(memorial_id: int, data: MemorialUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Memorial).where(Memorial.id == memorial_id))
    memorial = result.scalar_one_or_none()
    if not memorial:
        raise HTTPException(404, "大事记不存在")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(memorial, k, v)
    await db.commit()
    await db.refresh(memorial)
    return memorial

@router.delete("/{memorial_id}")
async def delete_memorial(memorial_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Memorial).where(Memorial.id == memorial_id))
    memorial = result.scalar_one_or_none()
    if not memorial:
        raise HTTPException(404, "不存在")
    await db.delete(memorial)
    await db.commit()
    return {"ok": True}