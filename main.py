from fastapi import FastAPI, HTTPException, Query, Response
from models import String_Record, String_Request, Filter_Response
from database import create_string, get_all_strings, get_string_by_value, delete_string
from utils import use_filters
import re
import asyncio
from db import init_db

app = FastAPI(title="My HNG String Analysis API", version="1.0")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
def rootendpoint():
    return {"Message": "Welcome to My HNG String Analysis API"}

@app.post("/strings", response_model=String_Record, status_code=201)
async def createstr(req: String_Request):
    if not isinstance(req.value, str):
        raise HTTPException(status_code=422, detail="Invalid data type for must be string")

    record = await create_string(req.value)
    if record is None:
        raise HTTPException(status_code=409, detail="String already exists in the system")

    return {
    "id": record.id,
    "value": record.value,
    "created_at": record.created_at,
    "properties": {
        "length": record.length,
        "is_palindrome": record.is_palindrome,
        "unique_chars": record.unique_chars,
        "word_count": record.word_count,
        "sha256_hash": record.sha256_hash,
        "character_frequency": record.character_frequency
    }
}

@app.get("/strings", response_model=Filter_Response)
async def filtered_strings(
    is_palindrome: bool = Query(None),
    min_length: int = Query(None),
    max_length: int = Query(None),
    word_count: int = Query(None),
    contains_char: str = Query(None)
):
    filters = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_char": contains_char
    }

    raw_data = await get_all_strings()
    filtered = use_filters(raw_data, filters)

    # ✅ Transform each SQLAlchemy object into Pydantic-compatible dict
    transformed = [
        {
            "id": item.id,
            "value": item.value,
            "created_at": item.created_at,
            "properties": {
                "length": item.length,
                "is_palindrome": item.is_palindrome,
                "unique_chars": item.unique_chars,
                "word_count": item.word_count,
                "sha256_hash": item.sha256_hash,
                "character_frequency": item.character_frequency
            }
        }
        for item in filtered
    ]

    return {
        "data": transformed,
        "count": len(transformed),
        "filters_applied": {k: v for k, v in filters.items() if v is not None}
    }

@app.get("/strings", response_model=Filter_Response)
async def filtered_strings(
    is_palindrome: bool = Query(None),
    min_length: int = Query(None),
    max_length: int = Query(None),
    word_count: int = Query(None),
    contains_char: str = Query(None)
):
    filters = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_char": contains_char
    }
    data = await get_all_strings()
    filtered = use_filters(data, filters)
    return {
        "data": filtered,
        "count": len(filtered),
        "filters_applied": {k: v for k, v in filters.items() if v is not None}
    }

@app.get("/strings/{string_value}", response_model=String_Record)
async def getstr(string_value: str):
    record = await get_string_by_value(string_value)
    if not record:
        raise HTTPException(status_code=404, detail="String does not exist in the system")

    return {
        "id": record.id,
        "value": record.value,
        "created_at": record.created_at,
        "properties": {
            "length": record.length,
            "is_palindrome": record.is_palindrome,
            "unique_chars": record.unique_chars,
            "word_count": record.word_count,
            "sha256_hash": record.sha256_hash,
            "character_frequency": record.character_frequency
        }
    }

