
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from app.state import TripState
from app.agents import planner_node, local_expert_node, logistics_node, finance_node
from app.tools import tools

# Load environment variables
load_dotenv()

# Define the graph
builder = StateGraph(TripState)

# Add Nodes
builder.add_node("planner", planner_node)
builder.add_node("logistics", logistics_node)
builder.add_node("finance", finance_node)
builder.add_node("local_expert", local_expert_node)
builder.add_node("planner_tools", ToolNode(tools))
builder.add_node("expert_tools", ToolNode(tools))

# Define Routing Logic
def planner_router(state: TripState):
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "planner_tools"
    # Linear flow: Planner -> Logistics
    return "logistics"

def expert_router(state: TripState):
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "expert_tools"
    return END

# Define Edges
builder.add_edge(START, "planner")

builder.add_conditional_edges(
    "planner",
    planner_router,
    {"planner_tools": "planner_tools", "logistics": "logistics"}
)
builder.add_edge("planner_tools", "planner")

# From Planner (via router) -> Logistics -> Finance -> Local Expert
builder.add_edge("logistics", "finance")
builder.add_edge("finance", "local_expert")

builder.add_conditional_edges(
    "local_expert",
    expert_router,
    {"expert_tools": "expert_tools", END: END}
)
builder.add_edge("expert_tools", "local_expert")

# Compile
graph = builder.compile()

def main():
    print("Welcome to the Multi-Agent Road Trip Planner!")
    origin = input("Enter start location: ")
    destination = input("Enter destination: ")
    interests = input("Enter interests (e.g., history, food, nature): ")
    requested_duration = int(input("Enter trip duration (Days): ") or "4")
    budget = float(input("Enter budget (₹): ") or "25000")
    
    initial_input = {
        "messages": [HumanMessage(content=f"Plan a road trip from {origin} to {destination}. Interests: {interests}")],
        "origin": origin,
        "destination": destination,
        "interests": interests,
        "requested_duration": requested_duration,
        "budget": budget
    }
    
    print("\nProcessing... (This may take a minute)\n")
    # Use invoke for simplicity to get final result, but stream for visibility
    final_state = graph.invoke(initial_input)
    
    print("\n=== Final Itinerary ===\n")
    # Print the last message which should be the Local Expert's refined plan
    print(final_state['messages'][-1].content)

if __name__ == "__main__":
    main()
