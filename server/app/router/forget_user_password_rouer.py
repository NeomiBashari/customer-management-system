from fastapi import APIRouter, HTTPException
from controllers.forget_user_password import ForgotPasswordController
from models.forget_user_password import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ForgotPasswordVerifyRequest,
    ForgotPasswordVerifyResponse,
)


class ForgotPasswordRouter:
    controller = ForgotPasswordController()
    router = APIRouter(prefix="/forgot-password", tags=["forgot-password"])

    @staticmethod
    @router.post("/validated", response_model=ForgotPasswordResponse)
    def request_reset(body: ForgotPasswordRequest):
        try:
            return ForgotPasswordRouter.controller.request_reset(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/unvalidated", response_model=ForgotPasswordVerifyResponse)
    def verify_code(body: ForgotPasswordVerifyRequest):
        try:
            return ForgotPasswordRouter.controller.verify_reset_password(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))