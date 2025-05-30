from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, index=True, unique=True,nullable=True)
    password=Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    contact=Column(String, unique=True, nullable=True)
