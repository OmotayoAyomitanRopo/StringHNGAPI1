from db import SessionLocal
from models_sql import StringRecord
from logic import analyze_string
from sqlalchemy.future import select
import hashlib

async def create_string(value: str):
    async with SessionLocal() as session:
        clean_value = value.strip().lower()
        properties = analyze_string(clean_value)
        hash_id = properties["sha256_hash"]

        result = await session.execute(select(StringRecord).where(StringRecord.id == hash_id))
        if result.scalar():
            return None

        new_record = StringRecord(
            id=hash_id,
            value=clean_value,
            length=properties["length"],
            is_palindrome=properties["is_palindrome"],
            unique_chars=properties["unique_chars"],
            word_count=properties["word_count"],
            sha256_hash=hash_id,
            character_frequency=properties["character_frequency"]
        )
        session.add(new_record)
        await session.commit()
        await session.refresh(new_record)
        return new_record

async def get_string_by_value(value: str):
    async with SessionLocal() as session:
        clean_value = value.strip().lower()
        hash_id = hashlib.sha256(clean_value.encode()).hexdigest()
        result = await session.execute(select(StringRecord).where(StringRecord.id == hash_id))
        return result.scalar()

async def delete_string(value: str):
    async with SessionLocal() as session:
        clean_value = value.strip().lower()
        hash_id = hashlib.sha256(clean_value.encode()).hexdigest()
        result = await session.execute(select(StringRecord).where(StringRecord.id == hash_id))
        record = result.scalar()
        if record:
            await session.delete(record)
            await session.commit()
            return True
        return False

async def get_all_strings():
    async with SessionLocal() as session:
        result = await session.execute(select(StringRecord))
        return result.scalars().all()


""" from typing import Dict
from logic import analyze_string
from datetime import datetime
import hashlib

# An empty DB that will serve as in-memeory database
DB: Dict[str, dict] = {}

# Helper to normalize string inconsistencies
def normalize_string(value: str) -> str:
    return value.strip()

# Function definition to store analyzed property
def create_string(value: str):
    clean_value = normalize_string(value)
    # calling the string analyzer function to retrieve the
    # Property of the input string
    properties = analyze_string(clean_value)

    # Extracting the SHA-256 hash, whiich will be used as a unique property
    hash_id = properties["sha256_hash"]

    if hash_id in DB: #If the unque identifier (hash_id) already exist in database
        return None
    
    DB[hash_id] = {
        "id": hash_id,
        "value": clean_value,
        "properties": properties,
        "created_at": datetime.utcnow()
    }
    return DB[hash_id]

#It will retrieve it properties from database
def get_string_by_value(value: str):
    clean_value = normalize_string(value)
    hash_id = hashlib.sha256(clean_value.encode()).hexdigest()
    return DB.get(hash_id)

# It will delete a string from the database
def delete_string(value: str):
    clean_value = normalize_string(value)
    hash_id = hashlib.sha256(clean_value.encode()).hexdigest()
    return DB.pop(hash_id, None)

#This will return all the dictionary value in the in-memory.
def get_all_strings():
    return list(DB.values())
 """