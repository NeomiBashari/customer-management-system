from typing import List
import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException
import bleach

from models.customers import CustomerCreateRequest, CustomerCreateRespone,CustomerGetByID,CustomerGetResponse, CustomerAllResponse
from dao.customer_dao import CustomerDAO

def sanitize(str):
        return bleach.clean(str,tags=[],attributes={},strip=True)

class CustomerController:
     def __init__(self):
        self.dao = CustomerDAO()    
     
     def create_customer_validated(self,cust_req: CustomerCreateRequest) -> CustomerCreateRespone:
        first_name  = sanitize(cust_req.firstname)
        last_name = sanitize(cust_req.lastname)
        email = sanitize(cust_req.email)

        try:
             customer_id = self.dao.insert_customer(first_name,last_name,email)
        except Exception as e:
             raise HTTPException(status_code=500,detail="Internal server error")
        return CustomerCreateRespone(res_id = customer_id,email=email,message="Customer created successfully")
    
     def create_customer_unvalidated(self,cust_req: CustomerCreateRequest) -> CustomerCreateRespone:
        first_name  = cust_req.firstname
        last_name = cust_req.lastname
        email = cust_req.email

        try:
             customer_id = self.dao.insert_customer(first_name,last_name,email)
        except Exception as e:
             raise HTTPException(status_code=500,detail="Internal server error")

        return CustomerCreateRespone(res_id=customer_id,email=email,message="Customer created successfully")

     def view_customer_validated(self,cust_req:CustomerGetByID) -> CustomerGetResponse:
        cust_id = sanitize(cust_req.id)

        try:
              customer = self.dao.get_customer_by_id(cust_id)
        except Exception as e:
             raise HTTPException(status_code=500,detail="Internal server error")

        return CustomerGetResponse(firstname=customer["firstname"],lastname=customer["lastname"],message="Customer retrived successfully")
    
     def view_customer_unvalidated(self,cust_req:CustomerGetByID) -> CustomerGetResponse:
        cust_id = cust_req.id

        try:
              customer = self.dao.get_customer_by_id(cust_id)
        except Error as e:
             print(f"MySQL Error: {e}")
             raise HTTPException(status_code=500,detail="Internal server error")

        return CustomerGetResponse(firstname=customer["firstname"],lastname=customer["lastname"],message="Customer retrived successfully")
     
     def view_all_customers(self) -> List:
        try:
             customers = self.dao.get_all_customers()
             return [CustomerAllResponse(id=c['id'], firstname=c['firstname'], lastname=c['lastname'], email=c['email']) for c in customers]
        except Error as e:
             print(f"MySQL Error: {e}")
             raise HTTPException(status_code=500,detail="Internal server error")
            