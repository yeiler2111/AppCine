from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.ticket_service import TicketService
from app.schemas.ticket_schema import TicketResponse
from app.core.security import get_current_user


router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/by-showtime/{showtime_id}", response_model=List[TicketResponse])
async def get_tickets_by_showtime(showtime_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = TicketService(db)
    return await service.get_tickets_by_showtime(showtime_id)

@router.get("/by-movie/{movie_id}", response_model=List[TicketResponse])
async def get_tickets_by_movie(movie_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = TicketService(db)
    return await service.get_tickets_by_movie(movie_id)

@router.get("/by-room/{room_id}", response_model=List[TicketResponse])
async def get_tickets_by_room(room_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = TicketService(db)
    return await service.get_tickets_by_room(room_id)
