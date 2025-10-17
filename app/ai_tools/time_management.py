from openai import AsyncOpenAI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os

router = APIRouter()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class WorkPattern(BaseModel):
    typical_work_hours: str
    main_responsibilities: List[str]
    common_distractions: List[str]
    goals: str

@router.post("/analyze-time-usage")
async def analyze_time_usage(request: WorkPattern):
    """Analyze work patterns and suggest improvements"""
    try:
        prompt = f"""
        Analyze this work pattern and provide time management recommendations:
        
        Work Hours: {request.typical_work_hours}
        Main Responsibilities: {', '.join(request.main_responsibilities)}
        Common Distractions: {', '.join(request.common_distractions)}
        Goals: {request.goals}
        
        Provide:
        1. Time Audit Analysis
        2. Productivity Bottlenecks Identified
        3. Time Wasters to Eliminate
        4. Recommended Time Blocking Schedule
        5. Focus Time Optimization
        6. Meeting Optimization Suggestions
        7. Energy Management Tips
        8. Tools/Techniques to Implement
        9. 30-day Improvement Plan
        10. Key Metrics to Track
        
        Be specific and actionable.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a time management coach specializing in productivity optimization for founders and executives."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=2000
        )
        
        analysis = response.choices[0].message.content
        
        return {
            "success": True,
            "analysis": analysis,
            "tool": "time_management_ai"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calendar-optimization")
async def optimize_calendar(request: dict):
    """Optimize calendar and suggest time blocks"""
    try:
        meetings = request.get("meetings", [])
        work_style = request.get("work_style", "mixed")  # maker, manager, mixed
        
        prompt = f"""
        Optimize this calendar for maximum productivity:
        
        Current Meetings: {len(meetings)} per week
        Work Style: {work_style}
        
        Provide:
        1. Ideal Weekly Calendar Template
        2. Focus Time Blocks (when to schedule deep work)
        3. Meeting Guidelines (when to schedule, how long)
        4. Buffer Time Recommendations
        5. Day Themes (e.g., Monday = Strategy, Tuesday = Execution)
        6. Break Schedule
        7. No-Meeting Zones
        8. Calendar Rules to Follow
        
        Optimize for energy levels and productivity patterns.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a calendar optimization expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=1500
        )
        
        optimization = response.choices[0].message.content
        
        return {
            "success": True,
            "optimization": optimization,
            "tool": "time_management_ai"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
