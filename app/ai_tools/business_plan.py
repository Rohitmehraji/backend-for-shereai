from openai import AsyncOpenAI
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class BusinessPlanRequest(BaseModel):
    business_name: str
    industry: str
    description: str
    target_market: str
    revenue_model: str
    funding_needed: Optional[str] = None

@router.post("/generate-business-plan")
async def generate_business_plan(request: BusinessPlanRequest):
    """Generate comprehensive business plan using GPT-4"""
    try:
        prompt = f"""
        Create a comprehensive business plan for:
        
        Business Name: {request.business_name}
        Industry: {request.industry}
        Description: {request.description}
        Target Market: {request.target_market}
        Revenue Model: {request.revenue_model}
        Funding Needed: {request.funding_needed or 'Not specified'}
        
        Generate a detailed business plan with the following sections:
        
        1. EXECUTIVE SUMMARY (2-3 paragraphs)
        2. COMPANY DESCRIPTION (detailed overview)
        3. MARKET ANALYSIS
           - Target Market Size
           - Customer Demographics
           - Market Trends
           - Competitive Landscape
        4. ORGANIZATION & MANAGEMENT
           - Organizational Structure
           - Key Team Members Needed
        5. PRODUCTS/SERVICES
           - Detailed Description
           - Unique Value Proposition
           - Competitive Advantages
        6. MARKETING & SALES STRATEGY
           - Marketing Channels
           - Customer Acquisition Strategy
           - Sales Funnel
        7. FINANCIAL PROJECTIONS (5 years)
           - Revenue Projections
           - Cost Structure
           - Break-even Analysis
           - Funding Requirements
        8. RISK ANALYSIS
           - Key Risks
           - Mitigation Strategies
        
        Make it professional, data-driven, and investor-ready. Use real market insights.
        Format with clear headings and bullet points where appropriate.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert business consultant who creates professional, investor-ready business plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        business_plan = response.choices[0].message.content
        
        return {
            "success": True,
            "business_plan": business_plan,
            "word_count": len(business_plan.split()),
            "tool": "business_plan_generator"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating business plan: {str(e)}")
