from typing import List
import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException
import bleach

from models.customers import CustomerCreateRequest, CustomerCreateRespone,CustomerGetByID,CustomerGetResponse
from dao.customer_dao import CustomerDAO

def sanitize(str):
        return bleach.clean(str,tags=[],attributes={},strip=True)

class CustomerController:
     def __init__(self):
        self.dao = CustomerDAO()
        self.policy = self.load_password_policy()
    
     
     def create_customer_validated(self,cust_req: CustomerCreateRequest) -> CustomerCreateRespone:
        first_name  = sanitize(cust_req.firstname)
        last_name = sanitize(cust_req.lastname)
        email = sanitize(cust_req.email)

        try:
             customer_id = self.dao.insert_customer(first_name,last_name,email)
        except Exception as e:
             raise HTTPException(status_code=500,detail="Internal server error")
        return CustomerCreateRespone(id = customer_id,email=email,message="Customer created successfully")
    
<<<<<<< HEAD
     def create_customer_unvalidated(self,cust_req: CustomerCreateRequest) -> CustomerCreateRespone:
        first_name  = cust_req.firstname
        last_name = cust_req.lastname
        email = cust_req.email
=======
    def create_customer_unvalidated(self,cust_req: CustomerCreateRequest) -> CustomerCreateRespone:
        id = cust_req.id
        first_name  = cust_req.firstname
        last_name = cust_req.lastname
        email = cust_req.email
        phone = cust_req.phone

        try:
             conn = self.get_db_connection()
             cursor = conn.cursor()
             cursor.execute(
                  "INSERT INTO customers (id, firstname, lastname, phone, email) VALUES (%s,%s,%s,%s,%s)",
                  (id,first_name,last_name,phone,email)
             )
             conn.commit()
             user_id = cursor.lastrowid
        except Error as e:
             print(f"MySQL Error: {e}")
             raise HTTPException(status_code=500,detail="Internal server error")
        finally:
            if cursor:
                  cursor.close()
            if conn:
                 conn.close()
        return CustomerCreateRespone(res_id=user_id,email=email,message="Customer created successfully")
>>>>>>> 98ff4f1 (added unsecure methods to customers)

        try:
             customer_id = self.dao.insert_customer(first_name,last_name,email)
        except Exception as e:
             raise HTTPException(status_code=500,detail="Internal server error")

        return CustomerCreateRespone(res_id=customer_id,email=email,message="Customer created successfully")

     def view_customer_validated(self,cust_req:CustomerGetByID) -> CustomerGetResponse:
        cust_id = sanitize(cust_req.id)

        try:
              customer = self.dao.get_customer_by_id
        except Exception as e:
             raise HTTPException(status_code=500,detail="Internal server error")

        return CustomerGetResponse(firstname=customer["firstname"],lastname=customer["lastname"],message="Customer retrived successfully")
    
     def view_customer_unvalidated(self,cust_req:CustomerGetByID) -> CustomerGetResponse:
        cust_id = cust_req.id

        try:
              customer = self.dao.get_customer_by_id
        except Error as e:
             print(f"MySQL Error: {e}")
             raise HTTPException(status_code=500,detail="Internal server error")
<<<<<<< HEAD

        return CustomerGetResponse(firstname=customer["firstname"],lastname=customer["lastname"],message="Customer retrived successfully")
     
     def view_all_customers(self) -> List:
        try:
              customers = self.dao.get_all_customers
        except Error as e:
             print(f"MySQL Error: {e}")
             raise HTTPException(status_code=500,detail="Internal server error")

        return customers
=======
        finally:
            if cursor:
                  cursor.close()
            if conn:
                 conn.close()
        return CustomerGetByIDResponse(res_id=user_id,message="Customer retrieved successfully")
    
    def view_customer_unvalidated(self,cust_req:CustomerGetByID) -> CustomerGetByIDResponse:
        cust_id = cust_req.id

        try:
              conn = self.get_db_connection()
              cursor = conn.cursor()
              cursor.execute(
                   "SELECT * FROM customers WHERE id=(cust_id) VALUES (%s) LIMIT 1",
                   (cust_id)
              )
              conn.commit()
              user_id = cursor.lastrowid
        except Error as e:
             print(f"MySQL Error: {e}")
             raise HTTPException(status_code=500,detail="Internal server error")
        finally:
            if cursor:
                  cursor.close()
            if conn:
                 conn.close()
        return CustomerGetByIDResponse(res_id=user_id,message="Customer retrieved successfully")
>>>>>>> 98ff4f1 (added unsecure methods to customers)
            