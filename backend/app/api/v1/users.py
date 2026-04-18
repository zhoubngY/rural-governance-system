from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_password_hash, get_current_user, RoleChecker, verify_password
from app.crud.user_crud import user_crud
from app.schemas.user import UserCreate, UserCreatePublic, UserInDB, UserUpdate
from app.models.user import User
from pydantic import BaseModel
router = APIRouter(prefix="/users", tags=["users"])

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

class AdminPasswordReset(BaseModel):
    new_password: str

@router.post("/register", response_model=UserInDB)
async def register_public(user_in: UserCreatePublic, db: AsyncSession = Depends(get_db)):
    existing = await user_crud.get_by_username(db, username=user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_data = user_in.dict()
    user_data["role"] = "villager"
    user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    user = await user_crud.create(db, obj_in=user_data)
    return user

@router.post("/", response_model=UserInDB)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(RoleChecker(["admin"]))):
    existing = await user_crud.get_by_username(db, username=user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_data = user_in.dict()
    user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    user = await user_crud.create(db, obj_in=user_data)
    return user

@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserInDB])
async def read_users(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(RoleChecker(["admin", "staff"]))):
    return await user_crud.get_multi(db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin"]))
):
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # 禁止修改自己的角色以防止锁定
    if user_id == current_user.id and user_in.role and user_in.role != current_user.role:
        raise HTTPException(status_code=400, detail="Cannot change your own role")
    return await user_crud.update(db, db_obj=user, obj_in=user_in)

@router.delete("/{user_id}", response_model=UserInDB)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin"]))
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_crud.remove(db, id=user_id)
from pydantic import BaseModel

# 当前用户自助修改密码
@router.post("/me/password")
async def change_my_password(
    pw: PasswordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(pw.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    current_user.hashed_password = get_password_hash(pw.new_password)
    await db.commit()
    return {"message": "Password updated"}

# 管理员重置任意用户密码
@router.post("/{user_id}/reset-password")
async def reset_user_password(
    user_id: int,
    pw: AdminPasswordReset,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin"]))
):
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(pw.new_password)
    await db.commit()
    return {"message": f"Password reset for {user.username}"}


