from pydantic import BaseModel

class Customer(BaseModel):
    id: int
    year_month: int
    customerno: str
    customername: str
    countrycd: str
    nace: int
    currencycd: str
    total_exposure: float
    nace_level_4: str
    is_green: bool