import json
import os
from typing import List, Optional
from app.models.schemas import Property, Intent, PropertyType


def load_properties() -> List[dict]:
    """Load properties from JSON file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "properties.json")
    with open(file_path, "r") as f:
        return json.load(f)


def search_properties(
    intent: Optional[str] = None,
    neighborhood: Optional[str] = None,
    max_price: Optional[int] = None,
    min_price: Optional[int] = None,
    bedrooms: Optional[int] = None,
    amenities: Optional[List[str]] = None,
    property_type: Optional[str] = None,
) -> List[dict]:
    """
    Search and filter properties based on criteria.
    Returns matching properties sorted by relevance.
    """
    properties = load_properties()
    results = []

    for prop in properties:
        score = 0

        # Filter by intent (buy/rent)
        if intent and intent != "unknown":
            if prop["intent"] != intent:
                continue
            score += 30

        # Filter by max price
        if max_price and prop["price"] > max_price:
            continue

        # Filter by min price
        if min_price and prop["price"] < min_price:
            continue

        # Filter by bedrooms
        if bedrooms:
            if prop["bedrooms"] == bedrooms:
                score += 25
            elif abs(prop["bedrooms"] - bedrooms) == 1:
                score += 10

        # Filter by neighborhood
        if neighborhood:
            if neighborhood.lower() in prop["neighborhood"].lower():
                score += 30
            elif neighborhood.lower() in prop["location"].lower():
                score += 15

        # Filter by property type
        if property_type and property_type != "any":
            if prop["type"] == property_type:
                score += 15

        # Filter by amenities
        if amenities:
            prop_amenities = [a.lower() for a in prop["amenities"]]
            for amenity in amenities:
                if amenity.lower() in prop_amenities:
                    score += 10

        # Boost featured properties
        if prop.get("is_featured"):
            score += 5

        prop["match_score"] = score
        results.append(prop)

    # Sort by match score
    results.sort(key=lambda x: x["match_score"], reverse=True)

    # Return top 3 results
    return results[:3]


def format_properties_for_ai(properties: List[dict]) -> str:
    """
    Formats property data as text for the AI to read and recommend.
    """
    if not properties:
        return "No properties found matching those criteria."

    text = "Here are the available properties I found:\n\n"
    for i, prop in enumerate(properties, 1):
        text += f"{i}. {prop['title']}\n"
        text += f"   Price: {prop['price_display']}\n"
        text += f"   Type: {prop['bedrooms']} bed, {prop['bathrooms']} bath {prop['type']}\n"
        text += f"   Location: {prop['location']}\n"
        text += f"   Amenities: {', '.join(prop['amenities'])}\n"
        text += f"   About: {prop['description']}\n\n"

    return text


def extract_search_params(message: str) -> dict:
    """
    Extracts search parameters from a user message using simple keyword matching.
    Phase 4 uses keywords. Phase 8 can use AI extraction for better accuracy.
    """
    message_lower = message.lower()
    params = {}

    # Extract intent
    if any(word in message_lower for word in ["rent", "rental", "renting", "lease"]):
        params["intent"] = "rent"
    elif any(word in message_lower for word in ["buy", "purchase", "buying", "own"]):
        params["intent"] = "buy"

    # Extract bedrooms
    for num, words in {
        1: ["1 bed", "one bed", "1br", "one br", "1 bedroom"],
        2: ["2 bed", "two bed", "2br", "two br", "2 bedroom"],
        3: ["3 bed", "three bed", "3br", "three br", "3 bedroom"],
        4: ["4 bed", "four bed", "4br", "four br", "4 bedroom"],
        5: ["5 bed", "five bed", "5br", "five br", "5 bedroom"],
    }.items():
        if any(word in message_lower for word in words):
            params["bedrooms"] = num
            break

    # Extract neighborhoods
    neighborhoods = [
        "westlands", "kilimani", "karen", "syokimau", "lavington",
        "muthaiga", "runda", "gigiri", "kileleshwa", "langata",
        "south b", "south c", "kasarani", "ruaka", "kitisuru",
        "parklands", "ngong", "kerarapon", "eastleigh", "roysambu"
    ]
    for neighborhood in neighborhoods:
        if neighborhood in message_lower:
            params["neighborhood"] = neighborhood
            break

    # Extract price (looks for numbers followed by M or K)
    import re
    price_match = re.search(r'(\d+(?:\.\d+)?)\s*m(?:illion)?', message_lower)
    if price_match:
        params["max_price"] = int(float(price_match.group(1)) * 1_000_000)

    rent_match = re.search(r'(\d+(?:\.\d+)?)\s*k(?:sh)?(?:\s*per\s*month)?', message_lower)
    if rent_match:
        params["max_price"] = int(float(rent_match.group(1)) * 1_000)

    # Extract amenities
    amenity_keywords = ["gym", "pool", "swimming", "parking", "garden", "security", "generator"]
    found_amenities = [a for a in amenity_keywords if a in message_lower]
    if found_amenities:
        params["amenities"] = found_amenities

    return params