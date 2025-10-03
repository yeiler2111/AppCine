from pydantic import BaseModel
from typing import Optional
from app.enums.payment_status import PaymentStatus
from app.enums.payment_method import PaymentMethod


class PaymentBase(BaseModel):
    ticket_id: int
    user_id: int
    method: PaymentMethod

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    status: PaymentStatus

    class Config:
        from_attributes  = True
