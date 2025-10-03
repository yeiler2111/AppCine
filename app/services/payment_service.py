from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


from app.repositories.payment_repository import PaymentRepository
from app.models.Payment import Payment
from app.enums.payment_status import PaymentStatus
from app.factories.payment_factory import PaymentFactory

from app.observers.payment_observer import PaymentObserver
from app.notify.Email import EmailNotifier, LoggerObserver, MockEmailService

from app.services.ticket_service import TicketService
from app.services.seat_service import SeatService
from app.proxies.payment_proxy import PaymentProxy


class PaymentService:
    def __init__(self, db: AsyncSession, ticket_service: TicketService, seat_service: SeatService):
        self.repo = PaymentRepository(db)
        self.db = db
        self._observers: List[PaymentObserver] = []
        self.ticket_service = ticket_service
        self.seat_service = seat_service

    def attach(self, observer: PaymentObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: PaymentObserver) -> None:
        self._observers.remove(observer)

    async def notify(self, payment: Payment) -> None:
        for observer in self._observers:
            await observer.update(payment)

    async def process_payment(self, ticket_id: int, user_id: int, method: str):
        strategy = PaymentFactory.get_strategy(method)

        proxy = PaymentProxy(strategy, self.ticket_service, self.seat_service)
        proxy_result = await proxy.pay(ticket_id, user_id)

        result = proxy_result["result"]
        price = proxy_result["price"]

        status = PaymentStatus.PAGADO if result["status"] == "success" else PaymentStatus.FALLIDO

        payment = Payment(
            ticket_id=ticket_id,
            user_id=user_id,
            amount=price,
            method=method,
            status=status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        saved_payment = await self.repo.create(payment)

        if status == PaymentStatus.PAGADO:
            self.attach(LoggerObserver())
            self.attach(EmailNotifier(MockEmailService()))
            await self.notify(saved_payment)

        return {"payment": saved_payment, "gateway_result": result}

    async def get_payments_by_user(self, user_id: int):
        return await self.repo.get_by_user_id(user_id)