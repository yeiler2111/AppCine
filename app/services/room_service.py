from sqlalchemy.ext.asyncio import AsyncSession
from app.models.room import Room
from app.repositories.room_repository import RoomRepository
from app.schemas.room_schema import RoomCreate, RoomUpdate

class RoomService:
    def __init__(self, db: AsyncSession):
        self.repo = RoomRepository(db)

    async def list_rooms(self):
        return await self.repo.get_all()

    async def get_room(self, room_id: int):
        return await self.repo.get_by_id(room_id)

    async def create_room(self, data: RoomCreate):
        new_room = Room(**data.dict())
        return await self.repo.create(new_room)

    async def update_room(self, room_id: int, data: RoomUpdate):
        room = await self.repo.get_by_id(room_id)
        if not room:
            return None
        return await self.repo.update(room, data.dict(exclude_unset=True))

    async def delete_room(self, room_id: int):
        room = await self.repo.get_by_id(room_id)
        if not room:
            return None
        await self.repo.delete(room)
        return room
