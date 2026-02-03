import streamlit as st
import os
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Multi-Agent Road Trip Planner", page_icon="🚗", layout="wide")

# Import the graph from main.py (now in the same directory)
try:
    from main import graph
except ImportError as e:
    st.error(f"Failed to import graph: {e}")
    st.stop()

st.title("🚗 Multi-Agent Road Trip Planner")
st.markdown("Powered by **LangGraph**, **Groq**, and **DuckDuckGo**")

# Debug info (can be removed later)
with st.expander("System Info"):
    st.write(f"CWD: {os.getcwd()}")
    st.write(f"Has API Key: {'GROQ_API_KEY' in os.environ or 'GROQ_API_KEY' in st.secrets}")

with st.sidebar:
    st.header("Trip Details")
    origin = st.text_input("Start Location", "New York")
    destination = st.text_input("Destination", "Boston")
    interests = st.text_area("Interests", "History, Local Food, Museums")
    budget = st.number_input("Budget (₹)", min_value=1000, value=25000, step=1000)
    requested_duration = st.number_input("Trip Duration (Days)", min_value=1, value=4, step=1)
    plan_button = st.button("Plan My Trip")

if plan_button:
    if not origin or not destination:
        st.error("Please provide both start and destination.")
    else:
        st.info("Agents are working on your itinerary... This may take a minute.")
        
        # Prepare Input
        initial_input = {
            "messages": [HumanMessage(content=f"Plan a road trip from {origin} to {destination}. Interests: {interests}")],
            "origin": origin,
            "destination": destination,
            "interests": interests,
            "budget": float(budget),
            "requested_duration": int(requested_duration)
        }
        
        # Run graph
        try:
            status_container = st.empty()
            final_state = graph.invoke(initial_input)
            
            final_response = (
                final_state.get('itinerary') or 
                final_state.get('draft_itinerary') or 
                final_state['messages'][-1].content
            )
            
            status_container.empty()
            st.success("Itinerary Ready!")
            
            # Display Metrics
            col1, col2, col3 = st.columns(3)
            dist = final_state.get('distance_km', 0)
            dur = final_state.get('duration_days', 0)
            cost = final_state.get('total_cost_inr', 0)
            
            col1.metric("Total Distance", f"{dist:.1f} km")
            col2.metric("Duration", f"{dur} Days")
            col3.metric("Est. Cost", f"₹{cost:,.0f}")
            
            st.markdown("### 🗺️ Your Road Trip Itinerary")
            st.markdown(final_response)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
