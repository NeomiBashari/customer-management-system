import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException
import bleach

from models.customers import CustomerCreateRequest, CustomerCreateRespone,CustomerGetByID,CustomerGetByIDResponse

def sanitize(str):
        return bleach.clean(str,tags=[],attributes={},strip=True)

class CustomerController:
    

    def get_db_connection(self):
        return mysql.connector.connect(
            host="127.0.0.1",
            user="myuser",
            password="mypassword",
            database="user_data"
        )
     
    def create_customer(self,cust_req: CustomerCreateRequest) -> CustomerCreateRespone:
        id = sanitize(cust_req.id)
        first_name  = sanitize(cust_req.firstname)
        last_name = sanitize(cust_req.lastname)
        email = sanitize(cust_req.email)
        phone = sanitize(cust_req.phone)

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

    def view_customer(self,cust_req:CustomerGetByID) -> CustomerGetByIDResponse:
        cust_id = sanitize(cust_req.id)

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
            