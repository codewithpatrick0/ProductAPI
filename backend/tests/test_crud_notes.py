import pytest

from crud.note_crud import create_note, get_notes_by_user, get_note_by_id, edit_note, delete_note, NoteNotFoundError
from schemes.note import NoteCreate, NoteEdit

def test_create_note(db_session, registered_user):
    note = create_note(db_session, registered_user.user.id, NoteCreate(
        title='Hello World',
        content='Test Content'
    ))

    assert note.user_id == registered_user.user.id

def test_get_notes_by_user_id(db_session, registered_user, created_note):
    list_notes = get_notes_by_user(db_session, registered_user.user.id)

    assert isinstance(list_notes, list)
    assert len(list_notes) == 1
    assert list_notes[0].user_id == created_note.user_id
    assert list_notes[0].id == created_note.id
    assert list_notes[0].title == created_note.title
    assert list_notes[0].content == created_note.content

def test_get_notes_by_user_only_returns_own_notes(db_session, second_registered_user, created_note):
    list_notes = get_notes_by_user(db_session, second_registered_user.user.id)

    assert list_notes == []

def test_get_note_by_id(db_session, registered_user, created_note):
    note = get_note_by_id(db_session, created_note.id, registered_user.user.id)

    assert note.id == created_note.id
    assert note.title == created_note.title
    assert note.content == created_note.content

def test_exception_get_note_by_id_not_found(db_session, registered_user):
    with pytest.raises(NoteNotFoundError):
        get_note_by_id(db_session, 9999, registered_user.user.id)

def test_exception_get_note_by_id_wrong_owner(db_session, second_registered_user, created_note):
    with pytest.raises(NoteNotFoundError):
        get_note_by_id(db_session, created_note.id, second_registered_user.user.id)

def test_edit_note(db_session, registered_user, created_note):
    edited_note = edit_note(db_session, created_note.id, NoteEdit(title='Updated Title'), registered_user.user.id)

    assert edited_note.title == 'Updated Title'
    assert edited_note.content == created_note.content

def test_exception_edit_note_wrong_owner(db_session, second_registered_user, created_note):
    with pytest.raises(NoteNotFoundError):
        edit_note(db_session, created_note.id, NoteEdit(title='Python developer'), second_registered_user.user.id)

def test_delete_note(db_session, registered_user, created_note):
    delete_note(db_session, created_note.id, registered_user.user.id)

    with pytest.raises(NoteNotFoundError):
        get_note_by_id(db_session, created_note.id, registered_user.user.id)

def test_exception_delete_note_wrong_owner(db_session, second_registered_user, created_note):
    with pytest.raises(NoteNotFoundError):
        delete_note(db_session, created_note.id, second_registered_user.user.id)
