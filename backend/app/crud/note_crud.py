from app.crud.base import CRUDBase
from app.models.note import WorkNote
from app.schemas.note import NoteCreate, NoteUpdate

class CRUDNote(CRUDBase[WorkNote, NoteCreate, NoteUpdate]):
    pass

note_crud = CRUDNote(WorkNote)
