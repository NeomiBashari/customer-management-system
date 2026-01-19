from typing import List
from fastapi import APIRouter, HTTPException
from models.customers import CustomerCreateRespone, CustomerCreateRequest,CustomerGetByID,CustomerGetResponse, CustomerAllResponse
from controllers.customer_controller import CustomerController

class CustomerRouter:
    controller = CustomerController()
    router = APIRouter(prefix="/customers", tags=["customers"])

    @staticmethod
    @router.post("/create/validated", response_model=CustomerCreateRespone)
    def create_customer_validated(body: CustomerCreateRequest):
        try:
            return CustomerRouter.controller.create_customer_validated(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    @router.post("/create/unvalidated", response_model=CustomerCreateRespone)
    def create_customer_unvalidated(body: CustomerCreateRequest):
        try:
            return CustomerRouter.controller.create_customer_unvalidated(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    @router.post("/{id}/validated", response_model=CustomerGetResponse)
    def view_customer_validated(body: CustomerGetByID):
        try:
            return CustomerRouter.controller.view_customer_validated(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    @router.post("/{id}/unvalidated", response_model=CustomerGetResponse)
    def view_customer_unvalidated(body: CustomerGetByID):
        try:
            return CustomerRouter.controller.view_customer_unvalidated(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    @router.post("/all", response_model=List[CustomerAllResponse])
    def view_all_customers():
        try:
            return CustomerRouter.controller.view_all_customers()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        
    
    
