from fastapi import HTTPException
from app.services.ticket_service import TicketService
from app.services.seat_service import SeatService
from app.enums.price_seat import PriceSeat

class PaymentProxy:
    def __init__(self, strategy, ticket_service: TicketService, seat_service: SeatService):
        self._strategy = strategy
        self._ticket_service = ticket_service
        self._seat_service = seat_service

    async def pay(self, ticket_id: int, user_id: int) -> dict:
        ticket = await self._ticket_service.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} no encontrado")

        seat = await self._seat_service.get_seat(ticket.seat_id)
        if not seat:
            raise HTTPException(status_code=404, detail=f"Asiento {ticket.seat_id} no encontrado")

        seat_price_enum = PriceSeat.from_id(seat.seat_type_price_id)
        price = seat_price_enum.price

        result = await self._strategy.pay(price)

        return {"result": result, "price": price}
