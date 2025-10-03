import asyncio
from app.database import engine, Base

from app import models 

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # borra
        await conn.run_sync(Base.metadata.create_all) #crea
        print("Tablas creadas con éxito.")


if __name__ == "__main__":
    asyncio.run(init_models())
