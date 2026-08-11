import jwt
from fastapi import HTTPException, Request, status
from security.tokens import verify_access_token

def get_exception_unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or expired token',
        headers={'WWW-Authenticate': 'Bearer'}
    )

def get_current_user_id(request: Request) -> int:
    token = request.cookies.get('access_token')
    if not token:
        raise get_exception_unauthorized()
    try:
        return verify_access_token(token)
    except jwt.InvalidTokenError:
        raise get_exception_unauthorized()
