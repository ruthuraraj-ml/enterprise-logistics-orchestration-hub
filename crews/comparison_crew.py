from crewai import Crew

from agents.comparison_agent import (
    create_comparison_agent
)

from tasks.comparison_task import (
    create_comparison_task
)


def run_comparison_crew(
    strategies
):

    agent = create_comparison_agent()

    task = create_comparison_task(
        agent,
        strategies
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    return crew.kickoff()