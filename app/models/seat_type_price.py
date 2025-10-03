from sqlalchemy import Column, Integer, String, DECIMAL
from app.database import Base
from sqlalchemy.orm import relationship

class SeatTypePrice(Base):
    __tablename__ = "seat_type_prices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)   # Ej: VIP, GENERAL, PAREJA
    price = Column(DECIMAL, nullable=False)

    # Relación con Seat
    seats = relationship("Seat", back_populates="seat_type_price")

    def __repr__(self):
        return f"<SeatTypePrice(name={self.name}, price={self.price})>"
