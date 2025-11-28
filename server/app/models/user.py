from pydantic import BaseModel, EmailStr, Field

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    message: str
