import os
import datetime
from sqlalchemy import create_engine, Integer, String, Column, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


POSTGRES_URI = os.getenv("POSTGRES_URI")
if POSTGRES_URI:
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
    SQLALCHEMY_DATABASE_URL = POSTGRES_URI
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
    )
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./db/npmrd_curator.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Single table for storing data
class Submission(Base):
    __tablename__ = "submission"
    # implicit autoincrement in SQLite
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    session = Column(String, nullable=False)
    doi = Column(String)
    email = Column(String)
    data = Column(Text)
    handled = Column(Boolean, default=False)
