from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud import note_crud
from database.connection import get_db
from schemes.note import NoteCreate, NoteEdit, NoteResponse
from security.dependencies import get_current_user_id

router_api = APIRouter(prefix='/notes', tags=['Notes'])


@router_api.post('/', response_model=NoteResponse)
def create_note(note_data: NoteCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return note_crud.create_note(db, user_id, note_data)


@router_api.get('/', response_model=list[NoteResponse])
def list_notes(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return note_crud.get_notes_by_user(db, user_id)


@router_api.get('/{note_id}', response_model=NoteResponse)
def get_note(note_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        return note_crud.get_note_by_id(db, note_id, user_id)
    except note_crud.NoteNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')


@router_api.patch('/{note_id}', response_model=NoteResponse)
def edit_note(note_id: int, note_data: NoteEdit, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        return note_crud.edit_note(db, note_id, note_data, user_id)
    except note_crud.NoteNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')


@router_api.delete('/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        note_crud.delete_note(db, note_id, user_id)
    except note_crud.NoteNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
