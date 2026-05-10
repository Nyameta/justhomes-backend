from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, properties, leads, health
from app.core.config import settings

app = FastAPI(
    title="JustHomes AI API",
    description="AI-powered real estate assistant for Kenya",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,      prefix="/api",            tags=["Health"])
app.include_router(chat.router,        prefix="/api/chat",       tags=["Chat"])
app.include_router(properties.router,  prefix="/api/properties", tags=["Properties"])
app.include_router(leads.router,       prefix="/api/leads",      tags=["Leads"])


@app.get("/")
async def root():
    return {
        "service": "JustHomes AI API",
        "version": "1.0.0",
        "status": "running"
    }