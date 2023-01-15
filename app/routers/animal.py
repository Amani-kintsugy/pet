from .. import models,schema
from fastapi import FastAPI, HTTPException,Depends,status,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    tags=['animal']
)
#Save animal to a database or process it here
@router.post("/animal",status_code=status.HTTP_201_CREATED)
def create_animal(animal: schema.Animal, db: Session = Depends(get_db)):
    new_animal = models.Animal(species=animal.species, gender=animal.gender,description=animal.description,image_url=animal.image_url)
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    return {"data": new_animal}
#Retrieve all available animals from the database
@router.get("/animals")
def read_animals(db: Session = Depends(get_db)):
    animals = db.query(models.Animal).filter(models.Animal.available == True).all()
    return animals

#update an animal by id in the list
@router.put("/animal/{animal_id}")
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


@router.delete("/animals/{id}")
def delete_animal(id: int, db: Session = Depends(get_db)):
    animal = db.query(models.Animal).filter(models.Animal.animal_id == id).first()
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    db.delete(animal)
    db.commit()
    return {"status_code": 200, "detail":"Animal deleted successfully"}


