from pydantic import BaseModel

class Production_or_Commercialization(BaseModel):
    category: str
    product: str
    quantity: float
    unit: str
    measurement: str
    year: int
