
from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.payment import razorpay_integration, stripe_integration
from app.ai_tools import (
    business_plan,
    market_research,
    financial_forecast,
    pitch_deck,
    content_generator,
    chatbot_builder,
    customer_support,
    task_manager,
    time_management
)

app = FastAPI(
    title="Sphere.AI Backend API",
    description="AI-powered tools for founders and entrepreneurs",
    version="1.0.0"
)

# CORS Configuration - Allow your frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-for-sphere-ai-k5z9-mvebyc1c1-rohits-projects-6d1c0263.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "*"  # Remove this in production, only for testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all AI tool routers
app.include_router(business_plan.router, prefix="/api/tools", tags=["Business Plan"])
app.include_router(market_research.router, prefix="/api/tools", tags=["Market Research"])
app.include_router(financial_forecast.router, prefix="/api/tools", tags=["Financial Forecast"])
app.include_router(pitch_deck.router, prefix="/api/tools", tags=["Pitch Deck"])
app.include_router(content_generator.router, prefix="/api/tools", tags=["Content Generator"])
app.include_router(chatbot_builder.router, prefix="/api/tools", tags=["Chatbot Builder"])
app.include_router(customer_support.router, prefix="/api/tools", tags=["Customer Support"])
app.include_router(task_manager.router, prefix="/api/tools", tags=["Task Manager"])
app.include_router(time_management.router, prefix="/api/tools", tags=["Time Management"])

app.include_router(razorpay_integration.router, prefix="/api/payment", tags=["Payment"])
app.include_router(stripe_integration.router, prefix="/api/payment", tags=["Payment"])


@app.get("/")
async def root():
    return {
        "message": "Sphere.AI API - AI Tools for Founders",
        "version": "1.0.0",
        "status": "active",
        "tools_available": 9,
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Sphere.AI Backend"
    }
