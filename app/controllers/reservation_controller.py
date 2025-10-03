from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from app.services.reservation_service import ReservationService

router = APIRouter(prefix="/reservations", tags=["Reservations"])

class ReserveSeatsRequest(BaseModel):
    showtime_id: int
    seat_ids: List[int]
    user_id: int

class ReleaseSeatsRequest(BaseModel):
    showtime_id: int
    seat_ids: List[int]
    user_id: int


@router.post("/reserve")
async def reserve_seats(data: ReserveSeatsRequest):
    service = ReservationService()
    return await service.reserve_seats(
        showtime_id=data.showtime_id,
        seat_ids=data.seat_ids,
        user_id=data.user_id
    )

@router.post("/release")
async def release_seats(data: ReleaseSeatsRequest):
    service = ReservationService()
    return await service.release_seats(
        showtime_id=data.showtime_id,
        seat_ids=data.seat_ids,
        user_id=data.user_id
    )

@router.get("/availability/{showtime_id}/{seat_id}")
async def check_availability(showtime_id: int, seat_id: int):
    service = ReservationService()
    available = await service.check_availability(showtime_id, seat_id)
    return {"seat_id": seat_id, "available": available}
