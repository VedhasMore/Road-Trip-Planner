import os
import re
import math
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from .state import TripState
from .tools import tools, search_web

load_dotenv()

# Configuration
LLM_MODEL = "llama-3.3-70b-versatile"

def get_api_key():
    # 1. Try environment variable (Local / Streamlit Cloud default)
    api_key = os.environ.get("GROQ_API_KEY")
    
    # 2. Try Streamlit Secrets (Explicitly for Streamlit Cloud)
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass
            
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Please set it in your .env file (local) "
            "or in Streamlit Cloud Secrets (deployment)."
        )
    return api_key

LLM_API_KEY = get_api_key()

# Initialize LLM
llm = ChatGroq(model=LLM_MODEL, api_key=LLM_API_KEY)
llm_with_tools = llm.bind_tools(tools)

def planner_node(state: TripState):
    """Generates the initial draft itinerary based on user input."""
    messages = state['messages']
    
    prompt = f"""You are a Lead Travel Planner.
    Plan a road trip from {state['origin']} to {state['destination']} based on interests: {state['interests']}.
    
    Constraints:
    - Duration: Target exactly {state['requested_duration']} days.
    - Budget: ₹{state['budget']}. Keep this in mind for the pace and type of stops.
    
    Structure the response as a Day-by-Day itinerary."""
    
    response = llm_with_tools.invoke([SystemMessage(content=prompt)] + messages)
    return {
        "messages": [response],
        "draft_itinerary": response.content
    }

def logistics_node(state: TripState):
    """Calculates trip distance and duration using driving heuristics."""
    origin, destination = state['origin'], state['destination']
    
    try:
        search_res = search_web.invoke(f"driving distance from {origin} to {destination} km")
        nums = re.findall(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*km", search_res, re.IGNORECASE)
        one_way_km = float(nums[0].replace(",", "")) if nums else 600.0
    except Exception:
        one_way_km = 600.0
        
    round_trip_km = one_way_km * 2
    days = math.ceil(round_trip_km / 300) # Avg 300km per day for India
    
    return {"distance_km": round_trip_km, "duration_days": days}

def finance_node(state: TripState):
    """Estimates the total trip cost based on distance and duration."""
    distance = state.get('distance_km', 1000.0)
    duration = state.get('requested_duration', state.get('duration_days', 4))
    
    # India-specific constants (2026)
    FUEL_PRICE, MILEAGE = 104, 15
    STAY_COST, FOOD_COST = 3500, 1500
    
    fuel = (distance / MILEAGE) * FUEL_PRICE
    accommodation = (duration - 1) * STAY_COST if duration > 1 else 0
    food_misc = duration * FOOD_COST 
    
    total = fuel + accommodation + food_misc
    return {
        "total_cost_inr": total,
        "fuel_cost": fuel,
        "accommodation_cost": accommodation
    }

def local_expert_node(state: TripState):
    """Enriches the itinerary with local secrets and budget-aware tips."""
    messages = state['messages']
    cost = state.get('total_cost_inr', 0)
    budget = state.get('budget', 0)
    budget_status = "✅ Within Budget" if cost <= budget else "⚠️ Over Budget"
    
    summary = f"""
    # 🇮🇳 Trip Summary
    - **Total Distance**: {state.get('distance_km', 0):.1f} km (Round Trip)
    - **Trip Duration**: {state.get('duration_days', 0)} Days
    - **Target Budget**: ₹{budget:,.0f}
    - **Budget Estimate**: ₹{cost:,.2f} ({budget_status})
      *(Fuel: ~₹{state.get('fuel_cost',0):,.0f}, Stay: ~₹{state.get('accommodation_cost',0):,.0f})*
    ---
    """
    
    prompt = f"""You are the Local Expert. REWRITE the Planner's itinerary into a final masterpiece.
    
    CRITICAL RULES:
    1. NO DISCLAIMERS. Output the FULL, detailed plan.
    2. SUMMARY FIRST: Start exactly with this summary:
    {summary}
    3. BUDGET FIT: User budget is ₹{budget}. Suggest spots accordingly.
    4. ENRICHMENT: Add 2 local restaurants, 1 hidden gem, and 1 cultural fact per day."""
    
    response = llm_with_tools.invoke([SystemMessage(content=prompt)] + messages)
    
    if len(response.content) > 300:
        return {"messages": [response], "itinerary": response.content}
    return {"messages": [response]}

