from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False) 
    capacity = Column(Integer, nullable=False) 

    seats = relationship("Seat", back_populates="room")
    showtimes = relationship("Showtime", back_populates="room")

    def __repr__(self):
        return f"<Room(id={self.id}, name='{self.name}', capacity={self.capacity})>"
