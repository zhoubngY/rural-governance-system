from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.policy import Policy
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyInDB

# 关键：redirect_slashes=False 禁止自动重定向
router = APIRouter(prefix="/policies", tags=["policies"], redirect_slashes=False)

@router.get("", response_model=List[PolicyInDB])   # 注意路径为 "" 而不是 "/"
async def list_policies(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    result = await db.execute(select(Policy).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{policy_id}", response_model=PolicyInDB)
async def get_policy(
    policy_id: int,
    db: AsyncSession = Depends(get_db),
):
    policy = await db.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@router.post("", response_model=PolicyInDB, status_code=201)   # 注意路径为 ""
async def create_policy(
    policy_in: PolicyCreate,
    db: AsyncSession = Depends(get_db),
):
    policy = Policy(**policy_in.dict())
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    return policy

@router.put("/{policy_id}", response_model=PolicyInDB)
async def update_policy(
    policy_id: int,
    policy_in: PolicyUpdate,
    db: AsyncSession = Depends(get_db),
):
    policy = await db.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    for key, value in policy_in.dict(exclude_unset=True).items():
        setattr(policy, key, value)
    await db.commit()
    await db.refresh(policy)
    return policy

@router.delete("/{policy_id}", status_code=204)
async def delete_policy(
    policy_id: int,
    db: AsyncSession = Depends(get_db),
):
    policy = await db.get(Policy, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    await db.delete(policy)
    await db.commit()