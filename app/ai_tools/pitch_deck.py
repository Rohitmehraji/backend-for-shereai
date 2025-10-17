from openai import AsyncOpenAI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PitchDeckRequest(BaseModel):
    business_name: str
    tagline: str
    problem: str
    solution: str
    target_market: str
    business_model: str
    competition: str
    traction: str
    team: str
    funding_ask: str

@router.post("/generate-pitch-deck")
async def generate_pitch_deck(request: PitchDeckRequest):
    """Generate investor pitch deck content"""
    try:
        prompt = f"""
        Create a compelling 10-slide investor pitch deck for:
        
        Business: {request.business_name}
        Tagline: {request.tagline}
        Problem: {request.problem}
        Solution: {request.solution}
        Target Market: {request.target_market}
        Business Model: {request.business_model}
        Competition: {request.competition}
        Traction: {request.traction}
        Team: {request.team}
        Funding Ask: {request.funding_ask}
        
        Generate content for these 10 slides with compelling copy:
        
        SLIDE 1: COVER
        - Company name, tagline, presenter info
        
        SLIDE 2: PROBLEM
        - What problem are you solving?
        - Why is it important?
        - Market pain points
        
        SLIDE 3: SOLUTION
        - Your product/service
        - How it solves the problem
        - Key features/benefits
        
        SLIDE 4: MARKET OPPORTUNITY
        - TAM, SAM, SOM
        - Market size and growth
        - Target customer segments
        
        SLIDE 5: PRODUCT/DEMO
        - Product screenshots/demo description
        - Key functionality
        - User experience highlights
        
        SLIDE 6: BUSINESS MODEL
        - How you make money
        - Pricing strategy
        - Unit economics
        
        SLIDE 7: TRACTION
        - Current metrics (users, revenue, growth)
        - Milestones achieved
        - Customer testimonials/case studies
        
        SLIDE 8: COMPETITION
        - Competitive landscape
        - Your unique advantages
        - Market positioning
        
        SLIDE 9: TEAM
        - Founder backgrounds
        - Key team members
        - Advisors/investors
        
        SLIDE 10: FUNDING ASK
        - Amount raising
        - Use of funds breakdown
        - Projected milestones
        
        For each slide, provide:
        - Headline (catchy and clear)
        - 3-5 bullet points with compelling copy
        - Data points or statistics where relevant
        - Call-to-action or key takeaway
        
        Make it investor-ready, data-driven, and persuasive.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a pitch deck expert who has helped raise millions for startups. Create compelling, investor-ready content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3500
        )
        
        pitch_deck_content = response.choices[0].message.content
        
        return {
            "success": True,
            "pitch_deck": pitch_deck_content,
            "slide_count": 10,
            "tool": "pitch_deck_creator"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
