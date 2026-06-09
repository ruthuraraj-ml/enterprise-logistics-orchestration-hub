from crewai import Agent

from config.llms import route_llm


def create_route_analyst():

    return Agent(
        role="Route Analyst",

        goal="""
        Analyze logistics and delivery performance metrics
        to identify operational bottlenecks, delivery risks,
        and geographic inefficiencies.
        """,

        backstory="""
        You are a senior logistics analyst specializing
        in transportation efficiency, route optimization,
        delivery risk assessment, and geospatial logistics.
        Your expertise lies in identifying delivery
        bottlenecks and recommending operational improvements.
        """,

        llm=route_llm,

        verbose=True
    )