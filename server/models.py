from sqlalchemy import Enum, Float, Boolean, Text, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(20), unique=True, index=True)
    name = Column(String(20))
    name = Column(Enum)
    img_url = Column(String(100))
    reviews = relationship("review", back_populates="parents")
    token = Column(Text)

#     is_active = Column(Boolean, default=True)


class Review(Base):
    __tablename__="review"

    id = Column(Integer, primary_key=True, index=True)
    user_id = relationship("user", back_populates="child")
    market_id = relationship("market", back_populates="child")
    rate = Column(Integer)
    comment = Column(Text)
    solution = Column(Text)

class Market(Base):
    __tablename__="market"

    id = Column(Integer, primary_key=True, index=True)
    market_name = Column(String(20))
    market_latitude = Column(Float)
    market_longitude = Column(Float)
    phone = Column(String(12))
    review = relationship("review",back_populates="parents")
