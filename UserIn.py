from pydantic import BaseModel


class UserIn(BaseModel):
    name:str
    username:str
    email:str
    password:str
    contact:str