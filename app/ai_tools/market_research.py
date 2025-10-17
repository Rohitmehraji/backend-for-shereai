from openai import AsyncOpenAI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MarketResearchRequest(BaseModel):
    industry: str
    target_market: str
    geography: str
    research_focus: str  # "competitor", "customer", "trends", "market_size"

@router.post("/market-research")
async def conduct_market_research(request: MarketResearchRequest):
    """AI-powered market research and analysis"""
    try:
        prompt = f"""
        Conduct comprehensive market research for:
        
        Industry: {request.industry}
        Target Market: {request.target_market}
        Geography: {request.geography}
        Focus: {request.research_focus}
        
        Provide detailed analysis on:
        1. Market Size & Growth (TAM, SAM, SOM)
        2. Key Market Trends (2025-2030)
        3. Customer Demographics & Psychographics
        4. Top 5-10 Competitors Analysis
        5. Market Entry Barriers
        6. Opportunities & Threats
        7. Pricing Landscape
        8. Distribution Channels
        9. Regulatory Considerations
        10. Market Forecast
        
        Use latest 2025 data and provide specific numbers where possible.
        Format with clear sections and bullet points.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a market research analyst with deep industry knowledge and access to market data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=3000
        )
        
        research_report = response.choices[0].message.content
        
        return {
            "success": True,
            "research_report": research_report,
            "tool": "market_research"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
