# tasks/inventory_analysis_task.py
from crewai import Task
from models.state import InventoryInsight

def create_inventory_analysis_task(agent, inventory_metrics) -> Task:
    return Task(
        description=f"""
        Analyze the following pre-calculated inventory metrics:

        {inventory_metrics}

        Evaluate the relationship between sales velocity and financial margins. 
        Determine the classification, risk profile, and optimization strategies.
        """,
        expected_output="""
        A clean JSON object structured exactly with the following fields:
        {
          "product_name": "...",
          "inventory_classification": "...",
          "inventory_risk": "...",
          "key_observation": "...",
          "recommendation": "..."
        }
        """,
        agent=agent,
        output_pydantic=InventoryInsight  # Forces CrewAI to guarantee output adheres perfectly to your Pydantic schema
    )