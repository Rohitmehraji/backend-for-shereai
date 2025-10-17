from openai import AsyncOpenAI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

router = APIRouter()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[str] = "medium"
    estimated_hours: Optional[float] = None

class TaskList(BaseModel):
    tasks: List[Task]

@router.post("/prioritize-tasks")
async def prioritize_tasks(request: TaskList):
    """AI-powered task prioritization"""
    try:
        tasks_text = "\n".join([
            f"- {task.title} (Deadline: {task.deadline or 'None'}, Priority: {task.priority}, Est. Hours: {task.estimated_hours or 'Unknown'})"
            for task in request.tasks
        ])
        
        prompt = f"""
        Analyze and prioritize these tasks using the Eisenhower Matrix and other productivity frameworks:
        
        {tasks_text}
        
        Provide:
        1. Prioritized Task List (with reasoning)
        2. Task Categories:
           - URGENT & IMPORTANT (Do First)
           - IMPORTANT but NOT URGENT (Schedule)
           - URGENT but NOT IMPORTANT (Delegate if possible)
           - NEITHER (Eliminate or Do Later)
        3. Suggested Schedule (when to do each task)
        4. Time Management Tips
        5. Tasks that can be batched together
        6. Recommended focus order for maximum productivity
        
        Consider deadlines, estimated time, and stated priorities.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a productivity expert and time management coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=1500
        )
        
        prioritization = response.choices[0].message.content
        
        return {
            "success": True,
            "prioritization": prioritization,
            "task_count": len(request.tasks),
            "tool": "task_manager_ai"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-schedule")
async def generate_schedule(request: TaskList):
    """Generate optimized daily/weekly schedule"""
    try:
        tasks_text = "\n".join([
            f"- {task.title} ({task.estimated_hours or 2}h)"
            for task in request.tasks
        ])
        
        prompt = f"""
        Create an optimized schedule for these tasks:
        
        {tasks_text}
        
        Assumptions:
        - Work day: 9 AM to 6 PM (with 1h lunch)
        - Focus blocks: 90-minute deep work sessions
        - Include breaks every 2 hours
        - Most important tasks in morning (peak productivity)
        
        Provide:
        1. Day-by-day schedule
        2. Time blocking suggestions
        3. Energy level considerations
        4. Buffer time for unexpected items
        5. Review/reflection time
        
        Format as a clear weekly calendar.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a scheduling expert who creates realistic, productive schedules."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=1200
        )
        
        schedule = response.choices[0].message.content
        
        return {
            "success": True,
            "schedule": schedule,
            "tool": "task_manager_ai"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
