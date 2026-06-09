from crewai import Agent

from config.llms import strategist_llm


def create_comparison_agent():

    return Agent(
        role="Supply Chain Portfolio Analyst",

        goal="""
        Compare multiple product optimization
        strategies and identify where management
        should invest resources.
        """,

        backstory="""
        You are a senior portfolio analyst
        responsible for allocating logistics,
        inventory, and infrastructure investments
        across competing product lines.
        """,

        llm=strategist_llm,

        verbose=True
    )