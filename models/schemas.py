from pydantic import BaseModel, field_validator
from typing import Optional, List
from enum import Enum


class Intent(str, Enum):
    BUY     = "buy"
    RENT    = "rent"
    UNKNOWN = "unknown"

class PropertyType(str, Enum):
    APARTMENT  = "apartment"
    HOUSE      = "house"
    VILLA      = "villa"
    STUDIO     = "studio"
    LAND       = "land"
    ANY        = "any"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    session_id: Optional[str] = None
    properties: Optional[List[dict]] = None
    lead_prompt: Optional[bool] = False

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    intent: Intent = Intent.UNKNOWN
    budget: Optional[str] = None
    location_preference: Optional[str] = None
    timeline: Optional[str] = None
    message: Optional[str] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = v.replace(" ", "").replace("-", "")
        if cleaned.startswith("+254"):
            cleaned = cleaned[1:]
        if cleaned.startswith("0"):
            cleaned = "254" + cleaned[1:]
        if not cleaned.startswith("254") or len(cleaned) != 12:
            raise ValueError("Enter a valid Kenyan phone number")
        return cleaned

class LeadResponse(BaseModel):
    success: bool
    message: str
    lead_id: Optional[str] = None
    whatsapp_url: Optional[str] = None

    