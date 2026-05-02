from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.core.database import get_db
from app.models.guide import Guide
from app.schemas.guide import GuideCreate, GuideUpdate, GuideResponse

router = APIRouter(prefix="/guides", tags=["guides"], redirect_slashes=False)

@router.get("", response_model=List[GuideResponse])
async def list_guides(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Guide).order_by(Guide.order.asc()))
    return result.scalars().all()

@router.get("/{guide_id}", response_model=GuideResponse)
async def get_guide(
    guide_id: int,
    db: AsyncSession = Depends(get_db),
):
    guide = await db.get(Guide, guide_id)
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")
    return guide

@router.post("", response_model=GuideResponse, status_code=201)
async def create_guide(
    guide_in: GuideCreate,
    db: AsyncSession = Depends(get_db),
):
    guide = Guide(**guide_in.dict())
    db.add(guide)
    await db.commit()
    await db.refresh(guide)
    return guide

@router.put("/{guide_id}", response_model=GuideResponse)
async def update_guide(
    guide_id: int,
    guide_in: GuideUpdate,
    db: AsyncSession = Depends(get_db),
):
    guide = await db.get(Guide, guide_id)
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")
    for key, value in guide_in.dict(exclude_unset=True).items():
        setattr(guide, key, value)
    await db.commit()
    await db.refresh(guide)
    return guide

@router.delete("/{guide_id}", status_code=204)
async def delete_guide(
    guide_id: int,
    db: AsyncSession = Depends(get_db),
):
    guide = await db.get(Guide, guide_id)
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")
    await db.delete(guide)
    await db.commit()