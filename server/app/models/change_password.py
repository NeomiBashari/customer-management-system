from pydantic import BaseModel, Field


class ChangePasswordRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=1)


class ChangePasswordResponse(BaseModel):
    user_id: int
    message: str
