from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ShowtimeBase(BaseModel):
    movie_id: int
    room_id: int
    start_time: datetime


class ShowtimeCreate(ShowtimeBase):
    """Schema para crear un nuevo showtime."""
    pass


class ShowtimeUpdate(BaseModel):
    movie_id: Optional[int] = None
    room_id: Optional[int] = None
    start_time: Optional[datetime] = None


class ShowtimeResponse(ShowtimeBase):
    id: int

    class Config:
        from_attributes  = True 
