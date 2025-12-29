from fastapi import APIRouter, HTTPException
from controllers.change_password_controller import ChangePasswordController
from models.change_password import ChangePasswordRequest, ChangePasswordResponse


class ChangePasswordRouter:
    controller = ChangePasswordController()
    router = APIRouter(prefix="/change-password", tags=["change-password"])

    @staticmethod
    @router.post("/", response_model=ChangePasswordResponse)
    def change_password(body: ChangePasswordRequest):
        try:
            return ChangePasswordRouter.controller.change_password(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# same import style as main.py expects: `from router.x import router as x_router`
router = ChangePasswordRouter.router
