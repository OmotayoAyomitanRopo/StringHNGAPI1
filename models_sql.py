from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class StringRecord(Base):
    __tablename__ = "strings"

    # Primary identifier: SHA-256 hash of the string
    id = Column(String, primary_key=True, index=True)

    # Original string value
    value = Column(String, unique=True, nullable=False)

    # Computed properties
    length = Column(Integer, nullable=False)
    is_palindrome = Column(Boolean, nullable=False)
    unique_chars = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    sha256_hash = Column(String, nullable=False)
    character_frequency = Column(JSON, nullable=False)

    # Timestamp of creation
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
