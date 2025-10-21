from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from models import String_Record, String_Properties, String_Request, Filter_Response
from database import create_string, get_all_strings, get_string_by_value, delete_string
from utils import use_filters

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
    print(">>> FILTER endpoint hit with query:", query_lower)
    filters = {}

    if "palindromic" in query_lower:
        filters["is_palindrome"] = True
    if "single word" in query_lower:
        filters["word_count"] = 1
        
    if "shorter than" in query_lower:
        match = re.search(r"shorter than (\d+)", query_lower)
        if match:
            filters["max_length"] = int(match.group(1)) - 1

    if "exactly" in query_lower and "characters" in query_lower:
        match = re.search(r"exactly (\d+)", query_lower)
        if match:
            filters["min_length"] = filters["max_length"] = int(match.group(1))

    if "longer than" in query_lower:
        import re
        match = re.search(r"longer than (\d+)", query_lower)
        if match:
            filters["min_length"] = int(match.group(1)) + 1
    if "containing the letter" in query_lower:
        import re
        match = re.search(r"letter (\w)", query_lower)
        if match:
            filters["contains_char"] = match.group(1)

    if not filters:
        raise HTTPException(status_code=400,detail="Unable to parse natural language query")
    
    data = get_all_strings()
    filtered = use_filters(data, filters)

    return {
        "data": filtered,
        "count": len(filtered),
        "filters_applied": filters
    }

@app.delete("/strings/{string_value}", status_code=204)
def delete_string_value(string_value: str):
    clean_value = string_value.strip()
    result = delete_string(clean_value)
    if not result:
        raise HTTPException(status_code=404, detail="String does not exist in the system")
    return

