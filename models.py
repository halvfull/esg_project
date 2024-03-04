from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base

class Customers(Base):
    __tablename__ ="customers"
    id = Column(Integer, primary_key=True, index=True)
    year_month =Column(Integer) 
    customerno = Column(String)
    customername = Column(String)
    countrycd = Column(String)
    nace = Column(Integer)
    currencycd = Column(String)
    total_exposure = Column(Float)
    nace_level_4 = Column(String)
    is_green= Column(Boolean)


    