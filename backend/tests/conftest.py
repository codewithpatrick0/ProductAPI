from dataclasses import dataclass

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.base import Base
import models

from security.tokens import create_refresh_token, create_access_token
from crud.user_crud import create_user
from schemes.user import UserRegister
from models.user import User

@pytest.fixture
def db_session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@dataclass
class RegisteredUser:
    user: User
    username: str
    password: str


@pytest.fixture
def registered_user(db_session):
    username='Pat23'
    password='password'
    user = create_user(db_session, UserRegister(
        name='Patrick',
        username=username,
        password=password
    ))
    return RegisteredUser(user=user, username=username, password=password)

@pytest.fixture
def tokens_registered_user(registered_user):
    return {
        'refresh_token': create_refresh_token(registered_user.user.id),
        'access_token': create_access_token(registered_user.user.id)
    }



