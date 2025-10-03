from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.room_service import RoomService
from app.schemas.room_schema import RoomCreate, RoomUpdate, RoomResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", response_model=List[RoomResponse])
async def list_rooms(db: AsyncSession = Depends(get_db)):
    service = RoomService(db)
    return await service.list_rooms()

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int, db: AsyncSession = Depends(get_db)):
    service = RoomService(db)
    room = await service.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return room

@router.post("/", response_model=RoomResponse)
async def create_room(room_data: RoomCreate, db: AsyncSession = Depends(get_db)):
    service = RoomService(db)
    return await service.create_room(room_data)

@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(room_id: int, room_data: RoomUpdate, db: AsyncSession = Depends(get_db)):
    service = RoomService(db)
    updated = await service.update_room(room_id, room_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return updated

@router.delete("/{room_id}")
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    service = RoomService(db)
    deleted = await service.delete_room(room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return {"message": "Sala eliminada"}
