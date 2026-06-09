from crewai import Crew

from agents.strategist import (
    create_strategist
)

from tasks.strategy_task import (
    create_strategy_task
)


def run_strategy_crew(
    inventory_insights,
    route_insights,
    memory_context=None
):

    strategist = create_strategist()

    # Pass memory context down into the task layer
    task = create_strategy_task(
        strategist,
        inventory_insights,
        route_insights,
        memory_context=memory_context
    )

    crew = Crew(
        agents=[strategist],
        tasks=[task],
        verbose=True
    )

    return crew.kickoff()