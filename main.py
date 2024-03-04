from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from customer import Customer
from models import Base, Customers
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import plotly.express as px
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func




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

@app.get("/customer-green-distribution")
def customer_green_distribution(db: Session = Depends(get_db)):
    fig = generate_green_customers_plot(db)
    return fig.to_json()

@app.get("/total-exposure-by-country")
def total_exposure_by_country(db: Session = Depends(get_db)):
    fig = total_exposure_by_country_plot(db)
    return fig.to_json()
''' 
@app.get("/green_customers_by_nace_plot")
def total_exposure_by_country(db: Session = Depends(get_db)):
    fig = total_exposure_by_country_plot(db)
    return fig.to_json()
'''

@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customers).filter(Customers.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def total_exposure_by_country_plot(db: Session):
    # Aggregate total exposure by country
    query = db.query(
        Customers.countrycd,
        func.sum(Customers.total_exposure).label('total_exposure')
    ).group_by(Customers.countrycd).all()

    countries = [result.countrycd for result in query]
    exposures = [result.total_exposure for result in query]

    fig = px.bar(x=countries, y=exposures, labels={'x': 'Country', 'y': 'Total Exposure'},
                 title="Total Exposure by Country")
    return fig


def generate_green_customers_plot(db: Session):
    # Fetching all customers to see who is green and who is not
    customer_data = db.query(Customers.is_green).all()
    # Count the number of green and not green customers
    green_count = sum(1 for customer in customer_data if customer.is_green)
    not_green_count = len(customer_data) - green_count
    
    # Data for plotting
    data = {
        'Category': ['Green', 'Not Green'],
        'Count': [green_count, not_green_count]
    }
    
    # Generate a bar plot
    fig = px.bar(data, x='Category', y='Count', title="Distribution of Green Customers")
    return fig