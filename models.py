# User model
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String(100), unique=True, nullable=False)
    user_name = Column(String(100), nullable=True)
