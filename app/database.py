import os
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class DatabaseInterface(ABC):
    @abstractmethod
    def get_session(self) -> AsyncSession:
        """Debe devolver una sesión de base de datos."""
        pass


class PostgresDatabase(DatabaseInterface):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgresDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "engine"):
            user = os.getenv("DB_USER", "admin")
            password = os.getenv("DB_PASSWORD", "admin123")
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "5432")
            db = os.getenv("DB_NAME", "appcine")

            url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

            self.engine = create_async_engine(url, echo=True, future=True)
            self.async_session = sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

    def get_session(self):
        return self.async_session()


DB_TYPE = os.getenv("DB_TYPE", "postgres")

if DB_TYPE == "postgres":
    db_instance = PostgresDatabase()

engine = db_instance.engine

async def get_db() -> AsyncSession:
    """Dependencia para inyectar la sesión en FastAPI."""
    async with db_instance.get_session() as session:
        yield session
