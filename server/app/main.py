from fastapi import FastAPI
import uvicorn
from router.user_router import router as user_router
from router.change_password_router import router as change_password_router
from router.forgot_password_router import router as forgot_password_router

app = FastAPI()
app.include_router(user_router)
app.include_router(change_password_router)
app.include_router(forgot_password_router)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)