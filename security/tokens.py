import jwt
import os
from datetime import datetime, timedelta, UTC
from typing import Literal
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = 'HS256'

def create_payload(user_id, token_type: Literal['access', 'refresh']) -> dict:
    expire_delta = (
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if token_type == 'access'
        else timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    exp = datetime.now(UTC) + expire_delta

    return {
        'sub': str(user_id),
        'token_type': token_type,
        'exp': int(exp.timestamp())
    }
        

def create_token(
        user_id: int,
        token_type: Literal['access', 'refresh']
    ) -> str:
    payload = create_payload(user_id, token_type)
    key = (
            SECRET_KEY 
           if token_type == 'access' 
           else REFRESH_SECRET_KEY
           )
    return jwt.encode(payload, key, algorithm=ALGORITHM)


def create_access_token(user_id: int) -> str:
    return create_token(user_id, 'access')


def create_refresh_token(user_id: int) -> str:
    return create_token(user_id, 'refresh')

def check_token(token: str, token_type: Literal['access', 'refresh']) -> int:
    key = (
        SECRET_KEY
        if token_type == 'access'
        else REFRESH_SECRET_KEY
        )
    payload = jwt.decode(token, key, algorithms=[ALGORITHM])
    return int(payload.get('sub'))


def verify_access_token(token: str) -> int:
    return check_token(token, 'access')


def verify_refresh_token(token: str) -> int:
    return check_token(token, 'refresh')


