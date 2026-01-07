from fastapi import APIRouter, HTTPException
from models.user import UserCreateRequest, UserCreateResponse, UserLoginRequest, UserChangePasswordRequest
from controllers.user_controller import UserController

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
    def create_user_without_validation(body: UserCreateRequest):
        try:
            return UserRouter.controller.create_user_without_validation(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/login/validated")
    def login_with_validation(body: UserLoginRequest):
        try:
            return UserRouter.controller.login(body.email, body.password)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    @router.post("/login/unvalidated")
    def login_without_validation(email: str, password: str):
        try:
            return UserRouter.controller.login(email, password)
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
    def change_password_without_validation(email: str, old_password: str, new_password: str):
        try:
            return UserRouter.controller.change_password_without_validation(email, old_password, new_password)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))