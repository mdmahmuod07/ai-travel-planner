from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TravelRequest(BaseModel):
    destination: str = Field(..., example="Tokyo, Japan")
    origin: Optional[str] = Field("New York, USA", example="New York, USA")
    start_date: Optional[str] = Field(None, example="2026-10-10")
    end_date: Optional[str] = Field(None, example="2026-10-17")
    duration_days: int = Field(5, ge=1, le=30, example=5)
    target_budget: Optional[float] = Field(None, example=50000.0)
    currency: str = Field("INR", example="INR")
    travel_style: str = Field("Moderate", example="Moderate")  # Budget, Moderate, Luxury
    budget: Optional[str] = Field("Moderate", example="Moderate")  # Budget, Moderate, Luxury
    companions: str = Field("Couple", example="Solo, Couple, Family, Friends")
    dietary_restrictions: List[str] = Field(default_factory=list, example=["Vegetarian"])
    interests: List[str] = Field(default_factory=list, example=["Food", "History", "Nature", "Shopping"])
    special_requests: Optional[str] = Field("", example="Prefer bullet train travel and quiet hotels")

TripRequest = TravelRequest

class ActivityItem(BaseModel):
    time_slot: str  # Morning, Afternoon, Evening
    title: str
    venue_name: Optional[str] = None
    neighborhood: Optional[str] = None
    location: str
    duration: str
    estimated_cost: str
    description: str = ""
    tips: Optional[str] = None
    category: Optional[str] = "Sightseeing"
    search_query: Optional[str] = None  # e.g. "Hagia Sophia, Sultanahmet, Istanbul"
    lat: Optional[float] = None
    lng: Optional[float] = None

class DayItinerary(BaseModel):
    day_number: int
    date_label: Optional[str] = None
    theme: str
    summary: str
    activities: List[ActivityItem]
    daily_estimated_cost: str

ItineraryDay = DayItinerary

class AccommodationOption(BaseModel):
    name: str
    type: str  # Hotel, Hostel, Resort, Boutique
    neighborhood: str
    price_per_night: str
    rating: str
    why_recommended: str
    lat: Optional[float] = None
    lng: Optional[float] = None

class RestaurantRecommendation(BaseModel):
    name: str
    cuisine: str
    meal_type: str  # Breakfast, Lunch, Dinner, Snack
    neighborhood: str
    price_range: str
    must_try_dish: str
    dietary_friendly: List[str] = []
    lat: Optional[float] = None
    lng: Optional[float] = None

class BudgetBreakdown(BaseModel):
    accommodation: str
    dining: str
    activities_and_tours: str
    local_transport: str
    miscellaneous: str
    total_estimated: str
    currency: str = "INR"
    target_budget: Optional[float] = None
    saving_tips: List[str] = []

class PackingCategory(BaseModel):
    category_name: str
    items: List[str]

class TravelSafetyTips(BaseModel):
    weather_summary: str
    visa_and_entry: str
    local_customs: List[str]
    currency_and_payment_tips: str
    electrical_specs: Optional[str] = None
    transit_tips: Optional[str] = None
    embassy_info: Optional[str] = None
    emergency_contacts: Optional[List[str]] = Field(default_factory=list)  # Deprecated

TravelSafetyGuide = TravelSafetyTips

class AgentStepLog(BaseModel):
    agent_id: str
    agent_name: str
    status: str  # pending, working, completed, error
    message: str
    timestamp: str

class TravelPlanResponse(BaseModel):
    trip_id: str
    destination: str
    duration_days: int
    overview: str
    best_time_to_visit: str
    itinerary: List[DayItinerary]
    accommodations: List[AccommodationOption]
    dining: List[RestaurantRecommendation]
    budget_breakdown: BudgetBreakdown
    packing_checklist: List[PackingCategory]
    travel_tips: TravelSafetyTips
    agent_logs: List[AgentStepLog] = []

TripPlan = TravelPlanResponse

class RefineRequest(BaseModel):
    current_plan: TravelPlanResponse
    user_instruction: str = Field(..., example="Make day 2 more budget friendly and add a museum")
