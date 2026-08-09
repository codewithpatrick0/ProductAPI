from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from schemes import user, token

from database.connection import get_db
from crud import user_crud

router_api = APIRouter(prefix='/auth', tags=['Authentication'])

@router_api.post('/register', response_model=user.UserResponse)
def register(user_data: user.UserRegister, db: Session = Depends(get_db)):
    try:
        return user_crud.create_user(db, user_data)
    except user_crud.UsernameAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists')

@router_api.post('/login', response_model=token.TokensResponse)
def login(user_data: user.UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        tokens = user_crud.login_user(db, user_data)
    except user_crud.CredentialsInvalidError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    response.set_cookie(
        key='access_token',
        value=tokens.access_token,
        httponly=True,
        secure=False,
           samesite='lax',
        max_age=60 * 15
    )

    response.set_cookie(
        key='refresh_token',
        value=tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=60 * 60 * 24 * 7
    )

    return tokens


@router_api.post('/refresh', response_model=token.AccessTokenResponse)
def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    try:
        access_token_response = user_crud.refresh_user(refresh_token)
    except user_crud.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    response.set_cookie(
        key='access_token',
        value=access_token_response.access_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=60 * 15
    )

    return access_token_response