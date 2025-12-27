from pydantic import BaseModel, Field


class ForgotPasswordRequest(BaseModel):
    user_id: int = Field(..., gt=0)


class ForgotPasswordResponse(BaseModel):
    user_id: int
    message: str


class ForgotPasswordVerifyRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    code: str = Field(..., min_length=4, max_length=12)


class ForgotPasswordVerifyResponse(BaseModel):
    user_id: int
    verified: bool
    next_action: str
    message: str
