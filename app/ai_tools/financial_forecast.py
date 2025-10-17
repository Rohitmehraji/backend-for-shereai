from openai import AsyncOpenAI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

router = APIRouter()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FinancialForecastRequest(BaseModel):
    business_name: str
    industry: str
    initial_investment: float
    monthly_revenue_month1: float
    monthly_costs: float
    growth_rate: float  # percentage
    forecast_months: int

@router.post("/financial-forecast")
async def generate_financial_forecast(request: FinancialForecastRequest):
    """Generate financial projections with AI analysis"""
    try:
        # Calculate projections
        projections = []
        cumulative_revenue = 0
        cumulative_costs = 0
        
        for month in range(1, request.forecast_months + 1):
            revenue = request.monthly_revenue_month1 * (1 + request.growth_rate/100) ** (month - 1)
            costs = request.monthly_costs * (1.02 ** (month - 1))  # 2% cost inflation
            profit = revenue - costs
            cumulative_revenue += revenue
            cumulative_costs += costs
            
            projections.append({
                "month": month,
                "revenue": round(revenue, 2),
                "costs": round(costs, 2),
                "profit": round(profit, 2),
                "cumulative_revenue": round(cumulative_revenue, 2),
                "cumulative_profit": round(cumulative_revenue - cumulative_costs, 2)
            })
        
        # Get AI analysis
        prompt = f"""
        Analyze this financial forecast for {request.business_name} in {request.industry}:
        
        Initial Investment: ₹{request.initial_investment:,.2f}
        Starting Monthly Revenue: ₹{request.monthly_revenue_month1:,.2f}
        Monthly Costs: ₹{request.monthly_costs:,.2f}
        Growth Rate: {request.growth_rate}% per month
        Forecast Period: {request.forecast_months} months
        
        Financial Projections (First 12 months):
        {json.dumps(projections[:12], indent=2)}
        
        Provide:
        1. Break-even Analysis (when will they break even?)
        2. Cash Flow Analysis
        3. Key Financial Metrics (ROI, Profit Margin, Burn Rate)
        4. Risk Assessment
        5. Recommendations for financial health
        6. Scenario Analysis (Best, Realistic, Worst case)
        
        Be specific with numbers and actionable insights.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a financial analyst specializing in startup finance and forecasting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=2000
        )
        
        analysis = response.choices[0].message.content
        
        return {
            "success": True,
            "projections": projections,
            "analysis": analysis,
            "summary": {
                "break_even_month": next((p["month"] for p in projections if p["cumulative_profit"] > request.initial_investment), None),
                "total_revenue_forecast": round(cumulative_revenue, 2),
                "total_profit_forecast": round(cumulative_revenue - cumulative_costs, 2)
            },
            "tool": "financial_forecast"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
