from sqlalchemy import create_engine, Integer, String, Column, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./npmrd_curator.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

## Single table for storing data
class Submission(Base):
    __tablename__ = "submission"
    # implicit autoincrement in SQLite
    id = Column(Integer, primary_key=True, index=True)
    session = Column(String, nullable=False)
    doi = Column(String)
    email = Column(String)
    data = Column(Text)
