from fastapi import APIRouter
from typing import List

router = APIRouter()


@router.get("")
async def get_properties():
    """Returns all properties. Phase 4 adds real data."""
    return []


@router.get("/{property_id}")
async def get_property(property_id: str):
    """Returns a single property by ID."""
    return {"message": f"Property {property_id} coming in Phase 4"}