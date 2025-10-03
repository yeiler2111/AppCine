from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.seat_service import SeatService
from app.schemas.seat_schema import SeatCreate, SeatUpdate, SeatResponse, BulkSeatCreate

router = APIRouter(prefix="/seats", tags=["Seats"])

@router.get("/", response_model=List[SeatResponse])
async def list_seats(db: AsyncSession = Depends(get_db)):
    service = SeatService(db)
    return await service.list_seats()

@router.get("/{seat_id}", response_model=SeatResponse)
async def get_seat(seat_id: int, db: AsyncSession = Depends(get_db)):
    service = SeatService(db)
    seat = await service.get_seat(seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="Silla no encontrada")
    return seat

@router.get("/room/{room_id}", response_model=List[SeatResponse])
async def get_seats_by_room(room_id: int, db: AsyncSession = Depends(get_db)):
    service = SeatService(db)
    return await service.get_seats_by_room(room_id)

@router.get("/room/{room_id}/showtime/{showtime_id}")
async def get_seats_by_showtime(
    room_id: int,
    showtime_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene los asientos de una sala (`room_id`) con el estado de disponibilidad
    para un showtime específico (`showtime_id`).
    """
    service = SeatService(db)
    return await service.get_seats_by_showtime(room_id, showtime_id)

@router.post("/", response_model=SeatResponse)
async def create_seat(seat_data: SeatCreate, db: AsyncSession = Depends(get_db)):
    service = SeatService(db)
    return await service.create_seat(seat_data)

@router.post("/bulk", response_model=List[SeatResponse])
async def create_bulk_seats(bulk_data: BulkSeatCreate, db: AsyncSession = Depends(get_db)):
    service = SeatService(db)
    return await service.create_bulk_seats(bulk_data)

@router.put("/{seat_id}", response_model=SeatResponse)
async def update_seat(seat_id: int, seat_data: SeatUpdate, db: AsyncSession = Depends(get_db)):
    service = SeatService(db)
    updated = await service.update_seat(seat_id, seat_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Silla no encontrada")
    return updated

@router.delete("/{seat_id}")
async def delete_seat(seat_id: int, db: AsyncSession = Depends(get_db)):
    service = SeatService(db)
    deleted = await service.delete_seat(seat_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Silla no encontrada")
    return {"message": "Silla eliminada"}


