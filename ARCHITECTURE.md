# Architecture Documentation

## Overview
The Multi-Agent Road Trip Planner uses a **LangGraph** StateGraph to orchestrate a collaboration between two primary agents:
1.  **Planner Agent**: Responsible for the high-level logistics, route planning, and day-by-day structure.
2.  **Local Expert Agent**: Responsible for enriching the itinerary with cultural depth, food recommendations, and "hidden gems".

## Workflow
1.  **Input**: User provides Origin, Destination, Interests, **Budget (₹)**, and **Trip Duration**.
2.  **Planner Node**: Generates a 1st draft itinerary.
3.  **Logistics Node**: Calculates exact round-trip distance via search and estimates travel days.
4.  **Finance Node**: Calculates a detailed breakdown of Fuel, Stay, and Food costs (India 2026 specs).
5.  **Local Expert Node**: Takes all previous data and produces a polished, budget-aware final itinerary with local secrets.
6.  **Output**: Final plan shown in the Streamlit UI with comparison metrics.

## Tech Stack
-   **LangGraph**: State management and cyclic graph execution.
-   **LangChain Groq**: Interface for Llama 3 (70b-versatile).
-   **Streamlit**: Web UI for user interaction.
-   **DuckDuckGo Search**: Real-time web information.

## Directory Structure
-   `app/`: Core logic modules.
    -   `agents.py`: Agent prompts and LLM binding.
    -   `state.py`: Shared state definition (`TripState`).
    -   `tools.py`: Search tool implementation.
    -   `ui.py`: Streamlit frontend.
-   `main.py`: CLI entry point and graph definition.
