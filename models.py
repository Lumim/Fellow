# User model
from sqlalchemy import Column, Integer, String, LargeBinary # type: ignore
from database import Base
from typing import List
from pydantic import BaseModel
class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=True)
    type = Column(String(100), nullable=True)
    card_number = Column(String(100), nullable=True)
    mobile_number = Column(String(100), unique=True, nullable=False)
    number_of_visits = Column(String(100), nullable=True)
    profile_img = Column(LargeBinary, nullable=True)
    

class CustomerOfferCalculateTable(Base):
    __tablename__ = "customer_offer_calculate_table"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=True)
    offer_id = Column(Integer, nullable=True)
    restaurant_id = Column(Integer, nullable=True)
    condition_met = Column(String(100), unique=True, nullable=False)
    offer_taken = Column(String(100), nullable=True)



class OfferTable(Base):
    __tablename__ = "offer_table"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(String(100), nullable=True)
    type = Column(String(100), nullable=True)
    details = Column(String(100), nullable=True)
    condition_type = Column(String(100), unique=True, nullable=False)
    condition_value = Column(Integer)
    offer_name = Column(String(100), unique=True, nullable=False)

class Points(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=True)
    available_points = Column(String(100), nullable=True)
    mobile_number = Column(String(100), nullable=True)
    used_points = Column(String(100), unique=True, nullable=False)

class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, index=True)
    profile_img = Column(LargeBinary, nullable=True)
    banner_img = Column(LargeBinary, nullable=True)
    owner_img = Column(LargeBinary, nullable=True)
    rest_name = Column(String(100), nullable=True)
    type = Column(String(100), unique=True, nullable=False)
    rest_mobile_number = Column(String(100), nullable=True)
    backup_number = Column(String(100), nullable=True)
    cvr = Column(String(100), nullable=True)
