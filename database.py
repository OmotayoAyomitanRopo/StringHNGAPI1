from sqlalchemy.future import select
from db import SessionLocal
from models_sql import Base
from models_sql import StringRecord
from logic import analyze_string

async def create_string(value: str):
    async with SessionLocal() as session:
        # Check for exact match (case-sensitive, no .lower())
        result = await session.execute(
            select(StringRecord).where(StringRecord.value == value.strip())
        )
        if result.scalar():
            return None  # Only return None if exact match exists

        props = analyze_string(value.strip())
        new_record = StringRecord(
            id=props["sha256_hash"],
            value=value.strip(),
            length=props["length"],
            is_palindrome=props["is_palindrome"],
            unique_chars=props["unique_chars"],
            word_count=props["word_count"],
            sha256_hash=props["sha256_hash"],
            character_frequency=props["character_frequency"]
        )
        session.add(new_record)
        await session.commit()
        await session.refresh(new_record)
        return new_record

from sqlalchemy.future import select
from db import SessionLocal
from models_sql import StringRecord

async def get_all_strings():
    async with SessionLocal() as session:
        result = await session.execute(select(StringRecord))
        return result.scalars().all()

async def get_string_by_value(value: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(StringRecord).where(StringRecord.value == value.strip())
        )
        return result.scalar()

async def delete_string(value: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(StringRecord).where(StringRecord.value == value.strip())
        )
        record = result.scalar()
        if not record:
            return False
        await session.delete(record)
        await session.commit()
        return True
