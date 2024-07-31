from unicodedata import category
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
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

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'],description=book['description'], summary=book['summary'], categories=book['categories'], is_published=book['is_published'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book_update: dict, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    for key, value in book_update.items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)

    return book
@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.delete(book)
    db.commit()
    
    return {"message": f"Book with id {book_id} deleted"}

@router_v1.get('/cafes')
async def get_cafes(db: Session = Depends(get_db)):
    return db.query(models.Cafe).all()

@router_v1.get('/cafes/{cafe_id}')
async def get_cafe(cafe_id: int, db: Session = Depends(get_db)):
    return db.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()

@router_v1.post('/cafes')
async def create_cafe(cafe: dict, response: Response, db: Session = Depends(get_db)):

    newcafe = models.Cafe(name=cafe['name'], price=cafe['price'], comments=cafe['comments'])
    db.add(newcafe)
    db.commit()
    db.refresh(newcafe)
    response.status_code = 201
    return newcafe

@router_v1.patch('/cafes/{cafe_id}')
async def update_cafe(cafe_id: int, cafe_update: dict, db: Session = Depends(get_db)):
    cafe = db.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()

    for key, value in cafe_update.items():
        setattr(cafe, key, value)
    db.commit()
    db.refresh(cafe)

    return cafe

@router_v1.delete('/cafes/{cafe_id}')
async def delete_cafe(cafe_id: int, db: Session = Depends(get_db)):
    cafe = db.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()
    db.delete(cafe)
    db.commit()
    
    return {"message": f"Cafe with id {cafe_id} deleted"}


@router_v1.get('/orders')

async def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router_v1.get('/orders/{order_id}')
async def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

@router_v1.post('/orders')
async def create_order(order: dict, response: Response, db: Session = Depends(get_db)):
    try:
        neworder = models.Order(
            total_order=order['total_order'], 
            total_price=order['total_price'], 
            comments=order['comments'], 
            status=order['status']
        )
        db.add(neworder)
        db.commit()
        db.refresh(neworder)
        response.status_code = 201
        return neworder
    except Exception as e:
        response.status_code = 400
        return {"message": f"เกิดข้อผิดพลาด: {str(e)}"}

@router_v1.patch('/orders/{order_id}')
async def update_order(order_id: int, order_update: dict, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    for key, value in order_update.items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)

    return order

@router_v1.delete('/orders/{order_id}')
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    db.delete(order)
    db.commit()
    
    return {"message": f"Order with id {order_id} deleted"}

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
