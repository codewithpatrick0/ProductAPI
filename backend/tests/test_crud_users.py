import pytest
from security.tokens import verify_access_token, verify_refresh_token
from crud.user_crud import UsernameAlreadyExistsError, CredentialsInvalidError, InvalidTokenError, create_user, login_user, get_user_by_id, get_user_by_username, refresh_user

from schemes.user import UserRegister, UserLogin

def test_create_user(db_session):

    new_user = create_user(db_session, UserRegister(
            name='Patrick',
            username='Pat23',
            password='password'
            )
        )
    assert new_user.id is not None
    assert new_user.name == 'Patrick'
    assert new_user.username == 'Pat23'
    assert isinstance(new_user.hash_password, str)

def test_login_user(db_session, registered_user):
    tokens = login_user(db_session, UserLogin(
        username=registered_user.username, 
        password=registered_user.password
    ))

    access_user_id = verify_access_token(tokens.access_token)
    refresh_user_id = verify_refresh_token(tokens.refresh_token)

    assert access_user_id == registered_user.user.id
    assert refresh_user_id == registered_user.user.id

def test_get_user_by_id(db_session, registered_user):
    user_id = get_user_by_id(db_session, registered_user.user.id).id

    assert user_id == registered_user.user.id

def test_get_user_by_username(db_session, registered_user):
    user = get_user_by_username(db_session, registered_user.username)

    assert user == registered_user.user

def test_refresh_user(registered_user, tokens_registered_user):
    new_access_token = refresh_user(tokens_registered_user.get('refresh_token'))
    user_id = verify_access_token(new_access_token.access_token)
    assert user_id == registered_user.user.id

def test_exception_user_already_exists_create_user(db_session, registered_user):
    new_user = UserRegister(
        name='Jorge',
        username='Pat23',
        password='123456'
    )
    with pytest.raises(UsernameAlreadyExistsError):
        create_user(db_session, new_user)

def test_exception_login_user_username_not_found(db_session):
    with pytest.raises(CredentialsInvalidError):
        login_user(db_session, UserLogin(
            username='Pat23',
            password='whatever'
        ))

def test_exception_login_user_wrong_password(db_session, registered_user):
    with pytest.raises(CredentialsInvalidError):
        login_user(db_session, UserLogin(
            username=registered_user.username,
            password='wrong_password'
        ))

def test_exception_refresh_user_invalid_token():
    with pytest.raises(InvalidTokenError):
        refresh_user('this.is.not.jwt')
