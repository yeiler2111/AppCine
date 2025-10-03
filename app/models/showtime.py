from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, TIMESTAMP, DateTime
from app.database import Base
from sqlalchemy.orm import relationship


class Showtime(Base):
    __tablename__ = "showtimes"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    movie = relationship("Movie", back_populates="showtimes")
    room = relationship("Room", back_populates="showtimes")
    tickets = relationship("Ticket", back_populates="showtime")

