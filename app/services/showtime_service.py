from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.showtime import Showtime
from app.models.ticket import Ticket
from app.models.seat import Seat
from app.repositories.showtime_repository import ShowtimeRepository
from app.schemas.showtime_schema import ShowtimeCreate, ShowtimeUpdate
from app.enums.ticket_status import TicketStatus
from datetime import timedelta
from app.repositories.movie_repository import MovieRepository

class ShowtimeService:
    def __init__(self, db):
        self.db = db
        self.repo = ShowtimeRepository(db)
        self.movie_repo = MovieRepository(db)

    async def list_showtimes(self):
        return await self.repo.get_all()

    async def get_showtime(self, showtime_id: int):
        return await self.repo.get_by_id(showtime_id)

    
    async def create_showtime(self, data: ShowtimeCreate):
        movie = await self.movie_repo.get_by_id(data.movie_id)
        if not movie:
            raise ValueError("La película no existe.")
        
        if not (movie.start_date <= data.start_time.date() <= movie.end_date):
            raise ValueError("La función está fuera del rango de fechas de la película.")
        
        end_time = data.start_time + timedelta(minutes=movie.duration_minutes)

        result = await self.db.execute(
            select(Showtime).where(
                and_(
                    Showtime.room_id == data.room_id,
                    Showtime.start_time < end_time,
                    Showtime.end_time > data.start_time
                )
            )
        )
        overlap = result.scalars().first()
        if overlap:
            raise ValueError("Ya existe otra función en la sala que se cruza en el horario.")

        new_showtime = Showtime(
            movie_id=data.movie_id,
            room_id=data.room_id,
            start_time=data.start_time,
            end_time=end_time
        )
        saved_showtime = await self.repo.create(new_showtime)

        result = await self.db.execute(select(Seat).where(Seat.room_id == data.room_id))
        seats = result.scalars().all()
        if not seats:
            raise ValueError("La sala no tiene asientos configurados.")

        tickets = [
            Ticket(
                showtime_id=saved_showtime.id,
                seat_id=seat.id,
                status=TicketStatus.LIBRE
            )
            for seat in seats
        ]
        self.db.add_all(tickets)
        await self.db.commit()

        return saved_showtime
  
    async def update_showtime(self, showtime_id: int, data: ShowtimeUpdate):
        showtime = await self.repo.get_by_id(showtime_id)
        if not showtime:
            return None

        update_data = data.dict(exclude_unset=True)
        return await self.repo.update(showtime, update_data)

    async def delete_showtime(self, showtime_id: int):
        showtime = await self.repo.get_by_id(showtime_id)
        if not showtime:
            return None
        await self.repo.delete(showtime)
        return showtime
