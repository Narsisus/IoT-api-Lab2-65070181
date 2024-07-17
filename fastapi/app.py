from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router_v1.get('/persons')
async def get_persons(db: Session = Depends(get_db)):
    return db.query(models.Person).all()

@router_v1.get('/persons/{person_id}')
async def get_person(person_id: int, db: Session = Depends(get_db)):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

@router_v1.post('/persons')
async def create_person(person: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    new_person = models.Person(
        first_name=person['first_name'],
        last_name=person['last_name'],
        id_number=person['id_number'],
        birth_date=person['birth_date'],
        gender=person['gender']
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    response.status_code = 201
    return new_person

@router_v1.patch('/persons/{person_id}')
async def update_person(person_id: int, person_update: dict, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()

    for key, value in person_update.items():
        setattr(person, key, value)
    db.commit()
    db.refresh(person)

    return person

@router_v1.delete('/persons/{person_id}')
async def delete_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    db.delete(person)
    db.commit()
    
    return {"message": f"Person with id {person_id} deleted"}

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
