from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from models.user import UserCreateRequest, UserCreateResponse, UserLoginRequest, UserChangePasswordRequest, ForgotPasswordRequest
from controllers.user_controller import UserController

class UnvalidatedLoginRequest(BaseModel):
    email: str
    password: str

class UserRouter:
    controller = UserController()
    router = APIRouter(prefix="/users", tags=["users"])

    @staticmethod
    @router.post("/create/validated", response_model=UserCreateResponse)
    def create_user_with_validation(body: UserCreateRequest):
        try:
            return UserRouter.controller.create_user_with_validation(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/create/unvalidated", response_model=UserCreateResponse)
    async def create_user_without_validation(request: Request):
        try:
            body = await request.json()
            email = body.get("email")
            password = body.get("password")

            return UserRouter.controller.create_user_without_validation(
                email, password
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/login/validated")
    def login_with_validation(body: UserLoginRequest):
        try:
            return UserRouter.controller.login(body.email, body.password)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/login/unvalidated")
    def login_without_validation(body: UnvalidatedLoginRequest):
        try:
            return UserRouter.controller.login_vulnerable(body.email, body.password)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    @router.put("/change-password/validated")
    def change_password_with_validation(body: UserChangePasswordRequest):
        try:
            return UserRouter.controller.change_password_with_validation(body.email, body.old_password, body.new_password)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.put("/change-password/unvalidated")
    def change_password_without_validation(body: UserChangePasswordRequest):
        try:
            return UserRouter.controller.change_password_without_validation(body.email, body.old_password, body.new_password)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/forgot-password/validated")
    def forgot_password_validated(body: ForgotPasswordRequest):
        try:
            return UserRouter.controller.initiate_forgot_password_validated(body.email)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/forgot-password/unvalidated")
    def forgot_password_unvalidated(body: ForgotPasswordRequest):
        try:
            return UserRouter.controller.initiate_forgot_password_unvalidated(body.email)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/reset-password/validated")
    def reset_password_validated(body: UserChangePasswordRequest):
        try:
            return UserRouter.controller.reset_password_validated(body.email, body.old_password, body.new_password)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/reset-password/unvalidated")
    def reset_password_unvalidated(body: UserChangePasswordRequest):
        try:
            return UserRouter.controller.reset_password_unvalidated(body.email, body.old_password, body.new_password)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
