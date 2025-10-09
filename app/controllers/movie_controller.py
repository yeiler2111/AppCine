from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.movie_service import MovieService
from app.schemas.movie_schema import MovieCreate, MovieUpdate, MovieResponse
from app.core.security import get_current_user


router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=List[MovieResponse])
async def list_movies(db: AsyncSession = Depends(get_db)):
    service = MovieService(db)
    return await service.list_movies()


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    service = MovieService(db)
    movie = await service.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return movie


@router.post("/", response_model=MovieResponse)
async def create_movie(movie_data: MovieCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = MovieService(db)
    return await service.create_movie(movie_data)


@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: int, movie_data: MovieUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = MovieService(db)
    updated = await service.update_movie(movie_id, movie_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return updated


@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = MovieService(db)
    deleted = await service.delete_movie(movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return {"message": "Película eliminada"}
