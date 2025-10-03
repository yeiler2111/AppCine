from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DECIMAL, UniqueConstraint
from app.database import Base
from app.enums.seat_type import SeatType
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from app.database import Base
from sqlalchemy.orm import relationship

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    row = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    seat_type_price_id = Column(Integer, ForeignKey("seat_type_prices.id"), nullable=False)

    room = relationship("Room", back_populates="seats")
    tickets = relationship("Ticket", back_populates="seat")
    seat_type_price = relationship("SeatTypePrice", lazy="joined") 

    __table_args__ = (UniqueConstraint("room_id", "row", "number", name="uq_room_row_number"),)
