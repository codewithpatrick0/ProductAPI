from pydantic import BaseModel, ConfigDict, Field


class UserRegister(BaseModel):
    name: str
    username: str
    password: str = Field(min_length=5, max_length=24)


class UserLogin(BaseModel):
    username: str
    password: str 


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
