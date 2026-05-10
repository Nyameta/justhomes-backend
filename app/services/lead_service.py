import json
import os
import uuid
from datetime import datetime
from app.models.schemas import LeadCreate


LEADS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "leads.json"
)


def load_leads() -> list:
    """Load existing leads from file."""
    if not os.path.exists(LEADS_FILE):
        return []
    try:
        with open(LEADS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception:
        return []


def save_lead(lead: LeadCreate) -> dict:
    """
    Save a new lead to the JSON file.
    Returns the saved lead with ID and timestamp.
    """
    leads = load_leads()

    new_lead = {
        "id": str(uuid.uuid4())[:8].upper(),
        "name": lead.name,
        "phone": lead.phone,
        "email": lead.email or "",
        "intent": lead.intent,
        "budget": lead.budget or "",
        "location_preference": lead.location_preference or "",
        "timeline": lead.timeline or "",
        "message": lead.message or "",
        "status": "new",
        "created_at": datetime.utcnow().isoformat(),
    }

    leads.append(new_lead)

    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2)

    return new_lead


def get_all_leads() -> list:
    """Returns all captured leads."""
    return load_leads()


def generate_whatsapp_url(lead: LeadCreate) -> str:
    """
    Generates a pre-filled WhatsApp message URL for the agent.
    """
    from app.core.config import settings
    number = settings.WHATSAPP_NUMBER.replace("+", "")
    message = (
        f"Hello JustHomes! My name is {lead.name}. "
        f"I am interested in {lead.intent}ing a property"
        f"{' in ' + lead.location_preference if lead.location_preference else ''}. "
        f"My budget is {lead.budget or 'flexible'}. "
        f"Please contact me on {lead.phone}."
    )
    import urllib.parse
    return f"https://wa.me/{number}?text={urllib.parse.quote(message)}"