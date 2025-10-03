from app.repositories.ticket_repository import TicketRepository

class TicketService:
    def __init__(self, db):
        self.repo = TicketRepository(db)

    async def get_tickets_by_showtime(self, showtime_id: int):
        return await self.repo.get_by_showtime(showtime_id)

    async def get_tickets_by_movie(self, movie_id: int):
        return await self.repo.get_by_movie(movie_id)

    async def get_tickets_by_room(self, room_id: int):
        return await self.repo.get_by_room(room_id)
    
    async def get_by_id(self, id_tiket: int):
        return await self.repo.get_by_id(id_tiket)
