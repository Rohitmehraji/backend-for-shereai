from openai import AsyncOpenAI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import json
import os

router = APIRouter()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatbotConfig(BaseModel):
    bot_name: str
    business_name: str
    business_description: str
    common_questions: List[str]
    tone: str  # friendly, professional, casual
    language: str  # english, hindi, mixed

class ChatMessage(BaseModel):
    message: str
    bot_config_id: int

@router.post("/create-chatbot-config")
async def create_chatbot_config(request: ChatbotConfig):
    """Create chatbot configuration"""
    try:
        # Generate system prompt for the chatbot
        system_prompt = f"""
        You are {request.bot_name}, an AI assistant for {request.business_name}.
        
        Business Description: {request.business_description}
        
        Your role:
        - Answer customer questions about {request.business_name}
        - Be {request.tone} in your responses
        - Communicate in {request.language}
        - Provide helpful, accurate information
        - If you don't know something, say so and offer to connect them with a human
        
        Common Questions You Should Know:
        {json.dumps(request.common_questions, indent=2)}
        
        Always be polite, helpful, and represent {request.business_name} professionally.
        """
        
        # Generate sample responses for common questions
        sample_responses = {}
        for question in request.common_questions[:5]:  # Limit to 5
            response_prompt = f"As {request.bot_name} for {request.business_name}, answer this question in a {request.tone} tone: {question}"
            
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": response_prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            sample_responses[question] = response.choices[0].message.content
        
        return {
            "success": True,
            "bot_config": {
                "bot_name": request.bot_name,
                "system_prompt": system_prompt,
                "sample_responses": sample_responses
            },
            "embedding_code": f"""
            <!-- Add this to your website -->
            <script>
              window.sphereAIChatbot = {{
                botName: "{request.bot_name}",
                businessName: "{request.business_name}",
                configId: "your-config-id-here"
              }};
            </script>
            <script src="https://cdn.sphere-ai.com/chatbot.js"></script>
            """,
            "tool": "chatbot_builder"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chatbot-respond")
async def chatbot_respond(request: ChatMessage):
    """Get chatbot response to user message"""
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful business assistant. Be friendly and professional."},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        bot_response = response.choices[0].message.content
        
        return {
            "success": True,
            "response": bot_response,
            "timestamp": "2025-10-17T11:16:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
