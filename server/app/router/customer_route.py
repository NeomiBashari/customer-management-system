from typing import List
from fastapi import APIRouter, HTTPException
from models.customers import CustomerCreateRespone, CustomerCreateRequest,CustomerGetByID,CustomerGetByEmail,CustomerGetResponse
from controllers.customer_controller import CustomerController

class CustomerRouter:
    controller = CustomerController()
    router = APIRouter(prefix="/customers", tags=["customers"])

    @staticmethod
    @router.post("/create/validated", response_model=CustomerCreateRespone)
<<<<<<< HEAD
    def create_customer_validated(body: CustomerCreateRequest):
=======
    def create_user(body: CustomerCreateRequest):
>>>>>>> 98ff4f1 (added unsecure methods to customers)
        try:
            return CustomerRouter.controller.create_customer_validated(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    @router.post("/create/unvalidated", response_model=CustomerCreateRespone)
<<<<<<< HEAD
    def create_customer_unvalidated(body: CustomerCreateRequest):
=======
    def create_user(body: CustomerCreateRequest):
        try:
            return CustomerRouter.controller.create_customer_unvalidated(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    @router.post("/{id}/validated", response_model=CustomerGetByIDResponse)
    def create_user(body: CustomerGetByID):
>>>>>>> 98ff4f1 (added unsecure methods to customers)
        try:
            return CustomerRouter.controller.create_customer_unvalidated(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
<<<<<<< HEAD
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
    @router.post("/all", response_model=List[CustomerCreateRespone])
    def view_all_customers():
        try:
            return CustomerRouter.controller.view_all_customers()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        
    
=======
    @router.post("/{id}/unvalidated", response_model=CustomerGetByIDResponse)
    def create_user(body: CustomerGetByID):
        try:
            return CustomerRouter.controller.create_customer_unvalidated(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
>>>>>>> 98ff4f1 (added unsecure methods to customers)
    
