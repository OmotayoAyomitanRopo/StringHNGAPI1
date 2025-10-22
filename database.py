from typing import Dict
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
