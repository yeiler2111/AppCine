from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.showtime import Showtime

class ShowtimeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Showtime))
        return result.scalars().all()

    async def get_by_id(self, showtime_id: int):
        result = await self.db.execute(
            select(Showtime).where(Showtime.id == showtime_id)
        )
        return result.scalar_one_or_none()

    async def create(self, showtime: Showtime):
        self.db.add(showtime)
        await self.db.commit()
        await self.db.refresh(showtime)
        return showtime

    async def update(self, showtime: Showtime, data: dict):
        for key, value in data.items():
            setattr(showtime, key, value)
        await self.db.commit()
        await self.db.refresh(showtime)
        return showtime

    async def delete(self, showtime: Showtime):
        await self.db.delete(showtime)
        await self.db.commit()
