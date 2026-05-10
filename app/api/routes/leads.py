from fastapi import APIRouter
from app.models.schemas import LeadCreate, LeadResponse
from app.services.lead_service import save_lead, generate_whatsapp_url, get_all_leads

router = APIRouter()


@router.post("")
async def capture_lead(lead: LeadCreate):
    """
    Captures lead information from the chat widget.
    Saves to file and returns WhatsApp URL.
    """
    try:
        saved_lead = save_lead(lead)
        whatsapp_url = generate_whatsapp_url(lead)

        return LeadResponse(
            success=True,
            message=f"Thank you {lead.name}! A JustHomes agent will contact you shortly on {lead.phone}.",
            lead_id=saved_lead["id"],
            whatsapp_url=whatsapp_url,
        )
    except Exception as e:
        print(f"Lead capture error: {e}")
        return LeadResponse(
            success=False,
            message="Sorry, something went wrong. Please try again.",
            lead_id=None,
            whatsapp_url=None,
        )


@router.get("")
async def get_leads():
    """
    Returns all captured leads.
    In production this would require authentication.
    """
    leads = get_all_leads()
    return {
        "total": len(leads),
        "leads": leads
    }