import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User
from schemes.user import UserRegister, UserLogin
from schemes.token import TokensResponse, AccessTokenResponse
from security.hashing import hash_password, verify_password

from security import tokens

class InvalidTokenError(Exception):
    pass

class UsernameAlreadyExistsError(Exception):
    pass

class CredentialsInvalidError(Exception):
    pass

def create_user(db: Session, user: UserRegister) -> User:
    if get_user_by_username(db, user.username):
        raise UsernameAlreadyExistsError

    db_user = User(
        name=user.name,
        username=user.username,
        hash_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, user: UserLogin) -> TokensResponse:
    user_extracted = get_user_by_username(db, user.username)
    if not user_extracted:
        raise CredentialsInvalidError
    if not verify_password(user.password, user_extracted.hash_password):
        raise CredentialsInvalidError
    access_token = tokens.create_access_token(user_extracted.id)
    refresh_token = tokens.create_refresh_token(user_extracted.id)
    return TokensResponse(access_token=access_token, refresh_token=refresh_token)
    
    
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

def get_user_by_username(db: Session, username: str) ->  User | None:
    return db.execute(select(User).where(User.username == username)).scalar_one_or_none()

def refresh_user(refresh_token: str) -> AccessTokenResponse:
    try:
        user_id = tokens.verify_refresh_token(refresh_token)
    except jwt.InvalidTokenError:
        raise InvalidTokenError

    access_token = tokens.create_access_token(user_id)
    return AccessTokenResponse(access_token=access_token)
    