from pydantic import BaseModel
from datetime import date
from typing import Optional

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date   
    end_date: date     
    duration_minutes: int  

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_minutes: Optional[int] = None

class MovieResponse(MovieBase):
    id: int

    class Config:
        from_attributes = True
