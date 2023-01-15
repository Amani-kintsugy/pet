import os 
import uuid
from fastapi import FastAPI, HTTPException,Depends,status
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schema
from .database import engine, get_db

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






#path operations
#posters:

#read all posts
@app.get("/posts")
def view_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    
#create a new post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:schema.Post, db: Session=Depends(get_db)):
    new_post = models.Post(title=post.title,content=post.content,image_url=post.image_url)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#delete a new post
@app.delete("/posts/{id}")
def delete_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.post_id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"status_code": 200, "detail":"Post deleted successfully"}

#update a certain post
@app.put("/posts/{id}")
def update_post(id:int, post:schema.Post, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.post_id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    return {"status_code": 200, "detail":"Post updated successfully"}





#animals:
#Save animal to a database or process it here
@app.post("/animal",status_code=status.HTTP_201_CREATED)
def create_animal(animal: schema.Animal, db: Session = Depends(get_db)):
    new_animal = models.Animal(species=animal.species, gender=animal.gender,description=animal.description,image_url=animal.image_url)
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    return {"data": new_animal}
#Retrieve all available animals from the database
@app.get("/animals")
def read_animals(db: Session = Depends(get_db)):
    animals = db.query(models.Animal).filter(models.Animal.available == True).all()
    return animals

#update an animal by id in the list
@app.put("/animal/{animal_id}")
def update_animal(animal_id: int, animal: schema.Animal, db: Session = Depends(get_db)):
    db_animal = db.query(models.Animal).filter(models.Animal.animal_id == animal_id).first()
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    db_animal.species = animal.species
    db_animal.gender = animal.gender
    db_animal.description = animal.description
    db_animal.image_url = animal.image_url
    db.commit()
    return {"status_code": 200, "detail":"Animals account updated successfully"}


@app.delete("/animals/{id}")
def delete_animal(id: int, db: Session = Depends(get_db)):
    animal = db.query(models.Animal).filter(models.Animal.animal_id == id).first()
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    db.delete(animal)
    db.commit()
    return {"status_code": 200, "detail":"Animal deleted successfully"}

#@app.post("/adoption/")
#def create_adoption(adoption: Adoption):
   # animal = next((animal for animal in animals_list if animal["animal_id"] == animal_id), None)
    #if animal is not None and animal["available"] == True:
        #animal["available"] = False
        #adoption_list.append(adoption.dict())
        #return {"message": "Adoption created successfully", "adoption": adoption}
    #else:
       # raise HTTPException(status_code=404, detail="Animal not found or not available for adoption")


#adoptors:  

# link in models between animal and adoption model
@app.get("/adoption/{id}")
def read_adoption(id: int, db: Session = Depends(get_db)):
    adoption = db.query(models.Adoption).filter(models.Adoption.adoption_id == id)
    if not adoption:
        raise HTTPException(status_code=404, detail="Adoption not found")
    return adoption

# Retrieve all adopt

@app.get("/adoption/")
def read_adoptions(db: Session=Depends(get_db)):
    adoptions = db.query(models.Adoption).all()
    return adoptions

@app.post("/adoption/newadoption",status_code=status.HTTP_201_CREATED)
def create_adoption(adoption: schema.Adoption, db: Session = Depends(get_db)):
    new_adoption = models.Adoption(adopter_name=adoption.adopter_name, adopter_email=adoption.adopter_email, adopter_phone=adoption.adopter_phone, animal_id=adoption.animal_id)
    db.add(new_adoption)
    db.commit()
    db.refresh(new_adoption)
    return new_adoption

@app.delete("/adoption/{id}")
def delete_adoption(id: int, db: Session = Depends(get_db)):
    adoption = db.query(models.Adoption).filter(models.Adoption.adoption_id == id).first()
    if adoption is None:
        raise HTTPException(status_code=404, detail="Adoption not found")
    db.delete(adoption)
    db.commit()
    return {"status_code": 200, "detail":"Adoption deleted successfully"}

#user
#create a new user
@app.post("/users",status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user:schema.UserCreate, db: Session=Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
