from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, RoleChecker
from app.crud.policy_crud import policy_crud
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyInDB
from app.models.user import User

router = APIRouter(prefix="/policy", tags=["policy"])

@router.get("/", response_model=List[PolicyInDB])
async def list_policies(db: AsyncSession = Depends(get_db)):
    return await policy_crud.get_multi(db)

@router.post("/", response_model=PolicyInDB)
async def create_policy(
    policy_in: PolicyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin"]))
):
    return await policy_crud.create(db, obj_in=policy_in)

@router.put("/{policy_id}", response_model=PolicyInDB)
async def update_policy(
    policy_id: int,
    policy_in: PolicyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin"]))
):
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return await policy_crud.update(db, db_obj=policy, obj_in=policy_in)

@router.delete("/{policy_id}", response_model=PolicyInDB)
async def delete_policy(
    policy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin"]))
):
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return await policy_crud.remove(db, id=policy_id)
