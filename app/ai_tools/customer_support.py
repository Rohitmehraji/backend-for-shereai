from openai import AsyncOpenAI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SupportTicket(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    message: str
    priority: Optional[str] = "medium"  # low, medium, high, urgent

@router.post("/analyze-support-ticket")
async def analyze_support_ticket(request: SupportTicket):
    """Analyze support ticket and suggest response"""
    try:
        prompt = f"""
        Analyze this customer support ticket:
        
        From: {request.customer_name} ({request.customer_email})
        Subject: {request.subject}
        Priority: {request.priority}
        
        Message:
        {request.message}
        
        Provide:
        1. Sentiment Analysis (positive, neutral, negative, angry)
        2. Category (technical, billing, feature_request, complaint, question)
        3. Priority Assessment (low, medium, high, urgent)
        4. Suggested Response (professional, empathetic, helpful)
        5. Required Actions (specific steps to resolve)
        6. Escalation Needed? (yes/no and why)
        
        Format your analysis clearly with sections.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a customer support expert who analyzes tickets and provides actionable insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=1000
        )
        
        analysis = response.choices[0].message.content
        
        # Extract sentiment (simple parsing)
        sentiment = "neutral"
        if "negative" in analysis.lower() or "angry" in analysis.lower():
            sentiment = "negative"
        elif "positive" in analysis.lower():
            sentiment = "positive"
        
        return {
            "success": True,
            "analysis": analysis,
            "sentiment": sentiment,
            "tool": "customer_support_ai"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-support-response")
async def generate_support_response(request: dict):
    """Generate professional support response"""
    try:
        message = request.get("message", "")
        
        prompt = f"""
        Generate a professional, empathetic customer support response for this issue:
        
        Customer Issue:
        {message}
        
        Requirements:
        - Be empathetic and understanding
        - Provide clear solution steps
        - Use professional but friendly tone
        - Include next steps or timeline
        - Offer additional help
        - End with positive note
        
        Format as email response.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert customer support representative known for excellent service."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        support_response = response.choices[0].message.content
        
        return {
            "success": True,
            "response": support_response,
            "tool": "customer_support_ai"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
