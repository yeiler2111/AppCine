from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.enums.price_seat import PriceSeat

from app.repositories.payment_repository import PaymentRepository
from app.models.Payment import Payment
from app.enums.payment_status import PaymentStatus
from app.factories.payment_factory import PaymentFactory

from app.observers.payment_observer import PaymentObserver
from app.notify.Email import EmailNotifier, LoggerObserver, MockEmailService
from app.services.ticket_service import TicketService
from app.services.seat_service import SeatService


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

        
        ticket = await self.ticket_service.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} no encontrado")

        seat = await self.seat_service.get_seat(ticket.seat_id)
        if not seat:
            raise HTTPException(status_code=404, detail=f"Asiento {ticket.seat_id} no encontrado")

        seat_price_enum = PriceSeat.from_id(seat.seat_type_price_id)
        price = seat_price_enum.price

        
        result = await strategy.pay(price)

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
