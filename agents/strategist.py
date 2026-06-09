from crewai import Agent

from config.llms import strategist_llm


def create_strategist():

    return Agent(
        role="Optimization Strategist",

        goal="""
        Develop logistics optimization strategies
        using inventory and route analysis insights.
        """,

        backstory="""
        You are a senior logistics optimization consultant.

        Your expertise lies in balancing inventory
        performance, delivery reliability, operational
        costs, customer satisfaction, and supply chain risk.

        You synthesize findings from multiple analysts
        and convert them into actionable optimization plans.
        """,

        llm=strategist_llm,

        verbose=True
    )