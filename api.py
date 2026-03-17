from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from src.core.planner import TravelPlanner

load_dotenv()

app = FastAPI(title="AI Travel Planner API")


class PlanRequest(BaseModel):
    city: str
    interests: str  # comma-separated, e.g. "food, museums, parks"


class PlanResponse(BaseModel):
    city: str
    interests: list[str]
    itinerary: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/plan", response_model=PlanResponse)
def plan(request: PlanRequest):
    if not request.city or not request.interests:
        raise HTTPException(status_code=400, detail="city and interests are required")

    planner = TravelPlanner()
    planner.set_city(request.city)
    planner.set_interests(request.interests)
    itinerary = planner.create_itineary()

    return PlanResponse(
        city=request.city,
        interests=planner.interests,
        itinerary=itinerary,
    )
