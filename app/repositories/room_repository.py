from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.room import Room

class RoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Room))
        return result.scalars().all()

    async def get_by_id(self, room_id: int):
        result = await self.db.execute(select(Room).where(Room.id == room_id))
        return result.scalar_one_or_none()

    async def create(self, room: Room):
        self.db.add(room)
        await self.db.commit()
        await self.db.refresh(room)
        return room

    async def update(self, room: Room, data: dict):
        for key, value in data.items():
            setattr(room, key, value)
        await self.db.commit()
        await self.db.refresh(room)
        return room

    async def delete(self, room: Room):
        await self.db.delete(room)
        await self.db.commit()
