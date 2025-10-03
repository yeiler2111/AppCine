from sqlalchemy.ext.asyncio import AsyncSession
from app.models.movie import Movie
from app.repositories.movie_repository import MovieRepository
from app.schemas.movie_schema import MovieCreate, MovieUpdate

class MovieService:
    def __init__(self, db: AsyncSession):
        self.repo = MovieRepository(db)

    async def list_movies(self):
        return await self.repo.get_all()

    async def get_movie(self, movie_id: int):
        return await self.repo.get_by_id(movie_id)

    async def create_movie(self, data: MovieCreate):

        new_movie = Movie(
            title=data.title,
            description=data.description,
            start_date=data.start_date,
            end_date=data.end_date,
            duration_minutes=data.duration_minutes,
        )
        return await self.repo.create(new_movie)

    async def update_movie(self, movie_id: int, data: MovieUpdate):
        movie = await self.repo.get_by_id(movie_id)
        if not movie:
            return None
        update_data = data.dict(exclude_unset=True)
        return await self.repo.update(movie, update_data)

    async def delete_movie(self, movie_id: int):
        movie = await self.repo.get_by_id(movie_id)
        if not movie:
            return None
        await self.repo.delete(movie)
        return movie
