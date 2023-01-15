from .. import models,schema,utility
from fastapi import FastAPI, HTTPException,Depends,status,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
   tags=['user']
)
#create a new user
@router.post("/users",status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user:schema.UserCreate, db: Session=Depends(get_db)):
    hashed_pwd=utility.hash(user.password)
    user.password=hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#get a specific user 
@router.get("/users/{id}",response_model=schema.UserOut)
def view_users(id:int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == id).first()
    if not user:
        raise HTTPExeption(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} does not exist")
    return user

