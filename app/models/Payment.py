from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DECIMAL, TIMESTAMP
from datetime import datetime

from sqlalchemy.orm import relationship


from app.database import Base
from app.enums.payment_status import PaymentStatus

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), unique=True)
    amount = Column(DECIMAL)
    method = Column(String)
    status = Column(Enum(PaymentStatus))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="payment")
    user = relationship("User", back_populates="payments")

