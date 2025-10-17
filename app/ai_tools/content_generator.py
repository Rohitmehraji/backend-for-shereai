from openai import AsyncOpenAI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ContentRequest(BaseModel):
    content_type: str  # blog, social, email, product_description, website
    topic: str
    tone: str  # professional, casual, friendly, formal, persuasive
    length: str  # short, medium, long
    keywords: Optional[str] = None
    target_audience: Optional[str] = None

@router.post("/generate-content")
async def generate_content(request: ContentRequest):
    """AI content generation for various formats"""
    try:
        # Determine word count based on length
        word_counts = {
            "short": "200-300 words",
            "medium": "500-700 words",
            "long": "1000-1500 words"
        }
        
        prompt = f"""
        Generate {request.content_type} content with these specifications:
        
        Topic: {request.topic}
        Tone: {request.tone}
        Length: {word_counts.get(request.length, '500-700 words')}
        Keywords: {request.keywords or 'Not specified'}
        Target Audience: {request.target_audience or 'General audience'}
        
        Requirements:
        - Write in {request.tone} tone
        - Make it engaging and valuable
        - Include relevant keywords naturally
        - Optimize for SEO (if blog/website content)
        - Add clear call-to-action at the end
        - Use proper formatting (headings, bullets where appropriate)
        
        Content Type Specific:
        """
        
        if request.content_type == "blog":
            prompt += "\n- Include catchy headline\n- Add meta description\n- Use H2/H3 headings\n- Include introduction and conclusion"
        elif request.content_type == "social":
            prompt += "\n- Keep it concise and engaging\n- Include relevant hashtags\n- Add emoji where appropriate\n- End with strong CTA"
        elif request.content_type == "email":
            prompt += "\n- Subject line\n- Personalized greeting\n- Clear value proposition\n- Strong CTA\n- Professional signature"
        elif request.content_type == "product_description":
            prompt += "\n- Highlight key features and benefits\n- Address pain points\n- Include specifications\n- Add compelling CTA"
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": f"You are a professional content writer skilled in creating {request.content_type} content that engages and converts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )
        
        generated_content = response.choices[0].message.content
        
        return {
            "success": True,
            "content": generated_content,
            "word_count": len(generated_content.split()),
            "content_type": request.content_type,
            "tool": "content_generator"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
