from pydantic import BaseModel
from typing import Optional
from app.schemas.seat_type_price_schema import SeatTypePriceResponse

class SeatBase(BaseModel):
    row: str
    number: int

class SeatCreate(SeatBase):
    room_id: int
    seat_type_price_id: int

class BulkSeatCreate(BaseModel):
    room_id: int
    row: str
    start_number: int
    quantity: int
    seat_type_price_id: int

class SeatUpdate(BaseModel):
    row: Optional[str] = None
    number: Optional[int] = None
    room_id: Optional[int] = None
    seat_type_price_id: Optional[int] = None

class SeatResponse(SeatBase):
    id: int
    room_id: int
    seat_type_price: SeatTypePriceResponse

    class Config:
        from_attributes = True
