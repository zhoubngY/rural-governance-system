from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File, Response, Form
from fastapi.responses import StreamingResponse
from sqlalchemy import select, text, func
from sqlalchemy.ext.asyncio import AsyncSession
from io import BytesIO
import pandas as pd
import json
from openpyxl import Workbook
from typing import Optional, Dict, Any

from app.core.database import get_db
from app.core.security import get_current_user
from app.crud.note_crud import note_crud
from app.schemas.note import NoteCreate, NoteUpdate, NoteInDB, NoteListResponse
from app.models.note import WorkNote
from app.models.user import User

router = APIRouter(prefix="/notes", tags=["notes"])

# ---------- 租户切换（必须）----------
async def ensure_tenant_schema(db: AsyncSession):
    """确保当前会话在 tenant_1 schema 中操作"""
    await db.execute(text("SET search_path TO tenant_1"))
    await db.execute(text("SELECT 1"))

# ---------- 扩展字段映射 ----------
def get_extra_fields(note_type: str) -> Dict[str, str]:
    if note_type == "vehicle":
        return {"purpose": "用车事由", "driver": "驾驶人", "user": "用车人", "remark": "备注"}
    elif note_type == "engineering":
        return {"project_name": "工程名称", "contractor": "施工方", "contract_amount": "合同金额", "progress": "进度", "remark": "备注"}
    elif note_type == "labor":
        return {"reason": "用工事由", "workers": "用工人员", "wage_amount": "工资金额", "total": "合计"}
    elif note_type == "other":
        return {"description": "说明", "remark": "备注"}
    elif note_type == "memo":
        return {"item": "事项", "description": "说明", "remark": "备注"}
    else:
        return {}

# ---------- 创建笔记 ----------
@router.post("/", response_model=NoteInDB)
async def create_note(
    note_in: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await ensure_tenant_schema(db)
    if isinstance(note_in.type, str):
        note_in.type = note_in.type.lower()
    data = note_in.dict()
    data["user_id"] = current_user.id
    note = await note_crud.create(db, obj_in=data)
    await db.commit()
    return note

# ---------- 列表查询（分页 + 租户 + 权限）----------
@router.get("/", response_model=NoteListResponse)
async def list_notes(
    type: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await ensure_tenant_schema(db)

    query = select(WorkNote)
    if type:
        query = query.where(WorkNote.type == type.lower())

    if type == "memo":
        query = query.where(WorkNote.user_id == current_user.id)
    elif current_user.role != "admin":
        query = query.where(
            (WorkNote.type != "memo") | (WorkNote.user_id == current_user.id)
        )

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    notes = result.scalars().all()

    return {
        "items": notes,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size
    }

# ---------- 更新笔记 ----------
@router.put("/{note_id}", response_model=NoteInDB)
async def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await ensure_tenant_schema(db)
    note = await note_crud.get(db, id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    if note_in.type and isinstance(note_in.type, str):
        note_in.type = note_in.type.lower()
    return await note_crud.update(db, db_obj=note, obj_in=note_in)

# ---------- 删除笔记 ----------
@router.delete("/{note_id}", response_model=NoteInDB)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await ensure_tenant_schema(db)
    note = await note_crud.get(db, id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    return await note_crud.remove(db, id=note_id)

# ---------- 下载模板 ----------
@router.get("/template")
async def download_template(type: str = Query(...)):
    wb = Workbook()
    ws = wb.active
    ws.title = "工作笔记模板"
    base_headers = ["标题", "内容"]
    extra_fields = get_extra_fields(type)
    extra_headers = list(extra_fields.values())
    headers = base_headers + extra_headers
    ws.append(headers)
    example = ["示例笔记", "这是示例内容"]
    for field in extra_fields.keys():
        if field == "purpose":
            example.append("采购物资")
        elif field == "driver":
            example.append("张三")
        elif field == "user":
            example.append("李四")
        elif field == "remark":
            example.append("无")
        elif field == "project_name":
            example.append("村道硬化工程")
        elif field == "contractor":
            example.append("XX建筑公司")
        elif field == "contract_amount":
            example.append("50000")
        elif field == "progress":
            example.append("50%")
        elif field == "reason":
            example.append("修路")
        elif field == "workers":
            example.append("王五,赵六")
        elif field == "wage_amount":
            example.append("200")
        elif field == "total":
            example.append("1000")
        elif field == "description":
            example.append("详细说明")
        elif field == "item":
            example.append("购买种子")
        else:
            example.append("")
    ws.append(example)
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename=note_template_{type}.xlsx"})

# ---------- 批量导入 ----------
@router.post("/import")
async def import_notes(
    file: UploadFile = File(...),
    type: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await ensure_tenant_schema(db)
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(400, "只支持 Excel 文件")
    df = pd.read_excel(file.file)
    if "标题" not in df.columns:
        raise HTTPException(400, "Excel 缺少'标题'列")
    extra_fields = get_extra_fields(type)
    success = 0
    errors = []
    for idx, row in df.iterrows():
        try:
            title = str(row["标题"]).strip()
            if not title:
                raise ValueError("标题不能为空")
            content = str(row["内容"]) if "内容" in df.columns and pd.notna(row["内容"]) else None
            extra_data = {}
            for field, header in extra_fields.items():
                if header in df.columns and pd.notna(row[header]):
                    val = row[header]
                    if field in ["contract_amount", "wage_amount", "total"]:
                        try:
                            val = float(val)
                        except:
                            pass
                    extra_data[field] = val
            await note_crud.create(db, obj_in={"type": type, "title": title, "content": content, "extra_data": extra_data, "user_id": current_user.id})
            success += 1
        except Exception as e:
            errors.append(f"第{idx+2}行: {str(e)}")
    await db.commit()
    return {"success": success, "errors": errors}

# ---------- 导出 ----------
@router.get("/export")
async def export_notes(
    type: str = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await ensure_tenant_schema(db)
    query = select(WorkNote).where(WorkNote.type == type.lower())
    if type.lower() == "memo":
        query = query.where(WorkNote.user_id == current_user.id)
    elif current_user.role != "admin":
        query = query.where((WorkNote.type != "memo") | (WorkNote.user_id == current_user.id))
    result = await db.execute(query)
    notes = result.scalars().all()
    extra_fields = get_extra_fields(type)
    base_headers = ["ID", "标题", "内容", "创建时间"]
    headers = base_headers + list(extra_fields.values())
    data = []
    for n in notes:
        row = [n.id, n.title, n.content or "", n.created_at.strftime("%Y-%m-%d %H:%M:%S") if n.created_at else ""]
        for field in extra_fields.keys():
            val = n.extra_data.get(field) if n.extra_data else ""
            if isinstance(val, float):
                val = f"{val:.2f}"
            row.append(val if val is not None else "")
        data.append(row)
    df = pd.DataFrame(data, columns=headers)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="工作笔记")
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename=notes_{type}_export.xlsx"})