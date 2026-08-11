from sqlalchemy import select
from sqlalchemy.orm import Session

from models.note import Note
from schemes.note import NoteCreate, NoteEdit


class NoteNotFoundError(Exception):
    pass


def create_note(db: Session, user_id: int, note: NoteCreate) -> Note:
    db_note = Note(
        user_id=user_id,
        title=note.title,
        content=note.content
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes_by_user(db: Session, user_id: int) -> list[Note]:
    return db.execute(select(Note).where(Note.user_id == user_id)).scalars().all()


def get_note_by_id(db: Session, note_id: int, user_id: int) -> Note:
    note = db.execute(select(Note).where(Note.id == note_id)).scalar_one_or_none()
    if not note:
        raise NoteNotFoundError
    if note.user_id != user_id:
        raise NoteNotFoundError
    
    
    return note


def edit_note(db: Session, note_id: int, note: NoteEdit, user_id: int) -> Note:
    db_note = get_note_by_id(db, note_id, user_id)

    for field, value in note.model_dump(exclude_unset=True).items():
        setattr(db_note, field, value)

    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int, user_id: int) -> None:
    note = get_note_by_id(db, note_id, user_id)
    db.delete(note)
    db.commit()
