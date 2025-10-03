from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.movie import Movie

class MovieRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Movie))
        return result.scalars().all()

    async def get_by_id(self, movie_id: int):
        result = await self.db.execute(select(Movie).where(Movie.id == movie_id))
        return result.scalar_one_or_none()

    async def create(self, movie: Movie):
        self.db.add(movie)
        await self.db.commit()
        await self.db.refresh(movie)
        return movie

    async def update(self, movie: Movie, data: dict):
        for key, value in data.items():
            setattr(movie, key, value)
        await self.db.commit()
        await self.db.refresh(movie)
        return movie

    async def delete(self, movie: Movie):
        await self.db.delete(movie)
        await self.db.commit()
