from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.core.database import get_db
from app.models.note import WorkNote
from app.schemas.note import NoteCreate, NoteUpdate, NoteInDB

router = APIRouter(prefix="/notes", tags=["notes"])

# 临时：固定用户 ID = 1（admin），确保开发环境下所有操作可用
FIXED_USER_ID = 1

@router.post("/", response_model=NoteInDB, status_code=201)
async def create_note(
    note_in: NoteCreate,
    db: AsyncSession = Depends(get_db),
):
    note = WorkNote(**note_in.dict(), user_id=FIXED_USER_ID)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note

@router.get("/", response_model=List[NoteInDB])
async def list_notes(
    type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(WorkNote).where(WorkNote.user_id == FIXED_USER_ID)
    if type:
        query = query.where(WorkNote.type == type)
    query = query.order_by(WorkNote.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    notes = result.scalars().all()
    return notes

@router.get("/{note_id}", response_model=NoteInDB)
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(WorkNote, note_id)
    if not note or note.user_id != FIXED_USER_ID:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteInDB)
async def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(WorkNote, note_id)
    if not note or note.user_id != FIXED_USER_ID:
        raise HTTPException(status_code=404, detail="Note not found")
    update_data = note_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)
    await db.commit()
    await db.refresh(note)
    return note

@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
):
    note = await db.get(WorkNote, note_id)
    if not note or note.user_id != FIXED_USER_ID:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.delete(note)
    await db.commit()