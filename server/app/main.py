from fastapi import FastAPI
import uvicorn
from router.user_router import UserRouter

app = FastAPI()
app.include_router(UserRouter.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)