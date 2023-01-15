from pydantic import BaseModel,validator,EmailStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    image_url:str
   

    #a post should at least have a title 
    @validator("title")
    def title_not_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Title should not be empty")
        return value

class Animal(BaseModel):
    
    species: str
    gender: str
    description: str 
    image_url: str 
    available: bool=None
    
  
    

class Adoption(BaseModel):
    animal_id:str
    adopter_name: str=None
    adopter_email: str=None
    adopter_phone: str
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    created_at:datetime
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
