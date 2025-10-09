from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.payment_service import PaymentService
from app.services.ticket_service import TicketService
from app.services.seat_service import SeatService
from app.schemas.payment_schema import PaymentCreate, PaymentResponse
from app.core.security import get_current_user


router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse)
async def process_payment(payment_data: PaymentCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    ticket_service = TicketService(db)
    seat_service = SeatService(db)

    service = PaymentService(db, ticket_service, seat_service)

    try:
        result = await service.process_payment(
            ticket_id=payment_data.ticket_id,
            user_id=payment_data.user_id,
            method=payment_data.method,
        )
        return result["payment"]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/by-user/{user_id}", response_model=List[PaymentResponse])
async def get_user_payments(user_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    ticket_service = TicketService(db)
    seat_service = SeatService(db)
    service = PaymentService(db, ticket_service, seat_service)
    return await service.get_payments_by_user(user_id)
