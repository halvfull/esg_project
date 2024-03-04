from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from customer import Customer
from models import Base, Customers
from database import engine, SessionLocal
from sqlalchemy.orm import Session


from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append('../') 

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

items = []


@app.get("/")
async def read_all(db : Session = Depends(get_db)):
    return db.query(Customers).all()
 

@app.post("/Customers")
def create_item(item: Customer):
    items.append(item)
    return items


@app.get("/Customers", response_model=list[Customer])
def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/Customers/{item_id}", response_model=Customer)
def get_item(item_id: int) -> Customer:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Customer {item_id} not found")