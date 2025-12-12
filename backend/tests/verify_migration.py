
import asyncio
from app.agents.agent import build_graph

async def verify_graph():
    print("Verifying LangGraph construction...")
    try:
        graph = build_graph()
        print("Graph built successfully!")
        
        # Print graph structure
        print("\nGraph Nodes:")
        for node in graph.nodes:
            print(f"- {node}")
            
        print("\nVerification successful.")
    except Exception as e:
        print(f"\nVerification FAILED: {e}")
        raise e

if __name__ == "__main__":
    asyncio.run(verify_graph())
