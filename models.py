from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

#Class structure for creating a new string analysis request
class String_Request(BaseModel):
    value: str = Field(..., description="String to be analyzed")

    #This are the properties of the analyzed string
class String_Properties(BaseModel):
    length: int
    is_palindrome: bool
    unique_chars: int
    word_count: int
    sha256_hash: str
    character_frequency: Dict[str, int]

class String_Record(BaseModel):
    id: str
    value: str
    properties: String_Properties
    created_at: datetime

class Filter_Response(BaseModel):
    data: list[String_Record]
    count: int
    filters_applied: Optional[dict] = None