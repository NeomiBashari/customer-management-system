from pydantic import BaseModel, EmailStr, Field

class CustomerCreateRequest(BaseModel):
    firstname : str
    lastname : str
    email : EmailStr

class CustomerCreateRespone(BaseModel):
    res_id: int
    email : EmailStr
    message: str

class CustomerGetByID(BaseModel):
    id: str

class CustomerGetResponse(BaseModel):
    firstname:str
    lastname:str
    message: str

class CustomerAllResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email : EmailStr

