from groq import Groq
from app.core.config import settings
from app.services.property_service import search_properties, format_properties_for_ai, extract_search_params

client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """You are Nyumba, an AI-powered real estate assistant for JustHomes — a premium Kenyan real estate platform.

Your personality:
- Friendly, professional, and knowledgeable
- You understand Kenyan real estate deeply
- You know Nairobi neighborhoods like Westlands, Kilimani, Karen, Syokimau, Eastleigh, Parklands, Lavington, Muthaiga, Runda, Gigiri, Kileleshwa, Langata, South B, South C, Kasarani, Ruaka, Kitisuru, Ngong, Kerarapon
- You understand Kenyan pricing (millions for sale, thousands per month for rent)
- You can respond in English or Swahili depending on what the user uses
- You are concise — never give very long responses

Your job:
- Help users find properties to buy or rent in Kenya
- When property data is provided to you, recommend those specific properties
- Ask clarifying questions about budget, location, bedrooms, amenities
- Give honest advice about neighborhoods and value for money
- Capture lead information naturally (name, phone, email)
- Suggest when a JustHomes agent should be involved

Kenyan context you know:
- Luxury areas: Karen, Muthaiga, Runda, Gigiri, Lavington
- Mid range areas: Westlands, Kilimani, Kileleshwa, Parklands
- Affordable areas: Syokimau, Ruaka, Kasarani, Langata, South B, South C, Ngong
- Property prices: studios from KSh 2M, 1BR from KSh 4M, 3BR from KSh 8M to 50M+
- Rental prices: studios from KSh 15K/mo, 1BR from KSh 25K/mo, 3BR from KSh 45K/mo+
- Always mention prices in Kenya Shillings (KSh)

Important rules:
- When property listings are provided, ALWAYS recommend them specifically by name and price
- Keep responses under 150 words unless explaining something complex
- End responses with a helpful follow up question when appropriate
- If user seems ready to connect with an agent, ask for their name and phone number
"""


async def get_ai_response(messages: list) -> tuple[str, list]:
    """
    Sends conversation history to Groq and returns AI response.
    Also searches for relevant properties based on the last message.
    Returns (ai_response, matched_properties)
    """
    try:
        # Get the last user message
        last_user_message = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break

        # Extract search parameters from the message
        search_params = extract_search_params(last_user_message)

        # Search for matching properties
        matched_properties = []
        property_context = ""

        if search_params:
            matched_properties = search_properties(**search_params)
            if matched_properties:
                property_context = "\n\nPROPERTY LISTINGS FOUND:\n"
                property_context += format_properties_for_ai(matched_properties)
                property_context += "\nPlease recommend these specific properties to the user."

        # Build messages with property context
        enhanced_system = SYSTEM_PROMPT + property_context

        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": enhanced_system},
                *messages
            ],
            max_tokens=400,
            temperature=0.7,
        )

        return response.choices[0].message.content, matched_properties

    except Exception as e:
        print(f"Groq API error: {e}")
        return "Samahani, I am having trouble right now. Please try again in a moment.", []