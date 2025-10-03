from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def list_users(self):
        return await self.repo.get_all()

    async def get_user(self, user_id: int):
        return await self.repo.get_by_id(user_id)

    async def create_user(self, data: UserCreate):
        if await self.repo.get_by_email(data.email):
            raise ValueError("El email ya está registrado.")

        hashed_password = pwd_context.hash(data.password)
        new_user = User(
            name=data.name,
            email=data.email,
            phone=data.phone,
            password_hash=hashed_password
        )
        return await self.repo.create(new_user)

    async def update_user(self, user_id: int, data: UserUpdate):
        user = await self.repo.get_by_id(user_id)
        if not user:
            return None

        update_data = data.dict(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = pwd_context.hash(update_data.pop("password"))

        return await self.repo.update(user, update_data)

    async def delete_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        if not user:
            return None
        await self.repo.delete(user)
        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
