import os
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finance.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    transactions = relationship("Transaction", back_populates="owner")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    category = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates='transactions')


Base.metadata.create_all(bind=engine)
