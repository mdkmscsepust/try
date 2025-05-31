from pydantic import BaseModel


class UserIn(BaseModel):
    name:str
    username:str
    email:str
    password:str
    contact:str
    
class UserOut(BaseModel):
    id: int
    name: str
    username: str
    email: str
    contact: str
    
    class config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
    
class LoginOut(BaseModel):
    access_token: str