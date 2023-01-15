from .. import models,schema
from fastapi import FastAPI, HTTPException,Depends,status,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    tags=['post']
)
#read all posts
@router.get("/posts")
def view_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    
#create a new post
@router.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:schema.Post, db: Session=Depends(get_db)):
    new_post = models.Post(title=post.title,content=post.content,image_url=post.image_url)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#delete a new post
@router.delete("/posts/{id}")
def delete_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.post_id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"status_code": 200, "detail":"Post deleted successfully"}

#update a certain post
@router.put("/posts/{id}")
def update_post(id:int, post:schema.Post, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.post_id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    return {"status_code": 200, "detail":"Post updated successfully"}