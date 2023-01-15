import os 
import uuid
from fastapi import FastAPI, HTTPException,Depends,status
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schema,utility
from .database import engine, get_db
from .routers import post,user,animal,adoption,auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
 
 
while True:

    try:
        conn = psycopg2.connect(host='localhost',database='pets',user='postgres',password='14323391',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection established successfully')
        break
    except exception as error: 
        print('database connection failed')
        print("error:",error)
        time.sleep(5)  

app.include_router(post.router)
app.include_router(user.router)
app.include_router(animal.router)
app.include_router(adoption.router)
app.include_router(auth.router)