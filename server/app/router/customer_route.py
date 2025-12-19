from fastapi import APIRouter, HTTPException
from models.customers import CustomerCreateRespone, CustomerCreateRequest,CustomerGetByID, CustomerGetByIDResponse
from controllers.customer_controller import CustomerController

class CustomerRouter:
    controller = CustomerController()
    router = APIRouter(prefix="/customers", tags=["customers"])

    @staticmethod
    @router.post("/", response_model=CustomerCreateRespone)
    def create_user(body: CustomerCreateRequest):
        try:
            return CustomerRouter.controller.create_customer(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    @router.post("/{id}", response_model=CustomerGetByIDResponse)
    def create_user(body: CustomerGetByID):
        try:
            return CustomerRouter.controller.create_customer(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
