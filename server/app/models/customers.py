from pydantic import BaseModel, EmailStr, Field

class CustomerCreateRequest(BaseModel):
    id : str
    firstname : str
    lastname : str
    phone : str
    email : EmailStr

class CustomerCreateRespone(BaseModel):
    res_id: int
    email : EmailStr
    message: str

class CustomerGetByID(BaseModel):
    id: str

class CustomerGetByIDResponse(BaseModel):
    res_id: int
    message: str