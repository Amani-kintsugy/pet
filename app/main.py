import os 
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import psycopg2
from psycopg2.extras import RealDictCursor #ADD THE COLUMN NAME
import time

app = FastAPI()

#database connection
while True:

    try:
        conn = psycopg2.connect(host='localhost',database='pets',user='postgres',password='14323391',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection established successfully')
        break
    except exception as error: 
        print('database connection failed')
        print("error:",error)
        time.sleep(5)  #reconnect automatically again after 5 seconds
    

# Set the location where the uploaded images will be saved
#UPLOAD_FOLDER = 'path/to/image/folder'


# blueprint
class Post(BaseModel):
    title: str
    content: str
    image_url:str=None
    posting_time:str=None

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
    



#path operations
#posters:

#read all posts
@app.get("/posts")
def view_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    print(posts)
    return{"posts":posts,"status_code": 200, "detail":"post created successfully"}
    
#create a new post
@app.post("/posts")
def create_post(post:Post):
   cursor.execute("""INSERT INTO posts (title,content) VALUES(%s,%s) RETURNING *""",
                    (post.title,post.content))
   new_post = cursor.fetchone()
   conn.commit()
   return {"data": new_post}

#delete a new post
@app.delete("/posts/{id}")
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE post_id = %s RETURNING *""",(id,))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post==None:
        raise HTTPException(status_code=404, detail="post not found")
    return {"status_code": 200, "detail":"post deleted successfully"}


#update a certain post







#animals:
#Save animal to a database or process it here
@app.post("/animal/")
def create_animal(animal: Animal):
    cursor.execute("""INSERT INTO animals (species,gender,description,image_url) VALUES(%s,%s,%s,%s) RETURNING *""",
                    (animal.species,animal.gender,animal.description,animal.image_url))
    new_animal = cursor.fetchone()
    conn.commit()
    return {"data": new_animal,"status_code": 200, "detail":"Animal created successfully"}

#Retrieve all available animals from the database
@app.get("/animals/")
def read_animals():
    cursor.execute("""SELECT * FROM ANIMALS WHERE available = True""")
    animals=cursor.fetchall()
    print(animals)
    return{"animals":animals}
    

#update an animal by id in the list
@app.put("/animal/{animal_id}")
def update_animal(animal_id: int, animal: Animal):
    animal_dict = animal.dict()
    animal_dict["animal_id"] = animal_id
    index = next((index for (index, d) in enumerate(animals_list) if d["animal_id"] == animal_id), None)
    if index is not None:
        animals_list[index] = animal_dict
        return animal_dict
    else:
        raise HTTPException(status_code=404, detail="Animals not found")

#delete an animal from the list
@app.delete("/animals/{id}")
def delete_animal(id: int):
    cursor.execute("""DELETE FROM animals WHERE animal_id = %s RETURNING *""",(id,))
    deleted_animal=cursor.fetchone()
    conn.commit()
    if deleted_animal==None:
        raise HTTPException(status_code=404, detail="animal not found")
    return {"status_code": 200, "detail":"animal deleted successfully"}




#adoptors:  

@app.post("/adoption/")
def create_adoption(adoption: Adoption):
    animal = next((animal for animal in animals_list if animal["animal_id"] == animal_id), None)
    if animal is not None and animal["available"] == True:
        animal["available"] = False
        adoption_list.append(adoption.dict())
        return {"message": "Adoption created successfully", "adoption": adoption}
    else:
        raise HTTPException(status_code=404, detail="Animal not found or not available for adoption")

# Retrieve a specific adoption by ID 
@app.get("/adoption/{id}")
def read_adoption(id: int):
    cursor.execute("""SELECT * FROM adoption WHERE adoption_id = %s""", (id,))
    adoption = cursor.fetchone()
    if not adoption:
        raise HTTPException(status_code=404, detail="Adoption not found")
    return {"adoption":adoption}

# Retrieve all adoptions
@app.get("/adoption/")
def read_adoptions():
   cursor.execute("""SELECT * FROM adoption""")
   adopter=cursor.fetchall()
   print(adopter)
   return{"adopter":adopter}

# Create a new adoption
@app.post("/adoption/newadoption")
def create_adoption(adoption: Adoption):
    cursor.execute("""INSERT INTO adoption (adopter_name,adopter_email,adopter_phone,animal_id) VALUES(%s,%s,%s,%s) RETURNING *""",
                        (adoption.adopter_name,adoption.adopter_email,adoption.adopter_phone,adoption.animal_id))
    new_adoption = cursor.fetchone()
    conn.commit()
    return {"data": new_adoption,"status_code": 200, "detail":"Adoption created successfully" }


# Update an existing adoption
@app.put("/adoption/{id}")
def update_adoption(id: int, adoption: Adoption):
    index = next((index for (index, d) in enumerate(adoptions_list) if d["id"] == id), None)
    if index is not None:
        adoptions_list[index] = adoption.dict()
        return {"message": "Adoption updated successfully", "adoption": adoption}
    else:
        raise HTTPException(status_code=404, detail="Adoption not found")

# Delete an adoption
@app.delete("/adoption/{id}")
def delete_adoption(id: int):
    cursor.execute("""DELETE FROM adoption WHERE adoption_id = %s RETURNING *""",(id,))
    deleted_adoption=cursor.fetchone()
    conn.commit()
    if deleted_adoption==None:
        raise HTTPException(status_code=404, detail="adoption not found")
    return {"status_code": 200, "detail":"adoption deleted successfully"}
