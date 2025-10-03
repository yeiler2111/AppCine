from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)

    # Relaciónes
    tickets = relationship("Ticket", back_populates="user")
    payments = relationship("Payment", back_populates="user")


    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
