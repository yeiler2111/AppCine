from pydantic import BaseModel
from app.enums.ticket_status import TicketStatus
from typing import Optional

class TicketBase(BaseModel):
    showtime_id: int
    seat_id: int
    status: TicketStatus

class TicketResponse(TicketBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
