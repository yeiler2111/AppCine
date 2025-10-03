from pydantic import BaseModel
from decimal import Decimal

class SeatTypePriceBase(BaseModel):
    name: str
    price: Decimal

class SeatTypePriceCreate(SeatTypePriceBase):
    pass

class SeatTypePriceUpdate(BaseModel):
    name: str
    price: Decimal

class SeatTypePriceResponse(SeatTypePriceBase):
    id: int

    class Config:
        from_attributes = True