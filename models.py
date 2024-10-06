# User model
from sqlalchemy import Column, Integer, String # type: ignore
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String(100), unique=True, nullable=False)
    user_name = Column(String(100), nullable=True)
class UserPoint(Base):
    __tablename__ = "userPoint"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=True)
    mobile_number = Column(String(100), unique=True, nullable=False)
    restaurant_name = Column(String(100), nullable=True)  # Fix the typo here
    points = Column(Integer, nullable=True)
    active=Column(Integer, nullable=True)
    
class RestaurantOfferTable(Base):
    __tablename__ = "restaurant_offer_table"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(100), nullable=True)
    offer_type = Column(String(100), unique=True, nullable=False)
    offer_value = Column(String(100), nullable=True)  # Fix the typo here
    offer_name = Column(Integer, nullable=True)
    points_deduct = Column(Integer, nullable=True)
    active_status=Column(Integer, nullable=True)

class RestaurantPointTable(Base):
    __tablename__ = "restaurant_point_table"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(100), nullable=True)
    product_name = Column(String(100), nullable=False)
    variant = Column(String(100), nullable=True)  # Fix the typo here
    points = Column(Integer, nullable=True)
    points_deduct = Column(Integer, nullable=True)
    active_status=Column(Integer, nullable=True)