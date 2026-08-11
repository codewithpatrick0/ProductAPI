import pytest
from security.tokens import SECRET_KEY, REFRESH_SECRET_KEY, create_access_token, create_refresh_token, verify_access_token, verify_refresh_token
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

def test_create_and_verify_access_token():
    token = create_access_token(user_id=1)

    assert isinstance(token, str)

    user_id = verify_access_token(token)
    assert user_id == 1

def test_create_and_verify_refresh_token():
    token = create_refresh_token(user_id=1)
    assert isinstance(token, str)

    decoded_user_id = verify_refresh_token(token)
    assert decoded_user_id == 1

def test_exception_invalid_token_access_token():
    with pytest.raises(InvalidTokenError):
        verify_access_token('this.is.not.jwt')

def test_exception_expired_access_token():
    payload = {
        'sub': '1',
        'token_type': 'access',
        'exp': 0
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    with pytest.raises(ExpiredSignatureError):
        verify_access_token(token)

def test_exception_invalid_access_token_by_incorrect_key():
        payload = {
            'sub': '2',
            'token_type': 'access_token',
            'exp': 99999
        }
        token = jwt.encode(payload, REFRESH_SECRET_KEY, algorithm='HS256')
        with pytest.raises(InvalidTokenError):
            verify_access_token(token)

def test_exception_invalid_token_refresh_token():
    with pytest.raises(InvalidTokenError):
        verify_refresh_token('this.is.not.jwt')

def test_exception_expired_refresh_token():
    payload = {
        'sub': '1',
        'token_type': 'refresh',
        'exp': 0
    }
    token = jwt.encode(payload, REFRESH_SECRET_KEY, algorithm='HS256')
    with pytest.raises(ExpiredSignatureError):
        verify_refresh_token(token)

def test_exception_invalid_refresh_token_by_incorrect_key():
    payload = {
        'sub': '2',
        'token_type': 'refresh',
        'exp': 9999999999
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    with pytest.raises(InvalidTokenError):
        verify_refresh_token(token)

