import asyncio
from datetime import date
from app.database import engine, Base
from app.models import User, Movie, Room, Seat, SeatTypePrice
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("✔️ Tablas borradas y creadas con éxito.")

    async with async_session() as session:
        # Usuarios
        user1 = User(name="Admin", email="admin@cine.com", phone="123456789", password_hash="hashed_admin")
        user2 = User(name="Cliente", email="cliente@cine.com", phone="987654321", password_hash="hashed_cliente")
        session.add_all([user1, user2])

        # Películas
        movie1 = Movie(
            title="Matrix",
            description="Ciencia ficción distópica",
            start_date=date(2025, 10, 10),
            end_date=date(2025, 12, 10),
            duration_minutes=130
        )
        movie2 = Movie(
            title="Interstellar",
            description="Viajes espaciales y agujeros negros",
            start_date=date(2025, 11, 1),
            end_date=date(2025, 12, 20),
            duration_minutes=170
        )
        session.add_all([movie1, movie2])

        # Sala
        room = Room(name="Sala 1", capacity=20)
        session.add(room)
        await session.flush()  # Para obtener room.id

        # Tipos de asiento
        vip = SeatTypePrice(name="VIP", price=25.00)
        general = SeatTypePrice(name="General", price=15.00)
        pareja = SeatTypePrice(name="Pareja", price=30.00)
        session.add_all([vip, general, pareja])
        await session.flush()  # Para obtener los IDs

        # Sillas
        seat_list = []
        for row in ['A', 'B']:
            for number in range(1, 6):
                seat_type = vip if row == 'A' else general
                seat = Seat(room_id=room.id, row=row, number=number, seat_type_price_id=seat_type.id)
                seat_list.append(seat)

        session.add_all(seat_list)

        await session.commit()
        print("✅ Datos iniciales insertados con éxito.")

if __name__ == "__main__":
    asyncio.run(init_models())
