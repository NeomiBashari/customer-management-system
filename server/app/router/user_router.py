from fastapi import APIRouter, HTTPException
from models.user import UserCreateRequest, UserCreateResponse
from controllers.user_controller import UserController

class UserRouter:
    controller = UserController()
    router = APIRouter(prefix="/users", tags=["users"])

    @staticmethod
    @router.post("/", response_model=UserCreateResponse)
    def create_user(body: UserCreateRequest):
        try:
            return UserRouter.controller.create_user(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
