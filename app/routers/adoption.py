from .. import models,schema
from fastapi import FastAPI, HTTPException,Depends,status,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
   tags=['adoption']
)


# link in models between animal and adoption model
@router.get("/adoption/{id}")
def read_adoption(id: int, db: Session = Depends(get_db)):
    adoption = db.query(models.Adoption).filter(models.Adoption.adoption_id == id)
    if not adoption:
        raise HTTPException(status_code=404, detail="Adoption not found")
    return adoption

# Retrieve all adopt

@router.get("/adoption/")
def read_adoptions(db: Session=Depends(get_db)):
    adoptions = db.query(models.Adoption).all()
    return adoptions

@router.post("/adoption/newadoption",status_code=status.HTTP_201_CREATED)
def create_adoption(adoption: schema.Adoption, db: Session = Depends(get_db)):
    new_adoption = models.Adoption(adopter_name=adoption.adopter_name, adopter_email=adoption.adopter_email, 
    adopter_phone=adoption.adopter_phone, animal_id=adoption.animal_id)
    db.add(new_adoption)
    db.commit()
    db.refresh(new_adoption)
    return new_adoption

@router.delete("/adoption/{id}")
def delete_adoption(id: int, db: Session = Depends(get_db)):
    adoption = db.query(models.Adoption).filter(models.Adoption.adoption_id == id).first()
    if adoption is None:
        raise HTTPException(status_code=404, detail="Adoption not found")
    db.delete(adoption)
    db.commit()
    return {"status_code": 200, "detail":"Adoption deleted successfully"}
