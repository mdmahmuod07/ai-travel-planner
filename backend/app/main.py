import json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from app.config import settings
from app.schemas.travel import TravelRequest, TripRequest, TravelPlanResponse, RefineRequest
from app.agents.orchestrator import orchestrator
from app.services.pdf_service import generate_markdown_plan

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "app": settings.PROJECT_NAME, "version": "1.0.0"}

@app.post(f"{settings.API_V1_STR}/plan", response_model=TravelPlanResponse)
async def create_travel_plan(request: TravelRequest):
    try:
        plan = await orchestrator.generate_trip_plan(request)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(f"{settings.API_V1_STR}/plan/stream")
async def create_travel_plan_stream(request: TravelRequest):
    """
    Streams Server-Sent Events (SSE) detailing each agent's execution log in real-time,
    concluding with the final JSON payload.
    """
    async def event_generator():
        queue = asyncio.Queue()

        async def log_cb(agent_id: str, message: str, status: str):
            await queue.put({
                "type": "log",
                "data": {
                    "agent_id": agent_id,
                    "message": message,
                    "status": status
                }
            })

        async def run_pipeline():
            try:
                plan = await orchestrator.generate_trip_plan(request, log_callback=log_cb)
                await queue.put({
                    "type": "result",
                    "data": plan.model_dump()
                })
            except Exception as e:
                await queue.put({
                    "type": "error",
                    "data": {"message": str(e)}
                })

        asyncio.create_task(run_pipeline())

        while True:
            item = await queue.get()
            yield f"data: {json.dumps(item)}\n\n"
            if item["type"] in ["result", "error"]:
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post(f"{settings.API_V1_STR}/plan/refine", response_model=TravelPlanResponse)
async def refine_travel_plan(refine_req: RefineRequest):
    try:
        updated_plan = await orchestrator.refine_trip_plan(refine_req)
        return updated_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(f"{settings.API_V1_STR}/export/markdown")
async def export_markdown(plan: TravelPlanResponse):
    md_content = generate_markdown_plan(plan)
    headers = {
        'Content-Disposition': f'attachment; filename="{plan.destination.lower()}_itinerary.md"'
    }
    return Response(content=md_content, media_type="text/markdown", headers=headers)

@app.get(f"{settings.API_V1_STR}/presets")
def get_preset_trips():
    return [
        {
            "title": "5 Days in Tokyo, Japan",
            "destination": "Tokyo, Japan",
            "duration_days": 5,
            "target_budget": 50000.0,
            "currency": "INR",
            "travel_style": "Budget",
            "budget": "Budget",
            "companions": "Couple",
            "interests": ["Food", "History", "Nature"],
            "dietary_restrictions": ["Vegetarian"]
        },
        {
            "title": "5 Days in Istanbul, Turkey",
            "destination": "Istanbul, Turkey",
            "duration_days": 5,
            "target_budget": 75000.0,
            "currency": "INR",
            "travel_style": "Moderate",
            "budget": "Moderate",
            "companions": "Couple",
            "interests": ["History", "Architecture", "Food", "Scenic Waterways"],
            "dietary_restrictions": []
        },
        {
            "title": "5 Days in Paris, France",
            "destination": "Paris, France",
            "duration_days": 5,
            "target_budget": 200000.0,
            "currency": "INR",
            "travel_style": "Luxury",
            "budget": "Luxury",
            "companions": "Couple",
            "interests": ["Art", "History", "Food", "Architecture"],
            "dietary_restrictions": []
        },
        {
            "title": "6 Days in Bali, Indonesia",
            "destination": "Bali, Indonesia",
            "duration_days": 6,
            "target_budget": 30000.0,
            "currency": "INR",
            "travel_style": "Budget",
            "budget": "Budget",
            "companions": "Solo",
            "interests": ["Nature", "Wellness", "Culture"],
            "dietary_restrictions": ["Vegan"]
        }
    ]
