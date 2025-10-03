from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.seat import Seat
from app.repositories.seat_repository import SeatRepository
from app.schemas.seat_schema import SeatCreate, SeatUpdate, BulkSeatCreate
from app.redis_client import redis_instance

class SeatService:
    def __init__(self, db: AsyncSession):
        self.repo = SeatRepository(db)
        self.redis = redis_instance.get_client()


    async def list_seats(self):
        return await self.repo.get_all()

    async def get_seat(self, seat_id: int):
        return await self.repo.get_by_id(seat_id)

    async def get_seats_by_showtime(self, room_id: int, showtime_id: int):
        """
        Lista los asientos de una sala con su estado de reserva temporal
        (según Redis).
        """
        seats = await self.repo.get_by_room(room_id)
        seats_with_status = []
        
        for seat in seats:
            key = f"seat:{showtime_id}:{seat.id}"
            reserved = await self.redis.get(key) is not None
            seats_with_status.append({
                "id": seat.id,
                "row": seat.row,
                "number": seat.number,
                "room_id": seat.room_id,
                "seat_type_price": seat.seat_type_price,
                "is_reserved": reserved
            })
        
        return seats_with_status

    async def create_seat(self, data: SeatCreate):
        new_seat = Seat(**data.dict())
        return await self.repo.create(new_seat)

    async def create_bulk_seats(self, data: BulkSeatCreate):
        existing_seats = await self.repo.get_by_room_and_row(data.room_id, data.row)
        existing_numbers = {s.number for s in existing_seats}

        to_create = []
        conflicts = []
        for i in range(data.start_number, data.start_number + data.quantity):
            if i in existing_numbers:
                conflicts.append(i)
            else:
                to_create.append(
                    Seat(
                        room_id=data.room_id,
                        row=data.row,
                        number=i,
                        seat_type_price_id=data.seat_type_price_id
                    )
                )

        if conflicts:
            raise HTTPException(
                status_code=400,
                detail=f"Asientos ya existen en fila {data.row}: {conflicts}"
            )

        return await self.repo.bulk_create(to_create)

    async def update_seat(self, seat_id: int, data: SeatUpdate):
        seat = await self.repo.get_by_id(seat_id)
        if not seat:
            return None
        return await self.repo.update(seat, data.dict(exclude_unset=True))

    async def delete_seat(self, seat_id: int):
        seat = await self.repo.get_by_id(seat_id)
        if not seat:
            return None
        await self.repo.delete(seat)
        return seat
    
    async def get_seats_by_room(self, room_id: int):   
        return await self.repo.get_by_room(room_id)
