from crewai import Agent
from config.llms import inventory_llm


def create_inventory_analyst():

    return Agent(
        role="Inventory Analyst",

        goal="""
        Analyze inventory performance metrics and identify
        inventory optimization opportunities.
        """,

        backstory="""
        You are a senior supply chain analyst specializing
        in inventory optimization, sales velocity analysis,
        and product profitability assessment.
        You focus on identifying high-performing products,
        slow-moving inventory, and operational risks.
        """,
        llm=inventory_llm,
        verbose=True
    )