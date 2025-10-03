from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.Payment import Payment

class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payment: Payment):
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_by_id(self, payment_id: int):
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        return result.scalar_one_or_none()

    async def update(self, payment: Payment, data: dict):
        for k, v in data.items():
            setattr(payment, k, v)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_by_user_id(self, user_id: int):
        result = await self.db.execute(select(Payment).where(Payment.user_id == user_id))
        return result.scalars().all()
    