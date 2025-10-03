from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, DECIMAL, TIMESTAMP, UniqueConstraint

from datetime import datetime

from sqlalchemy.orm import relationship


from app.database import Base
from app.enums.ticket_status import TicketStatus


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.LIBRE)

    user = relationship("User", back_populates="tickets")
    payment = relationship("Payment", back_populates="ticket", uselist=False)
    showtime = relationship("Showtime", back_populates="tickets")
    seat = relationship("Seat", back_populates="tickets")

    __table_args__ = (
        UniqueConstraint("showtime_id", "seat_id", name="uq_showtime_seat"),
    )
