from fastapi import FastAPI
import uvicorn
from router.user_router import UserRouter
from router.customer_route import CustomerRouter

app = FastAPI()
app.include_router(UserRouter.router)
app.include_router(CustomerRouter.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)