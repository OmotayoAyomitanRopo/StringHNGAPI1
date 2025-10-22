from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class StringRecord(Base):
    __tablename__ = "strings"

    id = Column(String, primary_key=True, index=True)  # SHA-256 hash
    value = Column(String, unique=True, nullable=False)
    length = Column(Integer)
    is_palindrome = Column(Boolean)
    unique_chars = Column(Integer)
    word_count = Column(Integer)
    sha256_hash = Column(String)
    character_frequency = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
