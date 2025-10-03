from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
from app.database import Base


from sqlalchemy.orm import relationship
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    duration_minutes =  Column(Integer, nullable=False)
    
    
    showtimes = relationship("Showtime", back_populates="movie")


    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}')>"
