from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from router.user_router import UserRouter
from router.customer_route import CustomerRouter

app = FastAPI()

app.include_router(UserRouter.router)
app.include_router(CustomerRouter.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
