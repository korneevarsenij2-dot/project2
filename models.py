from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    balance = Column(Integer, default=500000)
    supercars = relationship("Supercar", back_populates="owner")
    bikes = relationship("Bike", back_populates="owner")


class Supercar(Base):
    __tablename__ = 'supercars'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    owner = relationship("User", back_populates="supercars")

class Bike(Base):
    __tablename__ = 'bikes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    owner = relationship("User", back_populates="bikes")
   