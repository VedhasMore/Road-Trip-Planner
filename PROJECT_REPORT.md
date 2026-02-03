# 🚗 Multi-Agent Road Trip Planner - Project Report

## Overview
The **Multi-Agent Road Trip Planner** is an AI-powered travel assistant designed specifically for the Indian context. It leverages a team of specialized AI agents to handle different aspects of trip planning: itinerary generation, logistics (distance/duration), and finance (cost estimation).

## Key Features
- **Intelligent Itinerary Generation**: Day-by-day plans tailored to user interests (e.g., historical sites, local food).
- **India-Specific Logistics**: Calculates realistic driving distances and travel times considering Indian road conditions (55 km/h avg speed).
- **Dynamic Cost Estimation**: Estimates fuel, accommodation, and food costs in INR using 2026 market rates.
- **Budget & Duration Constraints**: Respects user-defined budget and trip length, with a status indicator (Within/Over Budget).
- **Local Expertise**: Enriches plans with "hidden gems," authentic food spots, and cultural context.
- **Modern UI**: A clean, interactive Streamlit dashboard.

## System Architecture
The system is built on **LangGraph**, using a linear state machine flow:
1. **Planner Agent**: Researches and creates the base itinerary.
2. **Logistics Agent**: Uses search tools to find exact distances and calculate realistic travel days.
3. **Finance Agent**: Projects expenses based on distance and duration.
4. **Local Expert Agent**: Polishes the final response into a user-ready guide.

## Technology Stack
- **LangGraph**: Orchestrates the multi-agent workflow and state management.
- **LangChain**: Interface for Large Language Models (LLMs) and tools.
- **Groq (Llama 3.3 70B)**: High-speed, high-intelligence LLM for agent logic.
- **Streamlit**: Web-based user interface.
- **DuckDuckGo Search**: Real-time information gathering.
