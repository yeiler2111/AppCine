from pydantic import BaseModel
from typing import Optional, List

class RoomBase(BaseModel):
    name: str
    capacity: int

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None

class RoomResponse(RoomBase):
    id: int
    # Opcional: incluir las sillas asociadas
    # seats: List["SeatResponse"] = []

    class Config:
        from_attributes = True  # en Pydantic v2
