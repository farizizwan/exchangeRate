from pydantic import BaseModel

class Rates(BaseModel):
    convertFrom: str
    to: str
    rates: float
    amount: float
    source: str

class History(BaseModel):
    maximum: float
    minumum: float
    rates: dict
    source: str

class Error(BaseModel):
    errorCode: int
    errorMessage: str

