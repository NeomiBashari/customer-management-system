from fastapi import APIRouter, HTTPException
from models.user import UserCreateRequest, UserCreateResponse
import controllers.user_controller as uc

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserCreateResponse)
def create_user(user_req: UserCreateRequest):
    try:
        # כאן קוראים לפונקציה שב־controller
        return uc.create_user(user_req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
