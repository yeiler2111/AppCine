from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.showtime_service import ShowtimeService
from app.schemas.showtime_schema import ShowtimeCreate, ShowtimeUpdate, ShowtimeResponse
from app.core.security import get_current_user


router = APIRouter(prefix="/showtimes", tags=["Showtimes"])


@router.get("/", response_model=List[ShowtimeResponse])
async def list_showtimes(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = ShowtimeService(db)
    return await service.list_showtimes()


@router.get("/{showtime_id}", response_model=ShowtimeResponse)
async def get_showtime(showtime_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = ShowtimeService(db)
    showtime = await service.get_showtime(showtime_id)
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime no encontrado")
    return showtime


@router.post("/", response_model=ShowtimeResponse)
async def create_showtime(data: ShowtimeCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Crea una nueva función de cine y genera automáticamente los tickets
    según los asientos de la sala.
    """
    service = ShowtimeService(db)
    return await service.create_showtime(data)


@router.put("/{showtime_id}", response_model=ShowtimeResponse)
async def update_showtime(showtime_id: int, data: ShowtimeUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = ShowtimeService(db)
    updated = await service.update_showtime(showtime_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Showtime no encontrado")
    return updated


@router.delete("/{showtime_id}")
async def delete_showtime(showtime_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = ShowtimeService(db)
    deleted = await service.delete_showtime(showtime_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Showtime no encontrado")
    return {"message": "Showtime eliminado"}
