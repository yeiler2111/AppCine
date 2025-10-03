from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.seat import Seat

class SeatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Seat))
        return result.scalars().all()

    async def get_by_id(self, seat_id: int):
        result = await self.db.execute(select(Seat).where(Seat.id == seat_id))
        return result.scalar_one_or_none()

    async def get_by_room_and_row(self, room_id: int, row: str):
        result = await self.db.execute(
            select(Seat).where(Seat.room_id == room_id, Seat.row == row)
        )
        return result.scalars().all()

    async def create(self, seat: Seat):
        self.db.add(seat)
        await self.db.commit()
        await self.db.refresh(seat)
        return seat

    async def bulk_create(self, seats: list[Seat]):
        self.db.add_all(seats)
        await self.db.commit()
        for seat in seats:
            await self.db.refresh(seat)
        return seats

    async def update(self, seat: Seat, data: dict):
        for key, value in data.items():
            setattr(seat, key, value)
        await self.db.commit()
        await self.db.refresh(seat)
        return seat

    async def delete(self, seat: Seat):
        await self.db.delete(seat)
        await self.db.commit()
    
    async def get_by_room(self, room_id: int):
        result = await self.db.execute(
            select(Seat).where(Seat.room_id == room_id)
        )
        return result.scalars().all()
