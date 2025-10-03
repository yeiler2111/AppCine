from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ticket import Ticket
from app.models.showtime import Showtime

class TicketRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_showtime(self, showtime_id: int):
        result = await self.db.execute(
            select(Ticket).where(Ticket.showtime_id == showtime_id)
        )
        return result.scalars().all()

    async def get_by_movie(self, movie_id: int):
        result = await self.db.execute(
            select(Ticket).join(Ticket.showtime).where(Showtime.movie_id == movie_id)
        )
        return result.scalars().all()

    async def get_by_room(self, room_id: int):
        result = await self.db.execute(
            select(Ticket).join(Ticket.showtime).where(Showtime.room_id == room_id)
        )
        return result.scalars().all()

    async def get_by_id(self, ticket_id: int):
        result = await self.db.execute(
            select(Ticket).where(Ticket.id == ticket_id)
        )
        return result.scalar_one_or_none()



    