from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.consultation import Consultation
from app.schemas.consultation import ConsultationCreate, ConsultationResponse
from app.api.v1.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/consultations", tags=["在线咨询"], redirect_slashes=False)

@router.post("", response_model=ConsultationResponse, status_code=201)
async def ask_question(data: ConsultationCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    consult = Consultation(user_id=user.id, question=data.question)
    db.add(consult)
    await db.commit()
    await db.refresh(consult)
    return consult

@router.get("/my", response_model=List[ConsultationResponse])
async def my_consultations(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Consultation).where(Consultation.user_id == user.id).order_by(Consultation.created_at.desc()))
    return result.scalars().all()

@router.get("/admin", response_model=List[ConsultationResponse])
async def admin_list_consultations(db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin_user)):
    result = await db.execute(select(Consultation).order_by(Consultation.created_at.desc()))
    return result.scalars().all()

@router.put("/{consult_id}/answer")
async def answer_question(consult_id: int, data: dict, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin_user)):
    result = await db.execute(select(Consultation).where(Consultation.id == consult_id))
    consult = result.scalar_one_or_none()
    if not consult:
        raise HTTPException(404, "咨询不存在")
    consult.answer = data.get("answer")
    consult.status = "answered"
    await db.commit()
    return {"ok": True}