@app.get("/strings/filter-by-natural-language", response_model=Filter_Response)
async def filter_by_natural_lang(query: str):
    query_lower = query.lower()
    filters = {}

    if "palindrome" in query_lower:
        filters["is_palindrome"] = True

    shorter_match = re.search(r"(shorter|less) than (\d+)", query_lower)
    if shorter_match:
        filters["max_length"] = int(shorter_match.group(2)) - 1

    longer_match = re.search(r"(longer|more) than (\d+)", query_lower)
    if longer_match:
        filters["min_length"] = int(longer_match.group(2)) + 1

    exact_match = re.search(r"(exactly|equal to) (\d+) characters", query_lower)
    if exact_match:
        filters["min_length"] = filters["max_length"] = int(exact_match.group(2))

    contains_match = re.search(r"(containing|includes|has) ['\"]?(\w+)['\"]?", query_lower)
    if contains_match:
        filters["contains_char"] = contains_match.group(2)

    start_match = re.search(r"starting with ['\"]?(\w+)['\"]?", query_lower)
    if start_match:
        filters["starts_with"] = start_match.group(1).lower()

    end_match = re.search(r"ending with ['\"]?(\w+)['\"]?", query_lower)
    if end_match:
        filters["ends_with"] = end_match.group(1).lower()

    if not filters:
        raise HTTPException(status_code=400, detail="Unable to parse natural language query")

    raw_data = await get_all_strings()
    filtered = use_filters(raw_data, filters)

    transformed = [
        {
            "id": item.id,
            "value": item.value,
            "created_at": item.created_at,
            "properties": {
                "length": item.length,
                "is_palindrome": item.is_palindrome,
                "unique_chars": item.unique_chars,
                "word_count": item.word_count,
                "sha256_hash": item.sha256_hash,
                "character_frequency": item.character_frequency
            }
        }
        for item in filtered
    ]

    return {
        "data": transformed,
        "count": len(transformed),
        "filters_applied": filters
    }

@app.delete("/strings/{string_value}", status_code=204)
async def delete_string_value(string_value: str):
    result = await delete_string(string_value)
    if not result:
        raise HTTPException(status_code=404, detail="String does not exist in the system")
    return Response(status_code=204)


""" from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from fastapi.responses import Response
from models import String_Record, String_Properties, String_Request, Filter_Response
from database import create_string, get_all_strings, get_string_by_value, delete_string
from utils import use_filters
import re

app = FastAPI(title="My HNG String Analysis API", version="1.0")


@app.get("/")
def rootendpoint():
    return {"Message": "Welcome to My HNG String Analysis API"}


@app.post("/strings", response_model=String_Record, status_code=201)
def createstr(req: String_Request):
    if not isinstance(req.value, str):
        raise HTTPException(status_code=422, detail="Invalid data type for must be string")
    
    record = create_string(req.value)
    if record is None:
        raise HTTPException(status_code=409, detail="String already exists in the system")
    
    return record

@app.get("/strings/{string_value}", response_model=String_Record)
def getstr(string_value: str):
    record = get_string_by_value(string_value)
    if not record:
        raise HTTPException(status_code=404, detail="String does not exist in the system")
    return record

@app.get("/strings", response_model=Filter_Response)
def filtered_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None),
    max_length: Optional[int] = Query(None),
    word_count: Optional[int] = Query(None),
    contains_char: Optional[str] = Query(None)
):
    filters = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_char": contains_char
    }
    data = get_all_strings()
    filtered = use_filters(data, filters)
    return {
        "data": filtered,
        "count": len(filtered),
        "filters_applied": {k: v for k, v in filters.items() if v is not None}
    }

@app.get("/strings/filter-by-natural-language", response_model=Filter_Response)
def filter_by_natural_lang(query: str):
    query_lower = query.lower()
    filters = {}

    # Palindrome detection
    if any(word in query_lower for word in ["palindrome", "palindromes", "palindromic"]):
        filters["is_palindrome"] = True

    # Single word detection
    if "single word" in query_lower or "only one word" in query_lower:
        filters["word_count"] = 1

    # Length filters
    longer_match = re.search(r"(longer|more) than (\\d+)", query_lower)
    if longer_match:
        filters["min_length"] = int(longer_match.group(2)) + 1

    shorter_match = re.search(r"(shorter|less) than (\\d+)", query_lower)
    if shorter_match:
        filters["max_length"] = int(shorter_match.group(2)) - 1

    exact_match = re.search(r"(exactly|equal to) (\\d+) characters", query_lower)
    if exact_match:
        filters["min_length"] = filters["max_length"] = int(exact_match.group(2))

    # Character containment
    contains_match = re.search(r"(containing|includes|has) ['\"]?(\\w+)['\"]?", query_lower)
    if contains_match:
        filters["contains_char"] = contains_match.group(2)

    if not filters:
        raise HTTPException(status_code=400, detail="Unable to parse natural language query")

    data = get_all_strings()
    filtered = use_filters(data, filters)
    return {
        "data": filtered,
        "count": len(filtered),
        "filters_applied": filters
    }

 """
