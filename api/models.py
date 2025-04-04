# models.py
from pydantic import BaseModel

class Production(BaseModel):
    category: str
    product: str
    quantity: float
    unit: str
    measurement: str
    year: int
