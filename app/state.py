import operator
from typing import Annotated, List, TypedDict, Optional
from langchain_core.messages import BaseMessage

class TripState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    origin: str
    destination: str
    interests: str
    itinerary: Optional[str]
    distance_km: float
    duration_days: int
    total_cost_inr: float
    fuel_cost: float
    accommodation_cost: float
    budget: float
    requested_duration: int
    draft_itinerary: Optional[str]
