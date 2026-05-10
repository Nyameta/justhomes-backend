from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.ai_service import get_ai_response
import uuid

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Receives conversation history from the frontend,
    searches for matching properties,
    and returns AI response with property recommendations.
    """
    session_id = request.session_id or str(uuid.uuid4())

    # Convert messages to the format Groq expects
    messages = [
        {"role": m.role, "content": m.content}
        for m in request.messages
    ]

    # Get AI response and matched properties
    ai_response, matched_properties = await get_ai_response(messages)

    return ChatResponse(
        message=ai_response,
        session_id=session_id,
        properties=matched_properties if matched_properties else None,
        lead_prompt=len(matched_properties) > 0,
    )